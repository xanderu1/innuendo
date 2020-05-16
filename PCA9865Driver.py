import smbus
import time
import constants as c
from threading import Lock

# ------------------------------------------------
# Servo Class
# ------------------------------------------------


class PCA9865:
    I2C_bus = None
    I2CLock = Lock()

    def __init__(self, port_nr):
        self.I2CLock.acquire()
        try:
            print(__name__, " -> Opening I2C-port: ", port_nr)
            self.I2C_bus = smbus.SMBus(port_nr)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
            print(__name__, " -> Initializing I2C PWM Driver for Servo control")
            self.I2C_bus.write_byte_data(c.I2CPCA9865ADDRESS,
                                         c.I2CPCA9865PRESCALREG,
                                         c.I2CPCA9865PRESCAL50HZ)
            self.I2C_bus.write_byte_data(c.I2CPCA9865ADDRESS,
                                         c.I2CPCA9865MODE1REG,
                                         c.I2CPCA9865AION)  # disable out subadress increment
            self.I2C_bus.write_byte_data(c.I2CPCA9865ADDRESS,
                                         c.I2CPCA9865MODE2REG,
                                         c.I2CPCA9865PUSHPULL | c.I2CPCA9865INVERTER)  # inverting output + PushPull
        except:
            print(__name__, " -> unable to open I2C-port: ", port_nr)
        self.I2CLock.release()

    def enable(self):
        print(__name__, " -> enable Servo Driver")
        self.I2CLock.acquire()
        self.I2C_bus.write_byte_data(c.I2CPCA9865ADDRESS,
                                     c.I2CPCA9865MODE1REG,
                                     c.I2CPCA9865AION & c.I2CPCA9865SLEEPOFF)  # enable out subadress increment
        self.I2CLock.release()

    def disable(self):
        print(__name__, " -> disable Servo Driver")
        self.I2CLock.acquire()
        self.I2C_bus.write_byte_data(c.I2CPCA9865ADDRESS,
                                     c.I2CPCA9865MODE1REG,
                                     c.I2CPCA9865AION | c.I2CPCA9865SLEEPON)  # disable out subadress increment
        self.I2CLock.release()

    def set_position(self, servo_nr, fangle):
        print(__name__, " -> Servo number: ", servo_nr, " set to angle: ", fangle)
        if servo_nr >= c.I2CPCA9865MINCH and servo_nr <= c.I2CPCA9865MAXCH:
            if fangle >= c.SERVOMINANGLE and fangle <= c.SERVOMAXANGLE:
                servo_nr = servo_nr * c.SERVOREGWIDTH + c.SERVOREGBASE
                ion_pwm = int(round(c.PWMOFFSET + fangle * c.PWMGAIN))
                itmp1 = ion_pwm % 256
                itmp2 = ion_pwm // 256
                ioff_pwm = 4096 - ion_pwm
                itmp3 = ioff_pwm % 256
                itmp4 = ioff_pwm // 256
                position = [itmp1, itmp2, itmp3, itmp4]
                self.I2CLock.acquire()
                self.I2C_bus.write_i2c_block_data(c.I2CPCA9865ADDRESS, servo_nr, position)
                self.I2CLock.release()

    def set_brightness(self, led_nr, lumix):
        # print(__name__, " -> Led number: ", led_nr, " set value: ", lumix)
        if led_nr >= c.I2CPCA9865MINCH and led_nr <= c.I2CPCA9865MAXCH:
            if lumix >= 0 and lumix <= 4096:
                led_nr = led_nr * c.SERVOREGWIDTH + c.SERVOREGBASE
                ion_pwm = int(lumix)
                itmp1 = ion_pwm % 256
                itmp2 = ion_pwm // 256
                ioff_pwm = 4095 - ion_pwm
                itmp3 = ioff_pwm % 256
                itmp4 = ioff_pwm // 256
                brightness = [itmp1, itmp2, itmp3, itmp4]
                self.I2CLock.acquire()
                self.I2C_bus.write_i2c_block_data(c.I2CPCA9865ADDRESS, led_nr, brightness)
                self.I2CLock.release()

    def disable_channel(self, servo_nr):
        print(__name__, " -> Servo number: ", servo_nr, " disabled")
        if servo_nr >= c.I2CPCA9865MINCH and servo_nr <= c.I2CPCA9865MAXCH:
            servo_nr = servo_nr * c.SERVOREGWIDTH + c.SERVOREGBASE
            itmp1 = 0
            itmp2 = 0
            ioff_pwm = 4096
            itmp3 = ioff_pwm % 256
            itmp4 = ioff_pwm // 256
            position = [itmp1, itmp2, itmp3, itmp4]
            self.I2CLock.acquire()
            self.I2C_bus.write_i2c_block_data(c.I2CPCA9865ADDRESS, servo_nr, position)
            self.I2CLock.release()
            
# ------------------------------------------------
# Preamp Front Door Class
# ------------------------------------------------


class PreampFrontDoor:
    Status = 0
    Servo = None

    def __init__(self, i2c_driver):
        self.Servo = i2c_driver

    def open(self):
        if self.Status == 0:
            print(__name__, " -> Opening Preamp Front Door")
            self.Servo.enable()
            for x in range(c.FRONTDOORCLOSEPOS, c.FRONTDOOROPENPOS, c.FRONDDOORPOSSTEP):
                self.Servo.set_position(c.FRONTDOORMOTOR1, -x)
                self.Servo.set_position(c.FRONTDOORMOTOR2, x)
                time.sleep(c.FRONTDOORSTEPDELAY)
            for x in range(c.KNOBSLEDECLOSEPOS, c.KNOBSLIDEOPENPOS, c.KNOBSLIDEPOSSTEP):
                self.Servo.set_position(c.KNOBSLIDEMOTOR1, x)
                self.Servo.set_position(c.KNOBSLIDEMOTOR2, -x)
                time.sleep(c.FRONTDOORSTEPDELAY)
            time.sleep(c.FRONTDOORSETTLEDELAY)
            self.Servo.disable_channel(c.FRONTDOORMOTOR1)
            self.Servo.disable_channel(c.FRONTDOORMOTOR2)
            self.Servo.disable_channel(c.KNOBSLIDEMOTOR1)
            self.Servo.disable_channel(c.KNOBSLIDEMOTOR2)
            self.Status = 1

    def close(self):
        if self.Status == 1:
            print(__name__, " -> Closing Preamp Front Door")
            self.Servo.enable()
            for x in range(c.KNOBSLIDEOPENPOS, c.KNOBSLEDECLOSEPOS, -c.KNOBSLIDEPOSSTEP):
                self.Servo.set_position(c.KNOBSLIDEMOTOR1, x)
                self.Servo.set_position(c.KNOBSLIDEMOTOR2, -x)
                time.sleep(c.FRONTDOORSTEPDELAY)
            for x in range(c.FRONTDOOROPENPOS, c.FRONTDOORCLOSEPOS, -c.FRONDDOORPOSSTEP):
                self.Servo.set_position(c.FRONTDOORMOTOR1, -x)
                self.Servo.set_position(c.FRONTDOORMOTOR2, x)
                time.sleep(c.FRONTDOORSTEPDELAY)
            time.sleep(c.FRONTDOORSETTLEDELAY)
            self.Servo.disable_channel(c.FRONTDOORMOTOR1)
            self.Servo.disable_channel(c.FRONTDOORMOTOR2)
            self.Servo.disable_channel(c.KNOBSLIDEMOTOR1)
            self.Servo.disable_channel(c.KNOBSLIDEMOTOR2)
            self.Status = 0

# ------------------------------------------------
# Preamp Controls Class
# ------------------------------------------------


class PreampControls:
    Volume = 0
    Bass = 0
    Middle = 0
    Trebble = 0
    Servo = None

    def __init__(self, i2c_driver):
        self.Servo = i2c_driver

    def enable(self):
        self.Servo.enable()

    def disable(self):
        self.Servo.disable()

    def set_volume(self, fvalue):
        print(__name__, " -> Set Volume to: ", fvalue)
        if fvalue >= c.CONTROLSZERO and fvalue <= c.CONTROLSMAX:
            fservo_value = int(round(c.CONTROLOFFSET + fvalue * c.CONTROLGAIN1))
            self.Servo.set_position(c.CONTROLVOLUMECH, fservo_value)

    def set_bass(self, fvalue):
        print(__name__, " -> Set Bass to: ", fvalue)
        if fvalue >= c.CONTROLSMIN and fvalue <= c.CONTROLSMAX:
            fservo_value = int(round(fvalue * c.CONTROLGAIN2))
            self.Servo.set_position(c.CONTROLBASSCH, fservo_value)

    def set_middle(self, fvalue):
        print(__name__, " -> Set Middle to: ", fvalue)
        if fvalue >= c.CONTROLSMIN and fvalue <= c.CONTROLSMAX:
            fservo_value = int(round(fvalue * c.CONTROLGAIN2))
            self.Servo.set_position(c.CONTROLMIDDLECH, fservo_value)

    def set_trebble(self, fvalue):
        print(__name__, " -> Set Trebble to: ", fvalue)
        if fvalue >= c.CONTROLSMIN and fvalue <= c.CONTROLSMAX:
            fservo_value = int(round(fvalue * c.CONTROLGAIN2))
            self.Servo.set_position(c.CONTROLTREBBLECH, fservo_value)

    def disable_channel(self, servo_nr):
        self.Servo.disable_channel(servo_nr)

# ------------------------------------------------
# Preamp Controls Class
# ------------------------------------------------


class LedControls:
    Led = None

    def __init__(self, i2c_driver):
        self.Led = i2c_driver

    def enable(self):
        self.Led.enable()

    def set_brightness(self, led_nr, brightness):
        self.Led.set_brightness(led_nr, brightness)
