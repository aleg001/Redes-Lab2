import socket
import difflib
import matplotlib.pyplot as plt
import seaborn as sns

def binary_to_ascii(binary_str):
    ascii_str = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        ascii_str += chr(int(byte, 2))
    return ascii_str

def fletcher_checksum_receptor(received_message):
    # Paso 2: Obtener el mensaje recibido y el checksum adjunto
    message = received_message[:-16]
    received_checksum = received_message[-16:]

    # Paso 3: Calcular el Fletcher checksum del mensaje recibido
    sum1 = sum2 = 0
    for bit in message:
        sum1 = (sum1 + int(bit, 2)) % 255
        sum2 = (sum2 + sum1) % 255

    # Paso 4: Comparar el checksum calculado con el recibido
    calculated_checksum = format(sum1, "08b") + format(sum2, "08b")
    if calculated_checksum == received_checksum:
        # a. No se detectaron errores
        return binary_to_ascii(message)
    else:
        # b. Se detectaron errores
        if sum1 == int(received_checksum[:8], 2):
            # c. Se detectaron y corrigieron errores
            error_bit = int(received_checksum[8:], 2)
            if error_bit < len(message):
                corrected_message = (
                    message[:error_bit]
                    + str(1 - int(message[error_bit], 2))
                    + message[error_bit + 1 :]
                )
                return binary_to_ascii(corrected_message)
            else:
                return None
        else:
            return None

def calcular_similitud(palabra1, palabra2):
    similarity = difflib.SequenceMatcher(None, palabra1, palabra2).ratio()
    similarity_percentage = similarity * 100
    return similarity_percentage

# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al puerto 8000
server_socket.bind(('localhost', 1050))

# Escuchar conexiones entrantes con una cola de tamaño 1
server_socket.listen(1)
print('Esperando conexiones en el puerto 1050...')

# Aceptar una conexión
client_socket, address = server_socket.accept()
print('Conexión desde:', address)

archivo = "palabras.txt"  # Cambia esto al nombre de tu archivo
lineas = []

# Abre el archivo en modo lectura
with open(archivo, "r") as f:
    for linea in f:
        lineas.append(linea.strip())

message_index = 0
similitudes =[]

# Leer datos en un bucle y cerrar cuando esté hecho
while True:
    data = client_socket.recv(1024)
    if data.decode() == '':
        with open('similitudes.txt', 'w') as file:
            for similitud in similitudes:
                file.write(str(similitud) + '\n')
        break
    word = fletcher_checksum_receptor(data.decode())
    if word is not None and word != '':
        linea_word = lineas[message_index % len(lineas)]
        similitud = round(calcular_similitud(word, linea_word))
        similitudes.append(similitud)
        print(message_index, word,linea_word, similitud)
        message_index += 1
    else:
        similitudes.append(0)
        message_index += 1


