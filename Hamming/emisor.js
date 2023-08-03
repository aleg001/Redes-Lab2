function hammingEmisor(message) {
  let parityBits = 0
  let n = message.length
  while (2 ** parityBits <= n + parityBits) {
    parityBits++
  }

  let encodedMessage = ''
  let j = 0
  for (let i = 1; i <= n + parityBits; i++) {
    if ((i & (i - 1)) === 0) {
      encodedMessage += 'P'
    } else {
      encodedMessage += message[j]
      j++
    }
  }

  for (let i = 0; i < parityBits; i++) {
    let parityCheck = 0
    for (let j = 1; j <= encodedMessage.length; j++) {
      if (j & (1 << i) && encodedMessage[j - 1] !== 'P') {
        parityCheck ^= parseInt(encodedMessage[j - 1], 2)
      }
    }
    const position = 2 ** i
    encodedMessage =
      encodedMessage.slice(0, position - 1) +
      parityCheck.toString() +
      encodedMessage.slice(position)
  }

  return encodedMessage
}

const tramas = [
  '110101100000101000101001',
  '11010110000001001',
  '100000101000101001',
  '11010101001',
]

for (let i = 0; i < tramas.length; i++) {
  const tramaConHamming = hammingEmisor(tramas[i])
  console.log('Trama enviada:', tramaConHamming)
}
