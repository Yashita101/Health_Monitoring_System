import spidev

class TemperatureSensor:
    def __init__(self, temp_channel = 0):
        self.temp_channel  = temp_channel
        
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000
        
    def ReadChannel(self):
        self.adc = self.spi.xfer2([1,(8+self.temp_channel)<<4,0])
        self.data = ((self.adc[1]&3) << 8) + self.adc[2]
        return self.data

     
    def ConvertVolts(self,data,places):
      self.volts = (data * 3.3) / float(1023)
      self.volts = round(self.volts,places)  
      return self.volts
      

    def ConvertTemp(self,data,places):
      self.temp = ((data * 330)/float(1023))-50
      self.temp = round(self.temp,places)
return self.temp
