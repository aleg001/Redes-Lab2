const fs = require('fs');
const net = require('net');

function fletcherChecksumEmisor(message) {
  let sum1 = 0
  let sum2 = 0
  for (let i = 0; i < message.length; i++) {
    sum1 = (sum1 + parseInt(message[i], 2)) % 255
    sum2 = (sum2 + sum1) % 255
  }

  const checksum =
    sum1.toString(2).padStart(8, '0') + sum2.toString(2).padStart(8, '0')
  return message + checksum
}

function process(message) {
  const binario = message.split('').map(char => {
    let bits = char.charCodeAt(0).toString(2).padStart(8, '0');
    return Array.from(bits).map(bit => {
      if (Math.random() < 0.01) {
        return bit === '0' ? '1' : '0';
      }
      return bit;
    }).join('');
  }).join('');
  return binario
}

const client = new net.Socket();

client.on('data', data => {
  console.log('Recibido:', data.toString());
});

client.on('close', () => {
  console.log('Conexión cerrada');
});

client.on('error', err => {
  console.error('Ocurrió un error:', err);
});

client.connect(1050, '127.0.0.1', () => {
  console.log('Conectado al puerto 1050');


  fs.readFile('palabras.txt', 'utf8', (err, data) => {
    if (err) {
      console.error('Ocurrió un error al leer el archivo:', err);
      return;
    }
    
    const lineas = data.split('\n');
    
    function sendTrama(index) {
      if (index >= lineas.length * 440) {
        // Se completaron las repeticiones necesarias.
        // Puedes hacer algo aquí, como cerrar la conexión si es necesario.
        client.end()
        return;
      }
  
      const palabraIndex = index % lineas.length;
      const trama = process(lineas[palabraIndex]);
      const fletcher_trama = fletcherChecksumEmisor(trama);
      const buffer = Buffer.from(fletcher_trama, 'binary');
      client.write(buffer);
      console.log('Trama enviada: ' + fletcher_trama);
  
      setTimeout(() => {
        sendTrama(index + 1); // Envío de la siguiente trama después de 1 segundo.
      }, 25);
    }
  
    sendTrama(0); // Iniciar el envío de tramas.
  });
});
