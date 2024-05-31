import machine
import network
import utime
import umail
from machine import SoftI2C
import struct
from enum import Enum

class MailboxState(Enum):
    CHECKED = 0
    UNCHECKED = 1

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

class wifi:
    def __init__(self):

        # SSID and key used to connect to network.
        self.SSID = 'SPU-Wireless'
        self.KEY = 'SPU-Wireless'

        # Connection timeout in seconds
        self.TIMEOUT = 10


    def connect(self):
        # Attempt to connect to the specified SSID via KEY
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.sta.connect(self.SSID, self.KEY)
        self.TIMEOUT = 10

        # Wait for the station status to resolve
        while self.sta.status() == network.STAT_CONNECTING:
            self.TIMEOUT -= 1
            print ('waiting for connection [' + str(self.TIMEOUT)+']')
            utime.sleep(1)

        # If station status is not success, raise an error
        if self.sta.status() != network.STAT_GOT_IP:
            raise RuntimeError('STA: ' + STATUS_KEY[self.sta.status()])

        # Print STA status as string
        # Print IP configuration to prove connection.
        print('STA : ' + STATUS_KEY[self.sta.status()])
        print('CONF: ' + str(self.sta.ifconfig()))


class emailer:
    def __init__(self):

        # connect to wifi
        self.wifi = wifi()
        self.wifi.connect()

        # Email server configuration
        self.sender_email = 'postpatrol.mailbox@gmail.com' # Replace with the email address of the sender
        self.sender_name = 'The Mailbox' # Replace with the name of the sender
        self.sender_app_password = 'nvcw mfkq fbhc jmhg' # Replace with the app password of the sender's email account
        self.recipient_email = 'critesg@spu.edu' # Replace with the email address of the recipient
        self.email_subject ='You\'ve Got Mail!' # Subject of the email

    def send_email(self):
        # Connect to the Gmail's SSL port
        self.smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
        # Login to the email account using the app password
        self.smtp.login(self.sender_email, self.sender_app_password)
        # Send the email
        self.smtp.to(self.recipient_email)
        self.smtp.write('From: ' + self.sender_name + ' <' + self.sender_email + '>\n')
        self.smtp.write('To: ' + self.recipient_email + '\n')
        self.smtp.write('Subject: ' + self.email_subject + '\n')
        self.smtp.write("You've got mail!\n")
        self.smtp.send()
        self.smtp.quit()

class scale:

    def __init__(self):
        self.addr = 0x26
        self.zeroer = 0.0
        self.i2c = SoftI2C(scl=machine.Pin(1), sda=machine.Pin(0), freq=100000)
        self.i2c.start()
        self.callibrate()

    def __deinit__(self):
        self.i2c.stop()

    def get_weight(self):
        raw_weight = struct.unpack('f', self.i2c.readfrom_mem(self.addr, 0x10, 4))[0]
        return raw_weight + self.zeroer

    def callibrate(self):
        utime.sleep(2)
        current_weight = struct.unpack('f', self.i2c.readfrom_mem(self.addr, 0x10, 4))[0]
        self.zeroer = -current_weight



class mailbox:
    def __iniit__(self):
        self.emailer = emailer()
        self.scale = scale()
        self.pir_sensor = machine.Pin(15, machine.Pin.IN)
        self.state = MailboxState.CHECKED
        self.reset_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.reset_button.irq(trigger=machine.Pin.IRQ_RISING, handler=isr)
        self.led = machine.PIN(14, machine.PIN.OUT)

    def change_state(self):
        if self.state == MailboxState.UNCHECKED:
            self.state = MailboxState.CHECKED
        else:
            self.state = MailboxState.UNCHECKED

#
def reset(mailbox.reset_button):
    global mailbox
    mailbox.weight_sensor.callibrate()

button.irq(trigger=machine.Pin.IRQ_RISING, handler=isr)

# Create mailbox object
mailbox = mailbox()

# Main loop
while True:
        
    if mailbox.pir_sensor.value() == 1:
        print("Motion detected!")
        if mailbox.state == MailboxState.CHECKED:
            utime.sleep(2)
            weight = mailbox.weight_sensor.get_weight()
            if weight > 2.0:
                mailbox.emailer.send_email()
                mailbox.change_state()
            else:
                mailbox.scale.callibrate()
        elif mailbox.state == MailboxState.UNCHECKED:
            weight = mailbox.weight_sensor.get_weight()
            if weight < 2.0:
                mailbox.change_state()

        utime.sleep(3)







