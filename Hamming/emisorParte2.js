const fs = require('fs')
const net = require('net')

function hammingEncoder(data) {
  // Suponemos que data es un string binario de 4 bits.
  // Generamos los bits de paridad p1, p2 y p4.
  let p1 = (parseInt(data[0]) ^ parseInt(data[1]) ^ parseInt(data[3])) & 1
  let p2 = (parseInt(data[0]) ^ parseInt(data[2]) ^ parseInt(data[3])) & 1
  let p4 = (parseInt(data[1]) ^ parseInt(data[2]) ^ parseInt(data[3])) & 1

  // Insertamos los bits de paridad en las posiciones correctas.
  return `${p1}${p2}${data[0]}${p4}${data.substring(1)}`
}

function process(message) {
  const binario = message
    .split('')
    .map((char) => {
      let bits = char.charCodeAt(0).toString(2).padStart(8, '0')
      return Array.from(bits)
        .map((bit) => {
          if (Math.random() < 0.01) {
            return bit === '0' ? '1' : '0'
          }
          return bit
        })
        .join('')
    })
    .join('')

  let encodedBinario = ''
  for (let i = 0; i < binario.length; i += 4) {
    encodedBinario += hammingEncoder(binario.substring(i, i + 4))
  }
  return encodedBinario
}

const client = new net.Socket()

client.on('data', (data) => {
  console.log('Recibido:', data.toString())
})

client.on('close', () => {
  console.log('Conexión cerrada')
})

client.on('error', (err) => {
  console.error('Ocurrió un error:', err)
})

client.connect(1050, '127.0.0.1', () => {
  console.log('Conectado al puerto 1050')

  fs.readFile('palabras.txt', 'utf8', (err, data) => {
    if (err) {
      console.error('Ocurrió un error al leer el archivo:', err)
      return
    }

    const lineas = data.split('\n')

    function sendTrama(index) {
      if (index >= lineas.length * 750) {
        client.write(Buffer.from('', 'binary'))
        client.end()
        return
      }

      const palabraIndex = index % lineas.length
      const trama = process(lineas[palabraIndex])
      const buffer = Buffer.from(trama, 'binary')
      client.write(buffer)
      console.log('Trama enviada: ' + trama)

      setTimeout(() => {
        sendTrama(index + 1)
      }, 25)
    }

    sendTrama(0)
  })
})
