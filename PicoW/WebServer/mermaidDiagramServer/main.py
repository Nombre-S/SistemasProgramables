import network
import socket
from time import sleep
import machine

ssid = 'INFINITUM1DE5_2.4G'
password = 'QxfcHsk6D2'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Conected on {ip}")
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
    # state = "Apagado"
    while True:
        client = connection.accept()[0]
        try:
            request = client.recv(1024)
            request = str(request)
            print(request)
            html = web_page()
            client.send(html)
        finally:
            client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    connection.close()
