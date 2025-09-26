/**
 * Função principal que processa a mensagem para criptografar ou descriptografar.
 * @param {boolean} isEncrypt - True para criptografar, false para descriptografar.
 */
function processMessage(isEncrypt) {
    // Obtenção dos elementos do HTML
    const messageInput = document.getElementById('message');
    const keyInput = document.getElementById('key');
    const resultOutput = document.getElementById('result');

    // Leitura dos valores do usuário
    const message = messageInput.value;
    const key = parseInt(keyInput.value, 10);

    // Tratamento de erros e validação
    if (!message) {
        alert("Por favor, insira uma mensagem para processar.");
        return;
    }
    if (isNaN(key) || key < 1 || key > 25) {
        alert("Por favor, insira uma chave válida (número entre 1 e 25).");
        return;
    }

    // Determina o deslocamento: positivo para criptografar, negativo para descriptografar
    const shift = isEncrypt ? key : -key;

    // Chama a função da Cifra de César e exibe o resultado
        resultOutput.textContent = caesarCipher(message, shift);
}

/**
 * Aplica o algoritmo da Cifra de César a uma string.
 * @param {string} text - O texto a ser processado.
 * @param {number} shift - O valor do deslocamento (chave).
 * @returns {string} - O texto resultante.
 */
function caesarCipher(text, shift) {
    let result = '';

    // Itera sobre cada caractere da mensagem
    for (let i = 0; i < text.length; i++) {
        let char = text[i];

        // Verifica se o caractere é uma letra maiúscula (A-Z)
        if (char >= 'A' && char <= 'Z') {
            let charCode = text.charCodeAt(i);
            let shiftedCharCode = ((charCode - 65 + shift) % 26 + 26) % 26 + 65;
            result += String.fromCharCode(shiftedCharCode);
        }
        // Verifica se o caractere é uma letra minúscula (a-z)
        else if (char >= 'a' && char <= 'z') {
            let charCode = text.charCodeAt(i);
            // 97 é o código ASCII de 'a'.
            let shiftedCharCode = ((charCode - 97 + shift) % 26 + 26) % 26 + 97;
            result += String.fromCharCode(shiftedCharCode);
        }
        // Se não for uma letra, mantém o caractere original (espaços, números, pontuação)
        else {
            result += char;
        }
    }

    return result;
}

function usarResultado() {
    // Pega o elemento que mostra o resultado
    const saidaResultado = document.getElementById('result');

    // Pega a caixa de texto da mensagem
    const entradaMensagem = document.getElementById('message');

    // Pega o texto que está no resultado
    const textoResultado = saidaResultado.textContent;

    // Se houver algum texto no resultado, coloca ele na caixa de mensagem
    if (textoResultado) {
        entradaMensagem.value = textoResultado;
    }
}
