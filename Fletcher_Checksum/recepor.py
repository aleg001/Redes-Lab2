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
    calculated_checksum = format(sum1, '08b') + format(sum2, '08b')
    if calculated_checksum == received_checksum:
        # a. No se detectaron errores
        print("Mensaje recibido sin errores:", message)
    else:
        # b. Se detectaron errores
        if sum1 == int(received_checksum[:8], 2):
            # c. Se detectaron y corrigieron errores
            error_bit = int(received_checksum[8:], 2)
            if error_bit < len(message):
                corrected_message = message[:error_bit] + str(1 - int(message[error_bit], 2)) + message[error_bit + 1:]
                print("Se corrigieron errores. Bit corregido en posición:", error_bit)
                print("Trama corregida:", corrected_message)
            else:
                print("La trama se descarta por detectar errores.")
        else:
            print("La trama se descarta por detectar errores.")

print("Tramas correctas")
tramas_correctas = ["1101011000001010001010010000101010001010", "110101100000010010000011101001011", "1000001010001010010000011000110011", "110101010010000011000101000"]
for trama in tramas_correctas:
    fletcher_checksum_receptor(trama)
print("Tramas modificadas")
tramas_errores = ["1101011010001010001010010000101010011010", "110101100000010010000011101001010", "1000011010001010010000011000110011", "110101010110000011000101000"]
for trama in tramas_errores:
    fletcher_checksum_receptor(trama)