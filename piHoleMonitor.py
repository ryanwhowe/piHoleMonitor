import json
import time
import requests
import subprocess
import board
import busio
from datetime import datetime
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


def buildLcd():
    """buildLcd create the lcd object for interacting with the screen & buttons
    """
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
    lcd.color = [0, 0, 100]
    return lcd


def getIp():
    ip_command = "hostname -I | cut -d\' \' -f1 | tr -d \'\\n\'"
    return subprocess.check_output(ip_command, shell=True).decode("utf-8")


def getHost():
    host_command = "hostname | tr -d \'\\n\'"
    return subprocess.check_output(host_command, shell=True).decode("utf-8")


def getDaysUptime():
    uptime_command = "uptime -s | tr -d \'\\n'"
    start_up_date = subprocess.check_output(
        uptime_command, shell=True).decode("utf-8")
    up_date = datetime.strptime(start_up_date, '%Y-%m-%d %H:%M:%S')
    delta = datetime.now() - up_date
    return delta.days


def getPiHoleApi():
    api_url = "http://localhost/admin/api.php"
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        PERCENT_BLOCKED = float(data['ads_percentage_today']) / float(100)
        LAST_UPDATE = int(data['gravity_last_updated']['absolute'])
        update_date = datetime.fromtimestamp(LAST_UPDATE)
        updated = datetime.now() - update_date
    except KeyError:
        return False
    return {"blocked": PERCENT_BLOCKED, "last_update": updated.days}


def nextPosition(content, position):
    next = position + 1
    if (next > (len(content) - 1)):
        return 0
    return next


def previousPosition(content, position):
    next = position - 1
    if(next < 0):
        return (len(content) - 1)
    return next


def centeredRow(text):
    return formatRow('{:^16s}'.format(text))


def formatRow(text):
    return '%.16s' % text.ljust(16)


def buildContent(data):
    result = []
    hostname = '!' + data['host'] + '!'
    divider = "".join(['-']*len(hostname))
    result.insert(0, centeredRow(hostname))
    result.insert(1, centeredRow(divider))
    result.insert(2, formatRow("up: {0} days".format(data['days_uptime'])))
    result.insert(3, formatRow(
        "updated: {0} days".format(data['last_update'])))
    result.insert(4, formatRow("Blocked: {0:.1%}".format(data['blocked'])))
    result.insert(5, centeredRow(divider))
    return result


def updateDisplay(display, position):
    lcd.message = display[position] + "\n" + \
        display[nextPosition(display, position)]


def updateData():
    piHole = getPiHoleApi()
    return {'host': getHost(), 'days_uptime': getDaysUptime(),
            "blocked": piHole['blocked'], "last_update": piHole['last_update']}


data = updateData()
content = buildContent(data)

lcd = buildLcd()
position = 0
updateDisplay(content, position)

while True:
    if lcd.down_button:
        content = buildContent(updateData())
        position = nextPosition(content, position)
        updateDisplay(content, position)
    if lcd.up_button:
        content = buildContent(updateData())
        position = previousPosition(content, position)
        updateDisplay(content, position)
    time.sleep(0.01)
