import PCA9865Driver
import MCP23S17Driver
import time
import UsrDefClasses
import constants as C

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

   def __init__(self, PwrCtrl, AudCtrl):
      self.PowerCtrl = PwrCtrl
      self.AudioCtrl = AudCtrl

   def RunDoor(self):
      Counter = 0
      print(__name__, " -> Power Satemachine is running")
      while self.PowerCtrl.StateMachineGo:
         #Heartbeat
         Counter = Counter + 1
         if Counter > C.HEARTBEAT:
            print(__name__, " -> Power Statemachine heartbeat")
            Counter = 0

         time.sleep(C.THREADTIMEDELAY)

         #Adjust Front Door
         if self.PowerCtrl.FrontDoor == 1:
            self.PreampFrontDoor.Open()
         else:
            self.PreampFrontDoor.Close()
      print(__name__, " -> Power Control Thread Terminated")

   def RunAudio(self):
      Counter = 0
      Delay = C.PWMONDELAY + 1
      print(__name__, " -> Audio Satemachine is running")
      while self.AudioCtrl.StateMachineGo:
         #Heartbeat
         Counter = Counter + 1
         if Counter > C.HEARTBEAT:
            print(__name__, " -> Audio Statemachine heartbeat")
            Counter = 0

         time.sleep(C.THREADTIMEDELAY)

	 #Delay for channel activation
         if Delay <= C.PWMONDELAY + 1:
            Delay = Delay + 1
         if Delay == C.PWMONDELAY:
            self.PreampAudio.DisableChannel(C.CONTROLVOLUMECH)
            self.PreampAudio.DisableChannel(C.CONTROLBASSCH)
            self.PreampAudio.DisableChannel(C.CONTROLMIDDLECH)
            self.PreampAudio.DisableChannel(C.CONTROLTREBBLECH)

         #Adjust audio controls
         if self.AudioCtrl.Volume != self.Volume:
            Delay = 0
            self.Volume = self.AudioCtrl.Volume
            print(__name__, " -> Volume Change: ", self.Volume)
            self.PreampAudio.Enable()
            self.PreampAudio.SetVolume(self.Volume)

         if self.AudioCtrl.Bass != self.Bass:
            Delay = 0
            self.Bass = self.AudioCtrl.Bass
            print(__name__, " -> Bass Change: ", self.Bass)
            self.PreampAudio.Enable()
            self.PreampAudio.SetBass(self.Bass)

         if self.AudioCtrl.Middle != self.Middle:
            Delay = 0
            self.Middle = self.AudioCtrl.Middle
            print(__name__, " -> Middle Change: ", self.Middle)
            self.PreampAudio.Enable()
            self.PreampAudio.SetMiddle(self.Middle)

         if self.AudioCtrl.Trebble != self.Trebble:
            Delay = 0
            self.Trebble = self.AudioCtrl.Trebble
            print(__name__, " -> Trebble Change: ", self.Trebble)
            self.PreampAudio.Enable()
            self.PreampAudio.SetBass(self.Trebble)

      print(__name__, " -> Audio Control Thread Terminated")

   def RunLed(self):
      Counter = 0
      Blink = 0
      BlinkCounter = 0

      print(__name__, " -> Led Satemachine is running")
      while self.PowerCtrl.StateMachineGo or self.AudioCtrl.StateMachineGo:
         #Heartbeat
         Counter = Counter + 1
         if Counter > C.HEARTBEAT:
            print(__name__, " -> Led Statemachine heartbeat")
            Counter = 0

         time.sleep(C.THREADTIMEDELAY)

         #Blink gerator
         BlinkCounter = BlinkCounter + 1
         if BlinkCounter >= (C.LEDBLINKPERIOD // 2):
            Blink = 0
         else:
            Blink = 4096
         if BlinkCounter >= C.LEDBLINKPERIOD:
            BlinkCounter = 0

         #Control Leds
         if self.MainPower == 0:
            self.PreampLeds.SetBrightness(C.LEDMAINPOWER, 0)
            self.MainPower = 1

         if self.PowerCtrl.PreampPower == 1:
            if self.PowerCtrl.LineOutput == 1:
               self.PreampLeds.SetBrightness(C.LEDSTANDBY, 0)
            else:
               self.PreampLeds.SetBrightness(C.LEDSTANDBY, Blink)
         else:
            self.PreampLeds.SetBrightness(C.LEDSTANDBY, 4096)
         self.PreampPower = self.PowerCtrl.PreampPower

         if self.AudioCtrl.Select == 1:
            self.PreampLeds.SetBrightness(C.LEDMEDIAPLAYER, 0)
         else:
            if self.AudioCtrl.PreSelect == 1:
               self.PreampLeds.SetBrightness(C.LEDMEDIAPLAYER, Blink)
            else:
               self.PreampLeds.SetBrightness(C.LEDMEDIAPLAYER, 4096)

         if self.AudioCtrl.Select == 2:
            self.PreampLeds.SetBrightness(C.LEDENETRADIO, 0)
         else:
            if self.AudioCtrl.PreSelect == 2:
               self.PreampLeds.SetBrightness(C.LEDENETRADIO, Blink)
            else:
               self.PreampLeds.SetBrightness(C.LEDENETRADIO, 4096)

         if self.AudioCtrl.Select == 3:
            self.PreampLeds.SetBrightness(C.LEDDVDPLAYER, 0)
         else:
            if self.AudioCtrl.PreSelect == 3:
               self.PreampLeds.SetBrightness(C.LEDDVDPLAYER, Blink)
            else:
               self.PreampLeds.SetBrightness(C.LEDDVDPLAYER, 4096)

         if self.AudioCtrl.Select == 4:
            self.PreampLeds.SetBrightness(C.LEDAUXILIARY, 0)
         else:
            if self.AudioCtrl.PreSelect == 4:
               self.PreampLeds.SetBrightness(C.LEDAUXILIARY, Blink)
            else:
               self.PreampLeds.SetBrightness(C.LEDAUXILIARY, 4096)

      print(__name__, " -> Led Control Thread Terminated")

   def RunRelay(self):
      Counter = 0

      print(__name__, " -> Relay Satemachine is running")
      while self.PowerCtrl.StateMachineGo or self.AudioCtrl.StateMachineGo:
         #Heartbeat
         Counter = Counter + 1
         if Counter > C.HEARTBEAT:
            print(__name__, " -> Relay Statemachine heartbeat")
            Counter = 0

         time.sleep(C.LARGETHREADTIMEDELAY)

         if self.PowerCtrl.PreampPower == 1:
            self.MCP23S17.PowerOn()
         else:
            self.MCP23S17.PowerOff()

         if self.PowerCtrl.LineOutput == 1:
            self.MCP23S17.SwitchLineOutOn()
         else:
            self.MCP23S17.SwitchLineOutOff()

         self.MCP23S17.InputSelect(self.AudioCtrl.Select)

      print(__name__, " -> Relay Control Thread Terminated")
