# ------------------------------------------------
# Global Constants
# ------------------------------------------------

# JSON key constants
JSONKEYVOLUMECTRL = 'VolumeCtrl'
JSONKEYBASSCTRL = 'BassCtrl'
JSONKEYMIDDLECTRL = 'MiddleCtrl'
JSONKEYTREBBLECTRL = 'TrebbleCtrl'
JSONKEYSELECTCTRL = 'SelectCtrl'
JSONKEYFRONTDOORCTRL = 'FrontDoorCtrl'
JSONKEYPREAMPPOWERCTRL = 'PreampPowerCtrl'
JSONKEYLINEOUTPUTCTRL = 'LineOutputCtrl'
JSONKEYVOLUMEFB = 'VolumeFB'
JSONKEYBASSFB = 'BassFB'
JSONKEYMIDDLEFB = 'MiddleFB'
JSONKEYTREBBLEFB = 'TrebbleFB'
JSONKEYSELECTFB = 'SelectFB'
JSONKEYFRONTDOORFB = 'FrontDoorFB'
JSONKEYPREAMPPOWERFB = 'PreampPowerFB'
JSONKEYLINEOUTPUTFB = 'LineOutputFB'
JSONKEYCMDSTATEFB = 'CmdStateFB'
JSONKEYURLSTATEFB = 'UrlStateFB'
JSONKEYINETRADIO = "inetradio"
JSONKEYNASSERVERS = "nasservers"
JSONKEYTITLE = "title"
JSONKEYLINK = "link"
JSONKEYSTART = "start"
JSONKEYLENGTH = "length"
JSONKEYIP = "ip"
JSONKEYDIRECTORY = "directory"
JSONKEYUSERNAME = "username"
JSONKEYPASSWORD = "password"

# Socketio constants
SOCKETIOPREAMPCTRL = 'preampcontrol'
SOCKETIOPOWERCTRL = 'powercontrol'
SOCKETIOMEDIACTRL = 'mediaplayerctrl'
SOCKETIOPREAMPFB = 'preampfeedback'
SOCKETIOPOWERFB = 'powerfeedback'

# PCA9865 driver constants
I2CPCA9865ADDRESS = 0x40
I2CPCA9865MODE1REG = 0x00
I2CPCA9865MODE2REG = 0x01
I2CPCA9865PUSHPULL = 0x04
I2CPCA9865INVERTER = 0x10
I2CPCA9865AION = 0x20
I2CPCA9865SLEEPON = 0x10
I2CPCA9865SLEEPOFF = 0xEF
I2CPCA9865MAXCH = 15
I2CPCA9865MINCH = 0
I2CPCA9865PRESCALREG = 0xFE
I2CPCA9865PRESCAL50HZ = 0x79

# MCP23S17 driver constants
SPIMCP23S17ADRESS = 0x40
SPIMCP23S17GPIOAREG = 0x12
SPIMCP23S17IODIRA = 0x00
SPIMCP23S17IODIRB = 0x01
SPIMCP23S17CLOCK = 7629

# Servo constants
SERVOMAXANGLE = 95
SERVOMINANGLE = -95
SERVOREGWIDTH = 4
SERVOREGBASE = 6
PWMOFFSET = 161.5
PWMGAIN = 1.116666666

# Preamp Front Door constants
FRONTDOORMOTOR1 = 0
FRONTDOORMOTOR2 = 1
FRONTDOORCLOSEPOS = -91
FRONTDOOROPENPOS = 91
FRONDDOORPOSSTEP = 10
FRONTDOORSTEPDELAY = 0.03
FRONTDOORSETTLEDELAY = 0.2
KNOBSLIDEMOTOR1 = 2
KNOBSLIDEMOTOR2 = 3
KNOBSLEDECLOSEPOS = -91
KNOBSLIDEOPENPOS = 91
KNOBSLIDEPOSSTEP = 10

# Audio Controls constants
CONTROLVOLUMECH = 4
CONTROLBASSCH = 5
CONTROLMIDDLECH = 6
CONTROLTREBBLECH = 7
CONTROLSMAX = 100
CONTROLSMIN = -100
CONTROLSZERO = 0
CONTROLOFFSET = -90
CONTROLGAIN1 = 1.8
CONTROLGAIN2 = 0.9

# LED controls constants
LEDBLINKPERIOD = 6
LEDMAINPOWER = 8
LEDSTANDBY = 9
LEDMEDIAPLAYER = 10
LEDENETRADIO = 11
LEDDVDPLAYER = 12
LEDAUXILIARY = 13

# Relay control constants
RELAYPREAMPPOWER = 0x08
RELAYPREAMPLINEOUT = 0x10
RELAYPREAMPNOCHANNEL = 0xF8
RELAYPREAMPINTERNALCHANNEL = 0x04
RELAYPREAMPDVDCHANNEL = 0x02
RELAYPREAMPAUXCHANNEL = 0x01

# General constants
HEARTBEAT = 50
PWMONDELAY = 4
THREADTIMEDELAY = 0.1
LARGETHREADTIMEDELAY = 0.5
MAXAUDIOINPUTS = 4

# Application Router
GETINDEXROUTE = ["/",
                 "/var/www/html/index.htm",
                 "text/html"]
GETCSSROUTE = ["/style.css",
               "/var/www/html/style.css",
               "text/css"]
GETJQUERY = ["/jquery-1.10.1.min.js",
             "/var/www/html/jquery-1.10.1.min.js",
             "text/script"]
GETSCGRIPT = ["/script.js",
              "/var/www/html/script.js",
              "text/script"]
GETSOCKETIO = ["/socket.io.js",
               "/var/www/html/socket.io.js",
               "text/script"]
GETIMAGE338 = ["/image338.jpg",
               "/var/www/html/image338.jpg",
               "image/jpeg"]
GETIMAGE293 = ["/image293.png",
               "/var/www/html/image293.png",
               "image/png"]
GETIMAGE299 = ["/image299.png",
               "/var/www/html/image299.png",
               "image/png"]
GETIMAGE357 = ["/image357.png",
               "/var/www/html/image357.png",
               "image/png"]
GETIMAGE359 = ["/image359.png",
               "/var/www/html/image359.png",
               "image/png"]
GETIMAGE363 = ["/image363.png",
               "/var/www/html/image363.png",
               "image/png"]
GETIMAGE365 = ["/image365.png",
               "/var/www/html/image365.png",
               "image/png"]
GETIMAGE423 = ["/image423.png",
               "/var/www/html/image423.png",
               "image/png"]
GETIMAGE321 = ["/image321.jpg",
               "/var/www/html/image321.jpg",
               "image/jpeg"]
GETIMAGE325 = ["/image325.jpg",
               "/var/www/html/image325.jpg",
               "image/jpeg"]
GETIMAGE327 = ["/image327.png",
               "/var/www/html/image327.png",
               "image/png"]
GETIMAGE329 = ["/image329.png",
               "/var/www/html/image329.png",
               "image/png"]
GETIMAGE387 = ["/image387.png",
               "/var/www/html/image387.png",
               "image/png"]
GETIMAGE389 = ["/image389.png",
               "/var/www/html/image389.png",
               "image/png"]
GETIMAGE391 = ["/image391.png",
               "/var/www/html/image391.png",
               "image/png"]
GETIMAGE393 = ["/image393.png",
               "/var/www/html/image393.png",
               "image/png"]
GETIMAGE463 = ["/image463.jpg",
               "/var/www/html/image463.jpg",
               "image/jpeg"]
GETIMAGE501 = ["/image501.jpg",
               "/var/www/html/image501.jpg",
               "image/jpeg"]
GETIMAGE530 = ["/image530.jpg",
               "/var/www/html/image530.jpg",
               "image/jpeg"]
GETIMAGE364 = ["/image364.png",
               "/var/www/html/image364.png",
               "image/png"]
GETIMAGE373 = ["/image373.png",
               "/var/www/html/image373.png",
               "image/png"]
GETIMAGE342 = ["/image342.png",
               "/var/www/html/image342.png",
               "image/png"]
GETIMAGE360 = ["/image360.png",
               "/var/www/html/image360.png",
               "image/png"]

ROUTES = [GETINDEXROUTE,
          GETCSSROUTE,
          GETJQUERY,
          GETSCGRIPT,
          GETSOCKETIO,
          GETIMAGE338,
          GETIMAGE293,
          GETIMAGE299,
          GETIMAGE357,
          GETIMAGE359,
          GETIMAGE363,
          GETIMAGE365,
          GETIMAGE423,
          GETIMAGE321,
          GETIMAGE325,
          GETIMAGE327,
          GETIMAGE329,
          GETIMAGE357,
          GETIMAGE359,
          GETIMAGE387,
          GETIMAGE389,
          GETIMAGE391,
          GETIMAGE393,
          GETIMAGE463,
          GETIMAGE501,
          GETIMAGE530,
          GETIMAGE364,
          GETIMAGE373,
          GETIMAGE342,
          GETIMAGE360]

# Paths
AUDIOFILES = [".wav", ".wma", ".mp3"]
INITFILEPATH = "/var/www/html/initialisation.json"
NASSERVERSPATH = "/home/pi/innuendo/nasservers/"
RADIOPHP = "/radio.php"
MEDIAPHP = "/media.php"

# MediaPlayer
DEFAULTAUDIOFILE = "~/innuendo/hammer.wma"
DEFAULTAUDIOTITLE = "Hammer to fall"
