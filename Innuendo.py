import sys
from aiohttp import web
from socketio import AsyncServer
import json
from threading import Thread
import constants as C
import UsrDefClasses
import StateMachines as SM

#------------------------------------------------
# Variables
#------------------------------------------------

sio = AsyncServer()
app = web.Application()
sio.attach(app)
AudioCtrl = UsrDefClasses.AudioControls()
PowerCtrl = UsrDefClasses.PowerControls()
StateMachine = SM.StateMachine(PowerCtrl, AudioCtrl)

#------------------------------------------------
# Functions/ events
#------------------------------------------------

#Retrieving HTML text
def index(request):
    with open( C.HTMLPAGELOCATION ) as f:
        return web.Response(text=f.read(), content_type='text/html')

#on receiving nu audio control signals
@sio.on( C.SOCKETIOPREAMPCTRL )
async def PreampControl_message(sid, message):
    global AudioCtrl
    print(__name__, " -> Client Control Message: " , sid, ": ", message)
    AudioCtrl.UpdatePreampControls(sid, message)
    await sio.emit( C.SOCKETIOPREAMPFB, AudioCtrl.ReturnPreampFeedback() )

#on receiving powermanagement control signals
@sio.on( C.SOCKETIOPOWERCTRL )
async def PowerControl_message(sid, message):
    global PowerCtrl
    print(__name__, " -> Client Power Message: " , sid, ": ", message)
    PowerCtrl.UpdatePowerControls(sid, message)
    await sio.emit( C.SOCKETIOPOWERFB, PowerCtrl.ReturnPowerFeedback() )

#on connect event handler
@sio.event
def connect(sid, environ):
    print(__name__, ' -> Client Connect ', sid)

#on disconnect event handler
@sio.event
def disconnect(sid):
    print(__name__, ' -> Client Disconnect ', sid)

#------------------------------------------------
# Program
#------------------------------------------------

#starting statemachines in thread
Thread1 = Thread(target=StateMachine.RunDoor)
Thread1.start()
Thread2 = Thread(target=StateMachine.RunAudio)
Thread2.start()
Thread3 = Thread(target=StateMachine.RunLed)
Thread3.start()
Thread4 = Thread(target=StateMachine.RunRelay)
Thread4.start()

app.router.add_get('/', index)
# start socketio server
if __name__ == '__main__':
    web.run_app(app)
