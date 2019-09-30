import json
from threading import Lock
import constants as C

#------------------------------------------------
# Audio Control Class
#------------------------------------------------

class AudioControls:
   StateMachineGo = True
   Volume = 0
   Bass = 0
   Middle = 0
   Trebble = 0
   Select = 1
   PreSelect = 2
   ControlLock = Lock()

   def IsBiDiAudioCtrl(self, message):
      return message.get( C.JSONKEYBASSCTRL ) or message.get( C.JSONKEYMIDDLECTRL ) or message.get( C.JSONKEYTREBBLECTRL )

   def ChangeBiDiAudioCtrl(self, Value, DeltaValue):
      Value = Value + DeltaValue
      if Value > 100:
         Value = 100
      if Value < -100:
         Value = -100
      return Value

   def IsUniAudioCtrl(self, message):
      return message.get( C.JSONKEYVOLUMECTRL )

   def ChangeUniAudioCtrl(self, Value, DeltaValue):
      Value = Value + DeltaValue
      if Value > 100:
         Value = 100
      if Value < 0:
         Value = 0
      return Value

   def IsAudioInputCtrl(self, message):
      return message.get( C.JSONKEYSELECTCTRL )

   def ChangeAudioInputCtrl(self, Value):
      if Value > 100:
         Value = 100
      if Value < 0:
         Value = 0
      return Value

   def ReturnPreampFeedback(self):
      return { C.JSONKEYVOLUMEFB: self.Volume,
                C.JSONKEYBASSFB: self.Bass,
                 C.JSONKEYMIDDLEFB: self.Middle,
                  C.JSONKEYTREBBLEFB: self.Trebble,
                   C.JSONKEYSELECTFB: self.Select}

   def UpdatePreampControls(self, sid, message):
      self.ControlLock.acquire()
      if message.get( 'TerminateAudio' ):
         print(__name__, " -> Terminating Audio Thread")
         self.StateMachineGo = False
      if self.IsUniAudioCtrl( message ):
         if message.get( C.JSONKEYVOLUMECTRL ):
            self.Volume = self.ChangeUniAudioCtrl(self.Volume , message[ C.JSONKEYVOLUMECTRL ])
      if self.IsBiDiAudioCtrl( message ):
         if message.get( C.JSONKEYBASSCTRL ):
            self.Bass = self.ChangeBiDiAudioCtrl(self.Bass , message[ C.JSONKEYBASSCTRL ])
         if message.get( C.JSONKEYMIDDLECTRL ):
            self.Middle = self.ChangeBiDiAudioCtrl(self.Middle , message[ C.JSONKEYMIDDLECTRL ])
         if message.get( C.JSONKEYTREBBLECTRL ):
            self.Trebble = self.ChangeBiDiAudioCtrl(self.Trebble , message[ C.JSONKEYTREBBLECTRL ])
      if self.IsAudioInputCtrl( message ):
         self.Select = self.ChangeAudioInputCtrl(message[ C.JSONKEYSELECTCTRL ] )
      self.ControlLock.release()

#------------------------------------------------
# Power Control Class
#------------------------------------------------

class PowerControls:
   StateMachineGo = True
   FrontDoor = 0
   PreampPower = 0
   LineOutput = 0
   PowerLock = Lock()

   def ChangePowerCtrl(self, Value):
             if Value >= 1:
                Value = 1
             else:
                Value = 0
             return Value

   def ReturnPowerFeedback(self):
      return { C.JSONKEYFRONTDOORFB: self.FrontDoor,
                C.JSONKEYPREAMPPOWERFB: self.PreampPower,
                 C.JSONKEYLINEOUTPUTFB: self.LineOutput}

   def UpdatePowerControls(self, sid, message):
      self.PowerLock.acquire()
      if message.get( 'TerminatePower' ):
         print(__name__, " -> Terminating Power Thread")
         self.StateMachineGo = False
      if message.get( C.JSONKEYFRONTDOORCTRL ):
         self.FrontDoor = self.ChangePowerCtrl(message[ C.JSONKEYFRONTDOORCTRL ])
      if message.get( C.JSONKEYPREAMPPOWERCTRL ):
         self.PreampPower = self.ChangePowerCtrl(message[ C.JSONKEYPREAMPPOWERCTRL ])
      if message.get( C.JSONKEYLINEOUTPUTCTRL ):
         self.LineOutput = self.ChangePowerCtrl(message[ C.JSONKEYLINEOUTPUTCTRL ])
      self.PowerLock.release()
