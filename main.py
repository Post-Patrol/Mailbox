import network
import time

# SSID and key used to connect to network. 
SSID = 'SPU-Wireless'
KEY= 'SPU-Wireless'

# Connection timeout in seconds
timeout = 10;

# Dictionary used to convert network status to strings.
# There might be a better way to do that. 
STATUS_KEY = {
    network.STAT_IDLE: 'IDLE',
    network.STAT_CONNECTING: 'CONNECTING',
    network.STAT_WRONG_PASSWORD: 'WRONG PASSWORD',
    network.STAT_NO_AP_FOUND: 'NO ACCESS POINT FOUND',
    network.STAT_CONNECT_FAIL: 'CONNECT FAILED',
    network.STAT_GOT_IP: 'SUCCESS'
};

# Attempt to connect to the specified SSID via KEY
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, KEY)
    
# Wait for the station status to resolve
while sta.status() == network.STAT_CONNECTING:
    timeout -= 1
    print ('waiting for connection [' + str(timeout)+']')
    time.sleep(1)

# If station status is not success, raise an error
if sta.status() != network.STAT_GOT_IP:
    raise RuntimeError('STA: ' + STATUS_KEY[sta.status()])

# Print STA status as string
# Print IP configuration to prove connection. 
print('STA : ' + STATUS_KEY[sta.status()])
print('CONF: ' + str(sta.ifconfig()))


