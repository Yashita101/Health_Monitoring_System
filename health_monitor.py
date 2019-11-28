import datetime
import time
import os
from pulsesensor import Pulsesensor
from temperaturesensor import TemperatureSensor
import RPi.GPIO as GPIO
import serial
import sys
import http.client
import urllib.request

pulse_key = "OV4UT8JRYDWS5B53"
temp_key="VMPNSROP5WNJPZJ3"     
pause=10                        #assumption

SERIAL_PORT="/dev/ttyS0"

ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)
p = Pulsesensor()
p.startAsyncBPM()
t = TemperatureSensor()

def health_monitor():
    delay = 2

    while True:
        try:
            temp_level = t.ReadChannel()
            temp_volts = t.ConvertVolts(temp_level,2)
            temp       = t.ConvertTemp(temp_level,2)
            bpm = p.BPM
            time.sleep(1)
            start=time.time()
            
            params1=urllib.parse.urlencode({'field1':temp,'key':temp_key})
            headers1={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
            conn1=http.client.HTTPConnection("api.thingspeak.com:80")
            
            params2=urllib.parse.urlencode({'field1':bpm,'key':pulse_key})
            headers2={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
            conn2=http.client.HTTPConnection("api.thingspeak.com:80")        

            conn1.request("POST","/update",params1,headers1)
            response1=conn1.getresponse()
            conn2.request("POST","/update",params2,headers2)
            response2=conn2.getresponse()
            
            phone=["+91**********", "+91**********"]
            
            if bpm > 0 and temp > 0:
                    
                    print ("--------------------------------------------"  )
                    print("BPM: %d" % bpm)
                    print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
                    time.sleep(5)
                    if (time.time()-start)>pause:
                        if temp < 36:
                            if bpm < 60:
                                #print("Low BP and Low Temp")
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPOTHERMIA and LOW BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_temp and low_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''

                            elif bpm > 100:
                                #print("High BP and Low Temperature")
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPOTHERMIA and HIGH BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_temp and HIGH_BP")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            else:
                                #print("Low Temperature")
                            
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPOTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.
                                
                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_temp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                        elif temp > 38:
                            if bpm < 60:
                                #print("high temp and low bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPERTHERMIA and LOW BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_temp and low_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            elif bpm>100:
                                #print("high temp and high bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPERTHERMIA and HIGH BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_temp and high_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            else:
                                #print("high temp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HYPERTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_temp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                    
                        elif bpm < 60:
                            if temp < 36:
                                #print("low_temp and low_bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has LOW BP and HYPOTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_bp and low_temp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            elif temp > 38:
                                #print("high temp and low bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has LOW BP and HYPERTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_temp and low_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            else:
                                #print("low_bp")
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has LOW BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                        elif bpm >100 :
                            
                            if temp <36:
                                #print("low temp and high bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HIGH BP and HYPOTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...low_temp and high_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            elif temp >38:
                                #print("high temp and high bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HIGH BP and HYPERTHERMIA."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_temp and high_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                            else:
                                #print("high_bp")
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY has HIGH BP."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.

                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...high_bp")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                                
                        
            else:
                    time.sleep(10)
                    if (time.time()-start)>10 and bpm == 0 or temp < 0:
                        print ("--------------------------------------------"  )
                        print("No Heartbeat found %d" % bpm)
                        print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
                                
                                for i in range(len(phone)):
                                    ser.write(str.encode('AT+CMGF=1\r'))
                                    time.sleep(2)
                                    ser.write(str.encode('AT+CMGS="%s"\r'%phone[i]))
                                    time.sleep(2)
                                    msg="Patient NRSY is in a critical condition.EMERGENCY."
                                    time.sleep(2)
                                    ser.write(str.encode(msg+chr(26)))
                                    time.sleep(2)
                                    print("message sent to",phone[i])
                                #time.sleep(1800)                                       #doctor and family members are reminded after half an hour about patient's health condition getting worse.
                    time.sleep(3)
                                '''
                                    #FOR CALLING:
                                    ser.write(str.encode("ATD+91**********;\r"))
                                    print("Dialling...emergency")
                                    time.sleep(2)
                                    ser.write(str.encode("ATH\r"))
                                    print("Hanging up")
                                    time.sleep(5)
                                '''
                        
            #print(response1.status,response1.reason,response2.status,response2.reason)
    
            data1=response1.read()
            data2=response2.read()
            
        except InterruptedError as ie:
            p.stopAsyncBPM()
            conn1.close()
            conn2.close()
        except ConnectionError as ce:
            print("Connection failed",ce)
        except KeyboardInterrupt as ki:
            print(ki)
            exit()
        
        time.sleep(delay)
    
if __name__=="__main__":
    while True:
health_monitor()
