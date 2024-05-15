import machine
import network
import utime
import umail

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
        sta.active(True)
        sta.connect(self.SSID, self.KEY)

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
        self.smtp.login(sender_email, sender_app_password)
        # Send the email
        self.smtp.to(self.recipient_email)
        self.smtp.write('From: ' + self.sender_name + ' <' + self.sender_email + '>\n')
        self.smtp.write('To: ' + self.recipient_email + '\n')
        self.smtp.write('Subject: ' + self.email_subject + '\n')
        self.smtp.write("You've got mail!\n")
        self.smtp.send()
        self.smtp.quit()


# Test with button press
# Push Button
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
emailer = emailer()

# interrupt handler
def isr(button):
    global emailer
    emailer.send_email()

button.irq(trigger=machine.Pin.IRQ_RISING, handler=isr)

# Main loop
while True:
    utime.sleep(1)







