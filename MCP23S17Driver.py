import spidev
import constants as C
from threading import Lock

class MCP23S17:
   SPI_bus = None
   SpiLock = Lock()
   SpiData = 0x00

   def __init__(self, PortNr, CS):
      self.SpiLock.acquire()
      try:
         print(__name__, " -> Opening SPI-port: ", PortNr, " CS:  ", CS)
         self.SPI_Bus = spidev.SpiDev()
         self.SPI_Bus.open(PortNr, CS)
         self.SPI_Bus.max_speed_hz = C.SPIMCP23S17CLOCK
         print(__name__, " -> Initializing SPI Relay Driver on SPI-Port: ", PortNr, " CS: ", CS)
         self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17IODIRA, 0xF0])
         self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17IODIRB, 0xFF])
      except:
         print(__name__, " -> unable to open SPI-port: ", PortNr, " CS: ", CS)
      self.SpiLock.release()

   def PowerOn(self):
      #print(__name__, " -> Power Relay On")
      self.SpiData = self.SpiData | C.RELAYPREAMPPOWER
      self.SpiLock.acquire()
      self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17GPIOAREG, self.SpiData])
      self.SpiLock.release()

   def PowerOff(self):
      #print(__name__, " -> Power Relay Off")
      self.SpiData = self.SpiData & ~C.RELAYPREAMPPOWER
      self.SpiLock.acquire()
      self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17GPIOAREG, self.SpiData])
      self.SpiLock.release()

   def SwitchLineOutOn(self):
      #print(__name__, " -> Line Out Relay On")
      self.SpiData = self.SpiData | C.RELAYPREAMPLINEOUT
      self.SpiLock.acquire()
      self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17GPIOAREG, self.SpiData])
      self.SpiLock.release()

   def SwitchLineOutOff(self):
      #print(__name__, " -> Line Out Relay Off")
      self.SpiData = self.SpiData & ~C.RELAYPREAMPLINEOUT
      self.SpiLock.acquire()
      self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17GPIOAREG, self.SpiData])
      self.SpiLock.release()

   def InputSelect(self, Index):
      #print(__name__, " -> Input Select Relay: ", Index)
      self.SpiData = self.SpiData & C.RELAYPREAMPNOCHANNEL
      if Index == 1 or Index == 2:
         self.SpiData = self.SpiData | C.RELAYPREAMPINTERNALCHANNEL
      if Index == 3:
         self.SpiData = self.SpiData | C.RELAYPREAMPDVDCHANNEL
      if Index == 4:
         self.SpiData = self.SpiData | C.RELAYPREAMPAUXCHANNEL
      self.SpiLock.acquire()
      self.SPI_Bus.xfer([C.SPIMCP23S17ADRESS, C.SPIMCP23S17GPIOAREG, self.SpiData])
      self.SpiLock.release()
