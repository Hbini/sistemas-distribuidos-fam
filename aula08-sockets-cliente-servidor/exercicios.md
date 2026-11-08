# Exercícios: Aula 08

**Exercício 1 (mensagens privadas).** Acrescente ao chat (Python ou Java) o comando `/msg <apelido> <texto>`, que envia a mensagem só para o destinatário. Se o apelido não existir, responda `*** usuário não encontrado`.

**Exercício 2 (enquadramento).** Crie um par cliente/servidor que troque mensagens com **prefixo de tamanho**: 4 bytes (inteiro big-endian) com o tamanho, seguidos da mensagem em UTF-8. Escreva a função `receber_mensagem(sock)` que lê exatamente o número de bytes indicado, mesmo que eles cheguem em vários `recv`. Teste enviando uma mensagem de 100.000 caracteres.

**Exercício 3 (servidor de arquivos).** Implemente um servidor que atende o comando `BAIXAR <nome>` e envia o conteúdo do arquivo pedido (de uma pasta `compartilhada/`), usando o enquadramento do exercício 2. Proteja o servidor contra o ataque de **path traversal** (`BAIXAR ../../senhas.txt`).

**Exercício 4 (conceitual).** Explique a diferença entre o socket devolvido por `accept()` e o socket que fez `listen()`. Por que um servidor TCP precisa de dois tipos de socket? O que muda em um servidor UDP?
