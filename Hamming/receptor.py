def hamming_receiver(received_message):
    parity_bits = 0
    n = len(received_message)
    while 2**parity_bits < n + parity_bits + 1:
        parity_bits += 1

    error_bit = 0
    for i in range(parity_bits):
        parity_check = 0
        for j in range(1, n + parity_bits + 1):
            if (j & (1 << i)) != 0 and j - 1 < n and received_message[j - 1] == "1":
                parity_check ^= 1
        if parity_check != 0:
            error_bit += 2**i

    corrected_message = list(received_message)
    if error_bit > 0 and error_bit <= n + parity_bits:
        corrected_message[error_bit - 1] = (
            "1" if corrected_message[error_bit - 1] == "0" else "0"
        )
        print(f"Se detectó y corrigió un error en la posición {error_bit}")

    # Eliminar los bits de paridad
    decoded_message = [
        bit for i, bit in enumerate(corrected_message) if not (i + 1) & (i + 1) - 1 == 0
    ]
    decoded_trama = "".join(decoded_message)

    if error_bit > 0:
        print(f"Mensaje decodificado: {decoded_trama}")
    else:
        print(f"No se detectaron errores: {decoded_trama}")


tramas_correctas = [
    "10101011011000010101000101001",
    "1011101001100000001001",
    "00110000001010010101001",
    "001010110101001",
]


tramas_errores = [
    "1101011010001010001010010000101010011010",
    "1000011010001010010000011000110011",
    "110101010110000011000101000",
]

print("Tramas correctas:")
for trama in tramas_correctas:
    hamming_receiver(trama)

print("\nTramas con errores:")
for trama in tramas_errores:
    hamming_receiver(trama)
