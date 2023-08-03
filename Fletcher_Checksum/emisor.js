function fletcherChecksumEmisor(message) {
  // Paso 2: Calcular la información adicional (Fletcher checksum)
  let sum1 = 0
  let sum2 = 0
  for (let i = 0; i < message.length; i++) {
    sum1 = (sum1 + parseInt(message[i], 2)) % 255
    sum2 = (sum2 + sum1) % 255
  }

  // Paso 3: Devolver el mensaje en binario concatenado con la información adicional
  const checksum =
    sum1.toString(2).padStart(8, '0') + sum2.toString(2).padStart(8, '0')
  return message + checksum
}

// Ejemplo de uso:
const tramas = [
  '110101100000101000101001',
  '11010110000001001',
  '100000101000101001',
  '11010101001',
]

for (var i = 0; i < tramas.length; i++) {
  const tramaConChecksum = fletcherChecksumEmisor(tramas[i])
  console.log('Trama enviada:', tramaConChecksum)
}
