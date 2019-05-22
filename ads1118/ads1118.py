import spidev

class ADS1118(object):
    MUX_AIN0_AIN1    = 0b000
    MUX_AIN0_AIN3    = 0b001
    MUX_AIN1_AIN3    = 0b010
    MUX_AIN2_AIN3    = 0b011
    MUX_AIN0         = 0b100
    MUX_AIN1         = 0b101
    MUX_AIN2         = 0b110
    MUX_AIN3         = 0b111
    PGA_6_114V       = 0b000
    PGA_4_096V       = 0b001
    PGA_2_048V       = 0b010
    PGA_1_024V       = 0b011
    PGA_0_512V       = 0b100
    PGA_0_256V_A     = 0b101  # equivalent to PGA_0_256V
    PGA_0_256V_B     = 0b110  # equivalent to PGA_0_256V
    PGA_0_256V       = 0b111
    MODE_CONTINUOUS  = 0
    MODE_SINGLESHOT  = 1
    DATARATE_8_SPS   = 0b000
    DATARATE_16_SPS  = 0b001
    DATARATE_32_SPS  = 0b010
    DATARATE_64_SPS  = 0b011
    DATARATE_128_SPS = 0b100
    DATARATE_250_SPS = 0b101
    DATARATE_475_SPS = 0b110
    DATARATE_860_SPS = 0b111
    TS_MODE_ADC      = 0
    TS_MODE_TEMP     = 1
    
    ADC_CONVERSION_FACTORS = {
        PGA_6_114V:   6.114/32767,
        PGA_4_096V:   4.096/32767,
        PGA_2_048V:   2.048/32767,
        PGA_1_024V:   1.024/32767,
        PGA_0_512V:   0.512/32767,
        PGA_0_256V_A: 0.256/32767,
        PGA_0_256V_B: 0.256/32767,
        PGA_0_256V:   0.256/32767
    }
    
    def __init__(self, spiBus, spiDev, spiHz = 5000, spiMode = 0b01):
        self.spi = spidev.SpiDev()
        self.spi.open(spiBus, spiDev)
        self.spi.max_speed_hz = spiHz
        self.spi.mode = spiMode
    
    def _encodeCommand(self, startSingleShot=True, mux=MUX_AIN0_AIN1, pga=PGA_2_048V, mode=MODE_SINGLESHOT,
                datarate=DATARATE_128_SPS, tsMode=TS_MODE_ADC, pullupEnable=True, nop=False):
        outputS = format(startSingleShot, "01b")
        outputS += format(mux,  "03b")
        outputS += format(pga,  "03b")
        outputS += format(mode, "01b")
        outputS += format(datarate, "03b")
        outputS += format(tsMode, "01b")
        outputS += format(pullupEnable, "01b")
        if nop:
            outputS += "00"
        else:
            outputS += "01"
        outputS += "1"
        return [int(outputS[:8], 2), int(outputS[8:], 2), 0, 0]
    
    def readData(self, startSingleShot=True, mux=MUX_AIN0_AIN1, pga=PGA_2_048V, mode=MODE_SINGLESHOT,
                datarate=DATARATE_128_SPS, tsMode=TS_MODE_ADC, pullupEnable=True, nop=False):
        command = self._encodeCommand(startSingleShot, mux, pga, mode, datarate, tsMode, pullupEnable, nop)
        outArr = self.spi.xfer(command+[0,0,0,0])
        out = outArr[4]*256+outArr[5]
        if out>=0x8000:
                out -= 0x10000
        if tsMode == self.TS_MODE_ADC:
            return out*self.ADC_CONVERSION_FACTORS[pga]
        else:
            return (out >> 2) * 0.03125
