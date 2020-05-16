import spidev
import constants as c
from threading import Lock


class MCP23S17:
    SPI_bus = None
    SpiLock = Lock()
    SpiData = 0x00

    def __init__(self, port_nr, cs):
        self.SpiLock.acquire()
        try:
            print(__name__, " -> Opening SPI-port: ", port_nr, " cs:  ", cs)
            self.SPI_Bus = spidev.SpiDev()
            self.SPI_Bus.open(port_nr, cs)
            self.SPI_Bus.max_speed_hz = c.SPIMCP23S17CLOCK
            print(__name__, " -> Initializing SPI Relay Driver on SPI-Port: ", port_nr, " cs: ", cs)
            self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17IODIRA, 0xE0])
            self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17IODIRB, 0xFF])
        except:
            print(__name__, " -> unable to open SPI-port: ", port_nr, " cs: ", cs)
        self.SpiLock.release()

    def power_on(self):
        # print(__name__, " -> Power Relay On")
        self.SpiData = self.SpiData | c.RELAYPREAMPPOWER
        self.SpiLock.acquire()
        self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17GPIOAREG, self.SpiData])
        self.SpiLock.release()

    def power_off(self):
        # print(__name__, " -> Power Relay Off")
        self.SpiData = self.SpiData & ~c.RELAYPREAMPPOWER
        self.SpiLock.acquire()
        self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17GPIOAREG, self.SpiData])
        self.SpiLock.release()

    def switch_line_out_on(self):
        # print(__name__, " -> Line Out Relay On")
        self.SpiData = self.SpiData | c.RELAYPREAMPLINEOUT
        self.SpiLock.acquire()
        self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17GPIOAREG, self.SpiData])
        self.SpiLock.release()

    def switch_line_out_off(self):
        # print(__name__, " -> Line Out Relay Off")
        self.SpiData = self.SpiData & ~c.RELAYPREAMPLINEOUT
        self.SpiLock.acquire()
        self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17GPIOAREG, self.SpiData])
        self.SpiLock.release()

    def input_select(self, index):
        # print(__name__, " -> Input Select Relay: ", index)
        self.SpiData = self.SpiData & c.RELAYPREAMPNOCHANNEL
        if index == 1 or index == 2:
            self.SpiData = self.SpiData | c.RELAYPREAMPINTERNALCHANNEL
        if index == 3:
            self.SpiData = self.SpiData | c.RELAYPREAMPDVDCHANNEL
        if index == 4:
            self.SpiData = self.SpiData | c.RELAYPREAMPAUXCHANNEL
        self.SpiLock.acquire()
        self.SPI_Bus.xfer([c.SPIMCP23S17ADRESS, c.SPIMCP23S17GPIOAREG, self.SpiData])
        self.SpiLock.release()
