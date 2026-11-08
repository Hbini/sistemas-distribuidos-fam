# Sistemas Distribuídos: exemplos de programação (FAM)

Repositório de apoio à disciplina **Sistemas Distribuídos** da FAM (Faculdade de Americana), cursos de Sistemas de Informação e Ciência da Computação.
Prof.º Esp. Hernane Bini.

Cada aula tem exemplos comentados em **Python** e **Java**, um README explicando o conceito e como executar, e uma lista de **exercícios**. Os exemplos Python e Java usam os mesmos protocolos, então um cliente Java conversa com um servidor Python e vice-versa (é a heterogeneidade dos sistemas distribuídos na prática).

## Índice

| Aula | Tema | Destaques |
|---|---|---|
| [02](aula02-centralizado-distribuido-paralelo) | Sistemas centralizados, distribuídos, paralelos e de alto desempenho | sequencial x paralelo, speedup, mestre/trabalhadores pela rede |
| [03](aula03-transparencia-flexibilidade-confiabilidade) | Transparência, flexibilidade e confiabilidade | serviço de nomes, réplicas, failover |
| [04](aula04-desempenho-escalabilidade) | Desempenho e escalabilidade | servidor sequencial x threads x pool, vazão, latência, Lei de Amdahl |
| [05](aula05-elementos-microsservicos) | Elementos básicos de um SD e microsserviços | loja em microsserviços Python + Java, API Gateway, Docker Compose |
| [06](aula06-mecanismos-comunicacao) | Mecanismos de comunicação: elementos básicos | serialização, marshalling, endianness, UDP x TCP, síncrona x assíncrona |
| [07](aula07-paradigmas-comunicacao) | Paradigmas de comunicação | memória compartilhada, pub/sub, fila de mensagens |
| [08](aula08-sockets-cliente-servidor) | Cliente/servidor e sockets | eco TCP, servidor multicliente, chat em grupo |
| [09](aula09-servico-de-grupo-p2p) | Serviço de grupo, eventos e peer-to-peer | IP multicast, ordem total com sequenciador, rede P2P |
| [11](aula11-middleware) | Middleware | RPC, JSON-RPC Python/Java, Java RMI, RabbitMQ |
| [12](aula12-algoritmos-distribuidos) | Algoritmos distribuídos | Lamport, relógio vetorial, Valentão, anel, Ricart e Agrawala, Berkeley |
| [13](aula13-so-distribuidos-parte1) | Sistemas operacionais distribuídos (parte 1) | heartbeat, consistência forte x eventual, CAP, checkpoint |
| [14](aula14-so-distribuidos-parte2) | Sistemas operacionais distribuídos (parte 2) | sistema de arquivos distribuído com cache, balanceamento de carga, HMAC |

A Aula 01 é a apresentação da disciplina e a Aula 10 é revisão.

## Pré-requisitos

* **Python 3.10 ou superior**. Os exemplos usam apenas a biblioteca padrão (exceto a pasta `aula11-middleware/rabbitmq`, que usa `pika`).
* **JDK 17 ou superior** (recomendado **JDK 21**, necessário para as *virtual threads* da Aula 04).
* **Docker Desktop** (opcional), para as Aulas 05 e 11.
* Git, para clonar o repositório.

## Como usar

```bash
git clone https://github.com/Hbini/sistemas-distribuidos-fam.git
cd sistemas-distribuidos-fam/aula08-sockets-cliente-servidor
python python/eco_servidor.py
```

Os programas Java **não precisam ser compilados antes**: a partir do Java 11, `java Arquivo.java` compila e executa em um passo.

```bash
java java/EcoCliente.java
```

### Dicas para o Windows

* Use `python` (ou `py`) em vez de `python3`.
* Se os acentos aparecerem trocados no terminal, execute `chcp 65001` antes, ou use o Windows Terminal.
* Na primeira execução de um servidor, o Firewall do Windows pode pedir permissão: clique em **Permitir**.

### Executando entre computadores do laboratório

Quase todos os exemplos usam `127.0.0.1` (a própria máquina). Para testar entre máquinas, rode o servidor em um computador, descubra o IP dele (`ipconfig`) e passe esse IP ao cliente. Os README de cada aula indicam como.

## Mapa de portas usadas

| Porta | Uso |
|---|---|
| 5000 | serviço de nomes (Aula 03) |
| 5007 | grupo multicast 224.1.1.1 (Aula 09) |
| 6001 a 6012 | trabalhadores (Aula 02) |
| 7001 a 7101 | réplicas da calculadora (Aula 03) |
| 8000 a 8004 | servidores de carga (Aula 04) e microsserviços (Aula 05) |
| 8101 a 8202 | nós P2P (Aula 09) |
| 9100 a 9700 | exemplos de comunicação e sockets (Aulas 06 a 08) |
| 9800, 9801, 1099 | RPC, JSON-RPC e RMI (Aula 11) |
| 9900, 9950 | heartbeat e sistema de arquivos (Aulas 13 e 14) |

## Observações

* Os exemplos são **didáticos**: priorizam clareza sobre robustez. Não use em produção sem tratamento de erros, autenticação e criptografia.
* Valores como cotações e cardápios são fictícios.
* Material elaborado com o auxílio da ferramenta de IA Claude (Anthropic), com revisão e testes do professor.

Licença: MIT.
