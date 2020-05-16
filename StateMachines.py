import PCA9865Driver
import MCP23S17Driver
import time
import UsrDefClasses
import constants as c
import subprocess


class StateMachine:
    Go = True
    PowerCtrl = None
    AudioCtrl = None
    MainPower = 0
    PreampPower = 0
    Volume = 0
    Bass = 0
    Middle = 0
    Trebble = 0

    PCA9865 = PCA9865Driver.PCA9865(1)
    MCP23S17 = MCP23S17Driver.MCP23S17(0, 0)
    PreampFrontDoor = PCA9865Driver.PreampFrontDoor(PCA9865)
    PreampAudio = PCA9865Driver.PreampControls(PCA9865)
    PreampLeds = PCA9865Driver.LedControls(PCA9865)
    MPlayer = None

    def __init__(self, pwr_ctrl, aud_ctrl, mp_ctrl):
        self.PowerCtrl = pwr_ctrl
        self.AudioCtrl = aud_ctrl
        self.MediaCtrl = mp_ctrl

    def run_door(self):
        counter = 0
        print(__name__, " -> Power Satemachine is running")
        while self.PowerCtrl.StateMachineGo:
            # Heartbeat
            counter = counter + 1
            if counter > c.HEARTBEAT:
                print(__name__, " -> Power Statemachine heartbeat")
                counter = 0

            time.sleep(c.THREADTIMEDELAY)

            # Adjust Front Door
            if self.PowerCtrl.FrontDoor == 1:
                self.PreampFrontDoor.open()
            else:
                self.PreampFrontDoor.close()
        print(__name__, " -> Power Control Thread Terminated")

    def run_audio(self):
        counter = 0
        delay = c.PWMONDELAY + 1
        print(__name__, " -> Audio Satemachine is running")
        while self.AudioCtrl.StateMachineGo:
            # Heartbeat
            counter = counter + 1
            if counter > c.HEARTBEAT:
                print(__name__, " -> Audio Statemachine heartbeat")
                counter = 0

            time.sleep(c.THREADTIMEDELAY)

            # delay for channel activation
            if delay <= c.PWMONDELAY + 1:
                delay = delay + 1
            if delay == c.PWMONDELAY:
                self.PreampAudio.disable_channel(c.CONTROLVOLUMECH)
                self.PreampAudio.disable_channel(c.CONTROLBASSCH)
                self.PreampAudio.disable_channel(c.CONTROLMIDDLECH)
                self.PreampAudio.disable_channel(c.CONTROLTREBBLECH)

            # Adjust audio controls
            if self.AudioCtrl.Volume != self.Volume:
                delay = 0
                self.Volume = self.AudioCtrl.Volume
                print(__name__, " -> Volume Change: ", self.Volume)
                self.PreampAudio.enable()
                self.PreampAudio.set_volume(self.Volume)

            if self.AudioCtrl.Bass != self.Bass:
                delay = 0
                self.Bass = self.AudioCtrl.Bass
                print(__name__, " -> Bass Change: ", self.Bass)
                self.PreampAudio.enable()
                self.PreampAudio.set_bass(self.Bass)

            if self.AudioCtrl.Middle != self.Middle:
                delay = 0
                self.Middle = self.AudioCtrl.Middle
                print(__name__, " -> Middle Change: ", self.Middle)
                self.PreampAudio.enable()
                self.PreampAudio.set_middle(self.Middle)

            if self.AudioCtrl.Trebble != self.Trebble:
                delay = 0
                self.Trebble = self.AudioCtrl.Trebble
                print(__name__, " -> Trebble Change: ", self.Trebble)
                self.PreampAudio.enable()
                self.PreampAudio.set_bass(self.Trebble)

        print(__name__, " -> Audio Control Thread Terminated")

    def run_led(self):
        counter = 0
        blink_counter = 0

        print(__name__, " -> Led Satemachine is running")
        while self.PowerCtrl.StateMachineGo or self.AudioCtrl.StateMachineGo:
            # Heartbeat
            counter = counter + 1
            if counter > c.HEARTBEAT:
                print(__name__, " -> Led Statemachine heartbeat")
                counter = 0

            time.sleep(c.THREADTIMEDELAY)

            # blink gerator
            blink_counter = blink_counter + 1
            if blink_counter >= (c.LEDBLINKPERIOD // 2):
                blink = 0
            else:
                blink = 4096
            if blink_counter >= c.LEDBLINKPERIOD:
                blink_counter = 0

            # Control Leds
            if self.MainPower == 0:
                self.PreampLeds.set_brightness(c.LEDMAINPOWER, 0)
                self.MainPower = 1

            if self.PowerCtrl.PreampPower == 1:
                if self.PowerCtrl.LineOutput == 1:
                    self.PreampLeds.set_brightness(c.LEDSTANDBY, 0)
                else:
                    self.PreampLeds.set_brightness(c.LEDSTANDBY, blink)
            else:
                self.PreampLeds.set_brightness(c.LEDSTANDBY, 4096)
            self.PreampPower = self.PowerCtrl.PreampPower

            if self.AudioCtrl.Select == 1:
                self.PreampLeds.set_brightness(c.LEDMEDIAPLAYER, 0)
            else:
                if self.AudioCtrl.PreSelect == 1:
                    self.PreampLeds.set_brightness(c.LEDMEDIAPLAYER, blink)
                else:
                    self.PreampLeds.set_brightness(c.LEDMEDIAPLAYER, 4096)

            if self.AudioCtrl.Select == 2:
                self.PreampLeds.set_brightness(c.LEDENETRADIO, 0)
            else:
                if self.AudioCtrl.PreSelect == 2:
                    self.PreampLeds.set_brightness(c.LEDENETRADIO, blink)
                else:
                    self.PreampLeds.set_brightness(c.LEDENETRADIO, 4096)

            if self.AudioCtrl.Select == 3:
                self.PreampLeds.set_brightness(c.LEDDVDPLAYER, 0)
            else:
                if self.AudioCtrl.PreSelect == 3:
                    self.PreampLeds.set_brightness(c.LEDDVDPLAYER, blink)
                else:
                    self.PreampLeds.set_brightness(c.LEDDVDPLAYER, 4096)

            if self.AudioCtrl.Select == 4:
                self.PreampLeds.set_brightness(c.LEDAUXILIARY, 0)
            else:
                if self.AudioCtrl.PreSelect == 4:
                    self.PreampLeds.set_brightness(c.LEDAUXILIARY, blink)
                else:
                    self.PreampLeds.set_brightness(c.LEDAUXILIARY, 4096)

        print(__name__, " -> Led Control Thread Terminated")

    def run_relay(self):
        counter = 0

        print(__name__, " -> Relay Satemachine is running")
        while self.PowerCtrl.StateMachineGo or self.AudioCtrl.StateMachineGo:
            # Heartbeat
            counter = counter + 1
            if counter > c.HEARTBEAT:
                print(__name__, " -> Relay Statemachine heartbeat")
                counter = 0

            time.sleep(c.LARGETHREADTIMEDELAY)

            if self.PowerCtrl.PreampPower == 1:
                self.MCP23S17.power_on()
            else:
                self.MCP23S17.power_off()

            if self.PowerCtrl.LineOutput == 1:
                self.MCP23S17.switch_line_out_on()
            else:
                self.MCP23S17.switch_line_out_off()

            self.MCP23S17.input_select(self.AudioCtrl.Select)

        print(__name__, " -> Relay Control Thread Terminated")

    def run_media(self):
        counter = 0

        print(__name__, " -> Media Satemachine is running")
        while self.MediaCtrl.StateMachineGo:
            # Heartbeat
            counter = counter + 1
            if counter > c.HEARTBEAT:
                print(__name__, " -> Media Statemachine heartbeat")
                counter = 0

            time.sleep(c.THREADTIMEDELAY)

            # terminate mplayer in subprocess if applicable
            if self.MPlayer is not None:
                if self.MediaCtrl.cmdState == "stop" and self.MPlayer.poll() != 0:
                    self.MPlayer.communicate(input=b"q")

            # mplayer play/ stop controls
            if self.MediaCtrl.cmdState != self.MediaCtrl.cmdReq or self.MediaCtrl.urlState != self.MediaCtrl.urlReq:
                if self.MediaCtrl.cmdReq == "play":
                    print(__name__, " -> Start mplayer with URL: ", self.MediaCtrl.urlReq)
                    tmp = self.MediaCtrl.urlReq.replace(' ', '\ ')
                    tmp = tmp.replace('&', '\&')
                    tmp = tmp.replace("(", "\(")
                    tmp = tmp.replace(")", "\)")
                    tmp = tmp.replace("\'", "\\\'")
                    cmdline = "mplayer " + tmp
                    if self.MPlayer is not None:
                        # there is another subprocess active
                        if self.MPlayer.poll() != 0:
                            # The mediaplayer still active
                            self.MPlayer.communicate(input=b"q")
                            self.MPlayer.wait(timeout=3)
                    self.MPlayer = subprocess.Popen(cmdline, shell=True, stdin=subprocess.PIPE, stdout=None)
                    self.MediaCtrl.cmdState = "play"
                    self.MediaCtrl.urlState = self.MediaCtrl.urlReq
                else:
                    print(__name__, " -> Stop mplayer")
                    self.MediaCtrl.cmdState = "stop"
        print(__name__, " -> Media Control Thread Terminated")
