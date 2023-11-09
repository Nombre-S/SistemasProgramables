################################################################################
# Nombre del Archivo: main.py
# Autor:             [Soto García Alejandro]
# Correo:            [l20212433@tectijuana.edu.mx]
# Fecha:             [2023-11-08]
# Institución:       Tecnológico Nacional de México (TECNM) - Campus ITT
# Curso:             Sistemas Programables 
#
# Objetivo:
# Este programa está diseñado para poder obtener información del módulo GPS, en una pantalla oled.
#
# Historial de Revisiones:
# [2023-11-08]        [Soto García Alejandro] - Creado
#
# Enlace a GitHub Repository ó GIST:
# [https://github.com/tectijuana/sp5-iot-ai-los-pistaches-anacletos]
#
# Enlace a Wokwi :
# [https://wokwi.com/projects/380890445535843329]
#
# Licencia:
# Este programa es software libre y puede ser redistribuido y/o modificado bajo los términos de la Licencia Pública General GNU
# como está publicado por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN GARANTÍA ALGUNA; incluso sin la garantía implícita de
# COMERCIALIZACIÓN o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la Licencia Pública General GNU para obtener más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
#
################################################################################

# Importación de modulos necesarios.
from machine import Pin, UART, I2C
from ssd1306 import SSD1306_I2C
import utime, time

# Conexión a Oled I2C.
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Conexión a GPS mediante UART.
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Impresión de detalles de conexión al módulo GPS.
print(gps_module)

# Variable para guardar strings NMEA.
buff = bytearray(255)

TIMEOUT = False

# Guardado del estado del satelite.
FIX_STATUS = False

# Variables para guardar los parametros de las coordenadas.
latitude = ""
longitude = ""
satellites = ""
gpsTime = ""


# Función para obtener las coordenadas del GPS.
def getPositionData(gps_module):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, gpsTime
    
    # Ciclo while para obtener los datos
    # O se detiene despues de una espera de 8 segundos
    timeout = time.time() + 8  
    while True:
        gps_module.readline()
        buff = str(gps_module.readline())
        parts = buff.split(',')
        
        #if no gps displayed remove "and len(parts) == 15" from below if condition
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                                
                latitude = convertToDigree(parts[2])
                
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDigree(parts[4])
                
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                gpsTime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
# Función para convertir la longitud y latitud.
def convertToDigree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)
    
    
while True:
    
    getPositionData(gps_module)

    # Si los datos son encontrados, se imprimen en el Oled display.
    if(FIX_STATUS == True):
        print("fix......")
        oled.fill(0)
        oled.text("Lat: "+latitude, 0, 0)
        oled.text("Lng: "+longitude, 0, 10)
        oled.text("No of Sat: "+satellites, 0, 20)
        oled.text("Time: "+gpsTime, 0, 30)
        oled.show()
        print(latitude)
        print(longitude)
        print(satellites)
        print(gpsTime)
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("Request Timeout: No GPS data is found.")
        #--------------------------------------------------
        #updated on 5-May-2022
        oled.fill(0)
        oled.text("No GPS data is found", 0, 0)
        oled.show()
        #--------------------------------------------------
        TIMEOUT = False
        
