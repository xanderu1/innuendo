import smbus
import time
import constants as C
from threading import Lock

#------------------------------------------------
# Servo Class
#------------------------------------------------

class PCA9865:
   I2C_bus = None
   I2CLock = Lock()

   def __init__(self, PortNr):
      self.I2CLock.acquire()
      try:
         print(__name__, " -> Opening I2C-port: ", PortNr)
         self.I2C_bus = smbus.SMBus( PortNr )    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
         print(__name__, " -> Initializing I2C PWM Driver for Servo control")
         self.I2C_bus.write_byte_data(C.I2CPCA9865ADDRESS,
                                       C.I2CPCA9865PRESCALREG,
                                        C.I2CPCA9865PRESCAL50HZ)
         self.I2C_bus.write_byte_data(C.I2CPCA9865ADDRESS,
                                       C.I2CPCA9865MODE1REG,
                                        C.I2CPCA9865AION) #disable out subadress increment
         self.I2C_bus.write_byte_data(C.I2CPCA9865ADDRESS,
                                       C.I2CPCA9865MODE2REG,
                                        C.I2CPCA9865PUSHPULL | C.I2CPCA9865INVERTER) #inverting output + PushPull
      except:
         print(__name__, " -> unable to open I2C-port: ", PortNr)
      self.I2CLock.release()

   def Enable(self):
      print(__name__, " -> Enable Servo Driver")
      self.I2CLock.acquire()
      self.I2C_bus.write_byte_data(C.I2CPCA9865ADDRESS,
                                    C.I2CPCA9865MODE1REG,
                                     C.I2CPCA9865AION & C.I2CPCA9865SLEEPOFF) #enable out subadress increment
      self.I2CLock.release()

   def Disable(self):
      print(__name__, " -> Disable Servo Driver")
      self.I2CLock.acquire()
      self.I2C_bus.write_byte_data(C.I2CPCA9865ADDRESS,
                                    C.I2CPCA9865MODE1REG,
                                     C.I2CPCA9865AION | C.I2CPCA9865SLEEPON) #disable out subadress increment
      self.I2CLock.release()

   def SetPosition(self, ServoNr, fAngle):
      print(__name__, " -> Servo number: ", ServoNr, " set to angle: ", fAngle)
      if(ServoNr >= C.I2CPCA9865MINCH and ServoNr <= C.I2CPCA9865MAXCH):
         if(fAngle >= C.SERVOMINANGLE and fAngle <= C.SERVOMAXANGLE):
            ServoNr = ServoNr * C.SERVOREGWIDTH + C.SERVOREGBASE
            iOnPWM = int(round(C.PWMOFFSET + fAngle * C.PWMGAIN))
            iTmp1 = iOnPWM % 256
            iTmp2 = iOnPWM // 256
            iOffPWM = 4096 - iOnPWM
            iTmp3 = iOffPWM % 256
            iTmp4 = iOffPWM // 256
            Position = [iTmp1, iTmp2, iTmp3, iTmp4]
            self.I2CLock.acquire()
            self.I2C_bus.write_i2c_block_data(C.I2CPCA9865ADDRESS, ServoNr, Position)
            self.I2CLock.release()

   def SetBrightness(self, LedNr, Lumix):
      #print(__name__, " -> Led number: ", LedNr, " set value: ", Lumix)
      if(LedNr >= C.I2CPCA9865MINCH and LedNr <= C.I2CPCA9865MAXCH):
         if(Lumix >= 0 and Lumix <= 4096):
            LedNr = LedNr * C.SERVOREGWIDTH + C.SERVOREGBASE
            iOnPWM = int(Lumix)
            iTmp1 = iOnPWM % 256
            iTmp2 = iOnPWM // 256
            iOffPWM = 4095 - iOnPWM
            iTmp3 = iOffPWM % 256
            iTmp4 = iOffPWM // 256
            Brightness = [iTmp1, iTmp2, iTmp3, iTmp4]
            self.I2CLock.acquire()
            self.I2C_bus.write_i2c_block_data(C.I2CPCA9865ADDRESS, LedNr, Brightness)
            self.I2CLock.release()

   def DisableChannel(self, ServoNr):
      print(__name__, " -> Servo number: ", ServoNr, " disabled")
      if(ServoNr >= C.I2CPCA9865MINCH and ServoNr <= C.I2CPCA9865MAXCH):
         ServoNr = ServoNr * C.SERVOREGWIDTH + C.SERVOREGBASE
         iTmp1 = 0
         iTmp2 = 0
         iOffPWM = 4096
         iTmp3 = iOffPWM % 256
         iTmp4 = iOffPWM // 256
         Position = [iTmp1, iTmp2, iTmp3, iTmp4]
         self.I2CLock.acquire()
         self.I2C_bus.write_i2c_block_data(C.I2CPCA9865ADDRESS, ServoNr, Position)
         self.I2CLock.release()

#------------------------------------------------
# Preamp Front Door Class
#------------------------------------------------

class PreampFrontDoor:
   Status = 0
   Servo = None

   def __init__(self, I2CDriver):
      self.Servo = I2CDriver

   def Open(self):
      if self.Status == 0:
         print(__name__, " -> Opening Preamp Front Door")
         self.Servo.Enable()
         for x in range(C.FRONTDOORCLOSEPOS, C.FRONTDOOROPENPOS, C.FRONDDOORPOSSTEP):
            self.Servo.SetPosition(C.FRONTDOORMOTOR1, -x)
            self.Servo.SetPosition(C.FRONTDOORMOTOR2, x)
            time.sleep(C.FRONTDOORSTEPDELAY)
         for x in range(C.KNOBSLEDECLOSEPOS, C.KNOBSLIDEOPENPOS, C.KNOBSLIDEPOSSTEP):
            self.Servo.SetPosition(C.KNOBSLIDEMOTOR1, x)
            self.Servo.SetPosition(C.KNOBSLIDEMOTOR2, -x)
            time.sleep(C.FRONTDOORSTEPDELAY)
         time.sleep(C.FRONTDOORSETTLEDELAY)
         self.Servo.DisableChannel(C.FRONTDOORMOTOR1)
         self.Servo.DisableChannel(C.FRONTDOORMOTOR2)
         self.Servo.DisableChannel(C.KNOBSLIDEMOTOR1)
         self.Servo.DisableChannel(C.KNOBSLIDEMOTOR2)
         self.Status = 1

   def Close(self):
      if self.Status == 1:
         print(__name__, " -> Closing Preamp Front Door")
         self.Servo.Enable()
         for x in range(C.KNOBSLIDEOPENPOS, C.KNOBSLEDECLOSEPOS, -C.KNOBSLIDEPOSSTEP):
            self.Servo.SetPosition(C.KNOBSLIDEMOTOR1, x)
            self.Servo.SetPosition(C.KNOBSLIDEMOTOR2, -x)
            time.sleep(C.FRONTDOORSTEPDELAY)
         for x in range(C.FRONTDOOROPENPOS, C.FRONTDOORCLOSEPOS, -C.FRONDDOORPOSSTEP):
            self.Servo.SetPosition(C.FRONTDOORMOTOR1, -x)
            self.Servo.SetPosition(C.FRONTDOORMOTOR2, x)
            time.sleep(C.FRONTDOORSTEPDELAY)
         time.sleep(C.FRONTDOORSETTLEDELAY)
         self.Servo.DisableChannel(C.FRONTDOORMOTOR1)
         self.Servo.DisableChannel(C.FRONTDOORMOTOR2)
         self.Servo.DisableChannel(C.KNOBSLIDEMOTOR1)
         self.Servo.DisableChannel(C.KNOBSLIDEMOTOR2)
         self.Status = 0

#------------------------------------------------
# Preamp Controls Class
#------------------------------------------------

class PreampControls:
   Volume = 0
   Bass = 0
   Middle = 0
   Trebble = 0
   Servo = None

   def __init__(self, I2CDriver):
      self.Servo = I2CDriver

   def Enable(self):
      self.Servo.Enable()

   def Disable(self):
      self.Servo.Disable()

   def SetVolume(self, fValue):
      print(__name__, " -> Set Volume to: ", fValue)
      if(fValue >= C.CONTROLSZERO and fValue <= C.CONTROLSMAX):
         fServoValue = int(round(C.CONTROLOFFSET + fValue * C.CONTROLGAIN1))
         self.Servo.SetPosition(C.CONTROLVOLUMECH, fServoValue)

   def SetBass(self, fValue):
      print(__name__, " -> Set Bass to: ", fValue)
      if(fValue >= C.CONTROLSMIN and fValue <= C.CONTROLSMAX):
         fServoValue = int(round(fValue * C.CONTROLGAIN2))
         self.Servo.SetPosition(C.CONTROLBASSCH, fServoValue)

   def SetMiddle(self, fValue):
      print(__name__, " -> Set Middle to: ", fValue)
      if(fValue >= C.CONTROLSMIN and fValue <= C.CONTROLSMAX):
         fServoValue = int(round(fValue * C.CONTROLGAIN2))
         self.Servo.SetPosition(C.CONTROLMIDDLECH, fServoValue)

   def SetTrebble(self, fValue):
      print(__name__, " -> Set Trebble to: ", fValue)
      if(fValue >= C.CONTROLSMIN and fValue <= C.CONTROLSMAX):
         fServoValue = int(round(fValue * C.CONTROLGAIN2))
         self.Servo.SetPosition(C.CONTROLTREBBLECH, fServoValue)

   def DisableChannel(self, ServoNr):
      self.Servo.DisableChannel(ServoNr)

#------------------------------------------------
# Preamp Controls Class
#------------------------------------------------

class LedControls:
   Led = None

   def __init__(self, I2CDriver):
      self.Led = I2CDriver

   def Enable(self):
      self.Led.Enable()

   def SetBrightness(self, LedNr, Brightness):
      self.Led.SetBrightness(LedNr, Brightness)
