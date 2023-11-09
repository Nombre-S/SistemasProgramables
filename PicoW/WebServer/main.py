import network
import socket
from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import images
import framebuf, sys

ssid = 'TecNM-ITT-Docentes'
password = 'tecnm2022!'
led = Pin("LED", Pin.OUT)
pix_res_x = 128
pix_res_y = 64
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c)

def connect():
    max_wait = 0
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while max_wait <= 10:
        oled.text('Conectando...', 0, 0)
        #displayImg(oled,images.wifiConnectionH, 32, 32, 20, 20)
        #displayImg(oled,images.wifiConnectionF, 32, 32, 20, 20)
        sleep(2)
        max_wait += 1
    if max_wait == 10:
        oled.fill_rect(0, 0, 104, 8, 0)
        oled.text("No Conexion", 0, 0)
        displayImg(oled, images.wifiFailed, 32, 32, 20, 20)
    ip = wlan.ifconfig()[0]
    oled.fill_rect(0, 0, 104, 8, 0)
    oled.text("Conectado en:", 0, 0)
    oled.text(str(ip), 0, 10)
    oled.show()
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection

def close_socket(connection):
    connection.close()

def web_page():
    page = open("index.html", "r")
    html = page.read()
    page.close()
    return str(html)

def serve(connection):
    led.off()
    while True:
        client = connection.accept()[0]
        try:
            request = client.recv(1024)
            request = str(request)
            print(request)
            try:
                request = request.split()[1]
            except IndexError:
                pass
            if request == '/lighton?':
                led.on()
            elif request == '/lightoff?':
                led.off()
            html = web_page()
            client.send(html)
        finally:
            client.close()

def displayImg(oled, IMGname, resX, resY, posX, posY):
    IMG = framebuf.FrameBuffer(IMGname, resX, resY, framebuf.MONO_HLSB)
    oled.blit(IMG, posX, posY)
    oled.show()

def main():
    try:
        ip = connect()
        connection = open_socket(ip)
        serve(connection)
    except KeyboardInterrupt:
        connection.close()

if __name__ == '__main__':
    main()
