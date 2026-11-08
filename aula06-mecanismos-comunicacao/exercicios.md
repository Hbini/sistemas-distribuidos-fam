# Exercícios: Aula 06

**Exercício 1 (marshalling).** Acrescente ao formato binário um campo `mesa` (inteiro de 1 byte) logo depois da quantidade. Atualize o servidor Python, o cliente Python e o cliente Java. Qual o novo tamanho da mensagem? O que acontece se você atualizar só o servidor?

**Exercício 2 (confiabilidade sobre UDP).** Modifique o cliente UDP para **retransmitir** cada mensagem até 5 vezes caso a resposta não chegue em 300 ms. Coloque um número de sequência em cada mensagem e faça o servidor ignorar duplicatas (mas reenviar a resposta). Quantas das 50 mensagens chegam agora? Qual protocolo real faz isso por você?

**Exercício 3 (comparação de formatos).** Meça o tamanho em bytes de uma lista com 1.000 pedidos serializada em JSON e em `struct`. Calcule a economia percentual do formato binário. Cite duas vantagens do JSON que justificam seu uso em APIs mesmo sendo maior.

**Exercício 4 (classificação).** Classifique como síncrona/assíncrona e transiente/persistente: (a) ligação telefônica; (b) mensagem de WhatsApp; (c) chamada a uma API REST; (d) e-mail; (e) transmissão ao vivo de vídeo via UDP.
