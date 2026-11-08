# Exercícios: Aula 09

**Exercício 1 (P2P em rede real).** Hoje o nó P2P anuncia sempre o endereço `127.0.0.1`. Acrescente o parâmetro `--host` para que o nó anuncie o IP real da máquina e monte, com os colegas, uma rede P2P de 5 computadores do laboratório. Desenhe a topologia usada e registre quantas mensagens de BUSCA cada nó recebeu para encontrar um arquivo.

**Exercício 2 (download P2P).** Após o `ACHEI`, o nó que fez a busca deve baixar o arquivo **diretamente** do peer que o possui (comando `BAIXAR <arquivo>`), sem passar pelos intermediários. Por que isso é importante para a escalabilidade do P2P?

**Exercício 3 (sequenciador e falhas).** No exemplo de ordem total, o sequenciador é um ponto único de falha. Descreva (não precisa implementar) duas soluções para isso e relacione com a eleição de líder que será estudada na Aula 12.

**Exercício 4 (custo da inundação).** Em uma rede P2P em que cada nó tem 4 vizinhos, quantas mensagens de BUSCA, no máximo, uma consulta com TTL = 1, 2, 3 e 4 pode gerar (desconsidere repetições)? O que isso diz sobre a escalabilidade da inundação? Pesquise como as DHTs (Chord, Kademlia) resolvem o problema.
