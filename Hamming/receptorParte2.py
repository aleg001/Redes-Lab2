import socket
import difflib


def binary_to_ascii(binary_str):
    ascii_str = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i : i + 8]
        ascii_str += chr(int(byte, 2))
    return ascii_str


def hamming_decoder(received_word):
    # Tabla de paridad (indices empiezan desde 1)
    parity_positions = [1, 2, 4]
    error = 0

    for position in parity_positions:
        xor_result = 0
        for j in range(1, len(received_word) + 1):
            if j & position:
                xor_result = xor_result ^ int(received_word[j - 1])
        error += xor_result * position

    # Si error es cero, no hay errores. Si es distinto de cero, indica la posición del error.
    if error:
        received_word = list(received_word)
        received_word[error - 1] = "1" if received_word[error - 1] == "0" else "0"
        received_word = "".join(received_word)

    # Descartar bits de paridad: posiciones 1, 2 y 4

    correct_word = received_word[2:3] + received_word[4:7]

    return correct_word


def calcular_similitud(palabra1, palabra2):
    similarity = difflib.SequenceMatcher(None, palabra1, palabra2).ratio()
    similarity_percentage = similarity * 100
    return similarity_percentage


# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al puerto 1050
server_socket.bind(("localhost", 1050))

# Escuchar conexiones entrantes con una cola de tamaño 1
server_socket.listen(1)
print("Esperando conexiones en el puerto 1050...")

# Aceptar una conexión
client_socket, address = server_socket.accept()
print("Conexión desde:", address)

archivo = "palabras.txt"
lineas = []

with open(archivo, "r") as f:
    for linea in f:
        lineas.append(linea.strip())

message_index = 0
similitudes = []


while True:
    data = client_socket.recv(1024)
    if data.decode() == "":
        with open("similitudes.txt", "w") as file:
            for similitud in similitudes:
                file.write(str(similitud) + "\n")
        break
    decoded_data = b"".join(
        [
            hamming_decoder(chunk)
            for chunk in [data[i : i + 7] for i in range(0, len(data), 7)]
        ]
    )
    word = binary_to_ascii(decoded_data)
    if word:
        linea_word = lineas[message_index % len(lineas)]
        similitud = round(calcular_similitud(word, linea_word))
        similitudes.append(similitud)
        print(message_index, word, linea_word, similitud)
        message_index += 1
    else:
        similitudes.append(0)
        message_index += 1
