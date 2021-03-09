# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import utime
from network import WLAN, STA_IF, AP_IF, STAT_IDLE, STAT_CONNECTING, STAT_WRONG_PASSWORD, STAT_NO_AP_FOUND, STAT_CONNECT_FAIL, STAT_GOT_IP
import webrepl

from my_secret import MY_LAN 
gc.collect()

wlan = network.WLAN(network.STA_IF)

def waitForConnection():
	retry = 60
	while wlan.status() == STAT_CONNECTING and retry > 0 :
		utime.sleep(0.1)
		retry =retry - 1
	print('wlan reply:',wlan.status(),' at time:',utime.ticks_ms(),' retry:',retry)
	return wlan.isconnected()

def do_connect():
    import network
    if not wlan.active() : wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        nets = wlan.scan()
        nets.sort(key=lambda ap: ap[3], reverse=True)
        for net in nets:
            print('Network found:',net[0].decode('UTF-8'),' bssid:',ubinascii.hexlify( net[1]),' sec:',decode_sec(net[4]),' rssi:',net[3])
            for sid,pwd in MY_LAN:    
               if net[0].decode('UTF-8') == sid:
#                 wlan.ifconfig(('192.168.1.12', '255.255.255.0', '192.168.1.1', '8.8.8.8')) #hardkoded data will save some time
                  wlan.connect(net[0].decode('UTF-8'), pwd)
                  if waitForConnection():
                     print('WLAN connection succeeded!')
                     break
    print('network config:', wlan.ifconfig())

do_connect()
webrepl.start(password=WEBREPL_PWD)
