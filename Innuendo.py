import sys
from aiohttp import web
from socketio import AsyncServer
import json
import os
from threading import Thread

import constants as c
import UsrDefClasses
import StateMachines as sM

# ------------------------------------------------
# Variables
# ------------------------------------------------

sio = AsyncServer()
app = web.Application()
sio.attach(app)
AudioCtrl = UsrDefClasses.AudioControls()
PowerCtrl = UsrDefClasses.PowerControls()
MediaCtrl = UsrDefClasses.MediaControls()
NAS = UsrDefClasses.Nas()
StateMachine = sM.StateMachine(PowerCtrl, AudioCtrl, MediaCtrl)
appRoutes = c.ROUTES
iNetRadioJson = list()
link = c.DEFAULTAUDIOFILE
title = c.DEFAULTAUDIOTITLE

# ------------------------------------------------
# Functions/ events
# ------------------------------------------------


def get_handler(request):
    # Get Handler
    global appRoutes
    print(__name__, " -> http request: ", str(request.method), ":", str(request.path))
    j = -1
    for i in range(len(appRoutes)):
        if appRoutes[i][0] == str(request.path):
            j = i
    if j != -1:
        with open(appRoutes[j][1], 'rb') as f:
            return web.Response(body=f.read(), content_type=appRoutes[j][2])


async def radio_post_handler(request):
    # Radio Post Handler
    global title
    global link
    params = None
    if request.body_exists:
        params = await request.post()
    print(__name__, " -> http request: ", str(request.method), ":", str(request.path), ":", params[c.JSONKEYSTART])
    i = int(params[c.JSONKEYSTART]) - 1
    if i < 0 or i > len(iNetRadioJson) - 1:
        i = 0
    title = str(iNetRadioJson[i][c.JSONKEYTITLE])
    link = str(iNetRadioJson[i][c.JSONKEYLINK])
    return web.Response(text='{ "title": "' + title + '", "link": "' + link + '", "maxRadioLink": "' + 
                        str(len(iNetRadioJson)) + '" }', content_type="text/plain")


async def media_post_handler(request):
    # Media Post Handler
    global NAS
    params = None
    if request.body_exists:
        params = await request.post()
    print(__name__, " -> http request: ", str(request.method), ":", str(request.path), ":", 
          params[c.JSONKEYSTART], ":", params[c.JSONKEYLENGTH], ":", params[c.JSONKEYLINK])
    i = int(params[c.JSONKEYSTART])
    length = int(params[c.JSONKEYLENGTH])
    url = str(params[c.JSONKEYLINK])
    response_str = NAS.get_files_from_directory(i, length, url)
    return web.Response(text=response_str, content_type="text/plain")


@sio.on(c.SOCKETIOPREAMPCTRL)
async def preamp_control_message(sid, message):
    # on receiving nu audio control signals
    global AudioCtrl
    print(__name__, " -> Client Control Message: ", sid, ": ", message)
    AudioCtrl.update_preamp_controls(sid, message)
    await sio.emit(c.SOCKETIOPREAMPFB, AudioCtrl.return_preamp_feedback())


@sio.on(c.SOCKETIOPOWERCTRL)
async def power_control_message(sid, message):
    # on receiving power management control signals
    global PowerCtrl
    print(__name__, " -> Client Power Message: ", sid, ": ", message)
    PowerCtrl.update_power_controls(sid, message)
    await sio.emit(c.SOCKETIOPOWERFB, PowerCtrl.return_power_feedback())


@sio.on(c.SOCKETIOMEDIACTRL)
async def media_control_message(sid, message):
    # on receiving media player control signals
    global MediaCtrl
    print(__name__, " -> Client Media Message: ", sid, ": ", message)
    MediaCtrl.update_media_controls(sid, message)


@sio.event
def connect(sid, environ):
    # on connect event handler
    print(__name__, ' -> Client Connect ', sid)


@sio.event
def disconnect(sid):
    # on disconnect event handler
    print(__name__, ' -> Client Disconnect ', sid)

# ------------------------------------------------
# Program
# ------------------------------------------------


Thread1 = Thread(target=StateMachine.run_door)  # starting state machines in thread
Thread1.start()
Thread2 = Thread(target=StateMachine.run_audio)
Thread2.start()
Thread3 = Thread(target=StateMachine.run_led)
Thread3.start()
Thread4 = Thread(target=StateMachine.run_relay)
Thread4.start()
Thread5 = Thread(target=StateMachine.run_media)
Thread5.start()

# route GET handlers
print(__name__, ' -> Added Routes for GET requests')
for i in range(len(appRoutes)):
    print(__name__, ' -> Router.add_Get [', i, ']: ', appRoutes[i][0])
    app.router.add_get(appRoutes[i][0], get_handler)

# route POST handlers
app.router.add_post(c.RADIOPHP, radio_post_handler)
app.router.add_post(c.MEDIAPHP, media_post_handler)

# Reading i-net radio channel from initialisation.json file
initFileText = open(c.INITFILEPATH, 'r').read()
initFileJson = json.loads(initFileText)
iNetRadioJson = initFileJson[c.JSONKEYINETRADIO]

# Mount NAS to "nasserver" directory
NAS.mount_nas_servers()

# start socket-io server
if __name__ == '__main__':
    web.run_app(app, port=5000)