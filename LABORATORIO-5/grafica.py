import serial
import matplotlib.pyplot as plt
import numpy as np

# Set up the serial connection 
ser = serial.Serial( 
    port='COM5',  # Replace with the appropriate serial port 
    baudrate=115200, 
    bytesize=serial.EIGHTBITS, 
    timeout=1  # Set a timeout value, in seconds 
) 


def calculate_checksum(data_):
    checksum = 0
   
    for byte in data_[3:11]:
        checksum += byte
    return checksum & 0xFF 

# Inicializa listas para los datos
rpm_data = []
time_data = []

# Inicializa la gráfica
plt.ion()  # Modo interactivo
fig, ax = plt.subplots()
line, = ax.plot([], [])

tmax = 0  # Variable de tiempo
contador=0
try:
    while True:
        if ser.in_waiting > 0:
            # Lee los datos en bruto (bytes)
            data = ser.read(ser.in_waiting)
            # Convierte los bytes a formato hexadecimal
            hex_data = data.hex()
            print(f'Datos recibidos en HEX: {hex_data}')
            
            suma=calculate_checksum(data)
           
            if suma==data[-2]:
                # Calculo de RPM (modifica esto según sea necesario)
                rpm = (data[3] << 24) 
                rpm |= (data[4] << 16) 
                rpm |= (data[5] << 8) 
                rpm |= (data[6])


                tmax = (data[7] << 24) 
                tmax |= (data[8] << 16) 
                tmax |= (data[9] << 8) 
                tmax |= (data[10])

            
                # Agrega los datos a las listas
                rpm_data.append(rpm)
                time_data.append(tmax)

                # Actualiza los datos de la gráfica
                line.set_xdata(time_data)
                line.set_ydata(rpm_data)

                # Ajusta los límites de los ejes
                ax.relim()
                ax.autoscale_view()

                # Redibuja la gráfica
                plt.draw()
                plt.pause(0.01)  # Pausa corta para actualización
                if tmax == 0 and data[-2]==0:
                     contador = 1
                if tmax == 0 and contador == 1:
                    print("Reiniciando la gráfica...")
                    # Reinicia los datos
                    rpm_data.clear()
                    time_data.clear()
                    
                    # Restablece los límites de los ejes
                    ax.relim()
                    ax.autoscale_view()
                    
                    # Reinicia la gráfica
                    line.set_xdata([])
                    line.set_ydata([])
                    plt.draw()
                    plt.pause(0.01)
                    contador = 0
                    
except KeyboardInterrupt:
    # Cierra la conexión al terminar
    ser.close()
    print("Conexión cerrada.")
