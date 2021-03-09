try:
  import usocket as socket
except:
  import socket
from time import sleep
from machine import Pin
import onewire, ds18x20

import network

import esp
esp.osdebug(None)

import gc
from time import sleep
from machine import Pin
import onewire, ds18x20

import network

import esp

import gc
from machine import Pin
ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
# Complete project details at https://RandomNerdTutorials.com
print('jaaka running temp_s18x')


def read_ds_sensor():
  print('jaaka running temp_s18x:read_ds_sensor')
  roms = ds_sensor.scan()
  print('Found DS devices: ', roms)
  print('Temperatures: ')
  ds_sensor.convert_temp()
  msg = {}
  i=0
  for rom in roms:
    temp = ds_sensor.read_temp(rom)
    if isinstance(temp, float):
      msg[i] = str(round(temp, 2))
      print(temp, end=' ')
      print('Valid temperature')
      print (i)
      i=i+1
  if i > 0:  
      return msg
  else:
      return {0:'0.0',1:'0.0'}
  
  
def web_page():
  print('jaaka running temp_s18x:web_page')
  temp =  {0:'10.0',1:'11.0'}
#  temp = read_ds_sensor()
  html = """<!DOCTYPE HTML><html><head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
    h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; } 
    .ds-labels{ font-size: 1.5rem; vertical-align:middle; padding-bottom: 15px; }
  </style></head><body><h2>ESP with DS18B20</h2>
  <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="ds-labels">Temperature Dusch:</span>
    <span id="temperatureD">""" + str(temp[0]) + """</span>
    <sup class="units">&deg;C</sup>
  </p>
    <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="ds-labels">Temperature Kök  :</span>
    <span id="temperatureK">""" + str(temp[1]) + """</span>
    <sup class="units">&deg;C</sup>
  </p></body></html>"""
  return html

def run_ds18x():
  print('jaaka running temp_s18x:un_ds18x')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
  while True:
   try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
   except OSError as e:
    conn.close()
    print('Connection closed')
