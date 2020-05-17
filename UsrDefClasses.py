import json
from threading import Lock
import constants as c
import os
from tinytag import TinyTag

# ------------------------------------------------
# NAS Class
# ------------------------------------------------


class Nas:
    aNasServers = []

    # Reading NAS servers from initialisation.json file
    def mount_nas_servers(self):
        init_file_text = open(c.INITFILEPATH, 'r').read()
        init_file_json = json.loads(init_file_text)
        self.aNasServers = init_file_json[c.JSONKEYNASSERVERS]
        for nasServer in self.aNasServers:
            print(__name__, "-> mounting NAS-server: ", nasServer[c.JSONKEYTITLE])
            cmd_line = c.NASSERVERSPATH + nasServer[c.JSONKEYTITLE] + "/"

            if not os.path.exists(cmd_line):
                print(__name__, " -> directory ", nasServer[c.JSONKEYTITLE], " does not exists, creating directory.")
                cmd_line = "sudo mkdir " + c.NASSERVERSPATH + nasServer[c.JSONKEYTITLE]
                os.system(cmd_line)
            cmd_line = "sudo mount -t cifs //" + nasServer[c.JSONKEYIP] \
                       + "/" + nasServer[c.JSONKEYDIRECTORY] \
                       + " -o username=" + nasServer[c.JSONKEYUSERNAME] \
                       + ",password=" + nasServer[c.JSONKEYPASSWORD] \
                       + " " + c.NASSERVERSPATH + nasServer[c.JSONKEYTITLE]
            os.system(cmd_line)

    # Retrieving Directory Contents
    def get_files_from_directory(self, start, length, path):

        class CDirectoryList:
            list = []
            maxLength = 0

        start = start - 1
        tmp = list()
        tmp.clear()
        result = CDirectoryList()
        if start >= 0 and length > 1:
            counter = 0

        # Make sure path is allowed
        if path[:len(c.NASSERVERSPATH)] != c.NASSERVERSPATH:
            print(__name__, " -> source path: ", path[:len(c.NASSERVERSPATH)], 
                  "is not allowed, set path to: ", c.NASSERVERSPATH)
            path = c.NASSERVERSPATH

        # scan directory for audio files and directories
        with os.scandir(path) as items:
            for item in items:
                if not item.name.startswith('.'):
                    if len(item.name) >= 4 and \
                       (item.is_file() and
                       item.name[-4:] in c.AUDIOFILES) or \
                       item.is_dir():
                        counter = counter + 1
                        dir_item = dict()
                        dir_item[c.JSONKEYTITLE] = item.name
                        dir_item[c.JSONKEYDIRECTORY] = str(item.is_dir())
                        dir_item[c.JSONKEYLINK] = item.path
                        tmp.append(dir_item)
        items.close()

        # retrieve title from meta data
        for i in range(len(tmp)):
            if tmp[i]["directory"] == "False":
                try:
                    tag = TinyTag.get(tmp[i]["link"])
                    if tag is not None:
                        if tag.title != "":
                            tmp[i]["title"] = tag.title
                except:
                    tag = ""

        # sort on alphabetic order (CAPS independent) + folders
        mod = True
        while mod:
            mod = False
            for i in range(len(tmp) - 1):
                if tmp[i + 1]["title"].upper() < tmp[i]["title"].upper() or \
                   (tmp[i + 1]["directory"] == "True" and tmp[i]["directory"] == "False"):
                    tmp3 = tmp[i]
                    tmp[i] = tmp[i + 1]
                    tmp[i + 1] = tmp3
                    mod = True

        # retrieve selection
        tmp2 = {}
        if start <= len(tmp):
            if start + length >= len(tmp):
                length = len(tmp) - start
            tmp2 = tmp[start: start + length]

        result.list = tmp2
        result.maxLength = str(len(tmp))
        return str(json.dumps(result.__dict__))

# ------------------------------------------------
# Media Control Class
# ------------------------------------------------


class MediaControls:
    StateMachineGo = True
    cmdState = "stop"
    urlState = c.DEFAULTAUDIOFILE
    cmdReq = "stop"
    urlReq = c.DEFAULTAUDIOFILE
    mPlayer = None
    MediaLock = Lock()

    def return_media_feedback(self):
        return {c.JSONKEYCMDSTATEFB: self.cmdState,
                c.JSONKEYURLSTATEFB: self.urlState}

    def update_media_controls(self, sid, message):
        self.MediaLock.acquire()
        if message.get('TerminateMedia'):
            print(__name__, " -> Terminating Media Thread: ", str(sid))
            self.StateMachineGo = False

        if message.get('cmd') == 'stop' or message.get('cmd') == 'play':
            print(__name__, " -> Media Command received: ", message.get('cmd'))
            self.cmdReq = message.get('cmd')

        if message.get('url') is not None:
            print(__name__, " -> Media URL received: ", message.get('url'))
            self.urlReq = message.get('url')

        self.MediaLock.release()

# ------------------------------------------------
# Audio Control Class
# ------------------------------------------------


class AudioControls:
    StateMachineGo = True
    Volume = 0
    Bass = 0
    Middle = 0
    Trebble = 0
    Select = 1
    PreSelect = 2
    ControlLock = Lock()

    def is_bi_di_audio_ctrl(self, message):
        return message.get(c.JSONKEYBASSCTRL) or message.get(c.JSONKEYMIDDLECTRL) or message.get(c.JSONKEYTREBBLECTRL)

    def change_bi_di_audio_ctrl(self, value, deltavalue):
        value = value + deltavalue
        if value > 100:
            value = 100
        if value < -100:
            value = -100
        return value

    def is_uni_audio_ctrl(self, message):
        return message.get(c.JSONKEYVOLUMECTRL)

    def change_uni_audio_ctrl(self, value, deltavalue):
        value = value + deltavalue
        if value > 100:
            value = 100
        if value < 0:
            value = 0
        return value

    def is_audio_input_ctrl(self, message):
        return message.get(c.JSONKEYSELECTCTRL)

    def change_audio_input_ctrl(self, value):
        if value > 100:
            value = 100
        if value < 0:
            value = 0
        return value

    def return_preamp_feedback(self):
        return {c.JSONKEYVOLUMEFB: self.Volume,
                c.JSONKEYBASSFB: self.Bass,
                c.JSONKEYMIDDLEFB: self.Middle,
                c.JSONKEYTREBBLEFB: self.Trebble,
                c.JSONKEYSELECTFB: self.Select}

    def update_preamp_controls(self, sid, message):
        self.ControlLock.acquire()
        if message.get('TerminateAudio'):
            print(__name__, " -> Terminating Audio Thread:", str(sid))
            self.StateMachineGo = False
        if self.is_uni_audio_ctrl(message):
            if message.get(c.JSONKEYVOLUMECTRL):
                self.Volume = self.change_uni_audio_ctrl(self.Volume, message[c.JSONKEYVOLUMECTRL])
        if self.is_bi_di_audio_ctrl(message):
            if message.get(c.JSONKEYBASSCTRL):
                self.Bass = self.change_bi_di_audio_ctrl(self.Bass, message[c.JSONKEYBASSCTRL])
            if message.get(c.JSONKEYMIDDLECTRL):
                self.Middle = self.change_bi_di_audio_ctrl(self.Middle, message[c.JSONKEYMIDDLECTRL])
            if message.get(c.JSONKEYTREBBLECTRL):
                self.Trebble = self.change_bi_di_audio_ctrl(self.Trebble, message[c.JSONKEYTREBBLECTRL])
        if self.is_audio_input_ctrl(message):
            self.Select = self.change_audio_input_ctrl(message[c.JSONKEYSELECTCTRL])
        self.ControlLock.release()

# ------------------------------------------------
# Power Control Class
# ------------------------------------------------


class PowerControls:
    StateMachineGo = True
    FrontDoor = 0
    PreampPower = 0
    LineOutput = 0
    PowerLock = Lock()

    def change_power_ctrl(self, value):
        if value >= 1:
            value = 1
        else:
            value = 0
        return value

    def return_power_feedback(self):
        return {c.JSONKEYFRONTDOORFB: self.FrontDoor,
                c.JSONKEYPREAMPPOWERFB: self.PreampPower,
                c.JSONKEYLINEOUTPUTFB: self.LineOutput}

    def update_power_controls(self, sid, message):
        self.PowerLock.acquire()
        if message.get('TerminatePower'):
            print(__name__, " -> Terminating Power Thread: ", str(sid))
            self.StateMachineGo = False
        if message.get(c.JSONKEYFRONTDOORCTRL):
            self.FrontDoor = self.change_power_ctrl(message[c.JSONKEYFRONTDOORCTRL])
        if message.get(c.JSONKEYPREAMPPOWERCTRL):
            self.PreampPower = self.change_power_ctrl(message[c.JSONKEYPREAMPPOWERCTRL])
        if message.get(c.JSONKEYLINEOUTPUTCTRL):
            self.LineOutput = self.change_power_ctrl(message[c.JSONKEYLINEOUTPUTCTRL])
        self.PowerLock.release()
