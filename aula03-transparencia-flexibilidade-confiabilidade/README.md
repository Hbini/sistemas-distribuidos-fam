# Aula 03: Propriedades críticas: Transparência, Flexibilidade e Confiabilidade

## Arquitetura do exemplo

```
                 1. REGISTRAR calculadora           +------------------+
   +-----------+ ---------------------------------> |                  |
   | réplica A |                                    | serviço de nomes |
   +-----------+          +-----------+             |   (porta 5000)   |
   | réplica B | -------> | réplica C |  <--------  +------------------+
   +-----------+          +-----------+     ^
          ^                     ^           | 2. RESOLVER calculadora
          |   3. SOMA 2 3       |           |
          +---------------------+------ cliente_transparente
```

| Propriedade | Onde aparece no código |
|---|---|
| Transparência de **localização** | o cliente usa o nome lógico `calculadora`, nunca um IP fixo |
| Transparência de **replicação** | existem várias réplicas, mas o cliente só vê "o serviço" |
| Transparência de **falha** | se uma réplica cai, `calcular()` tenta a próxima sem avisar o usuário |
| Transparência de **acesso** | réplicas Python e Java atendem o mesmo cliente, com o mesmo protocolo |
| **Flexibilidade / abertura** | nova operação = nova linha no dicionário `OPERACOES`; qualquer linguagem que fale o protocolo entra no sistema |
| **Confiabilidade** | redundância (réplicas) + failover no cliente |

## Como executar

Abra um terminal para cada linha (o serviço de nomes é o mesmo para Python e Java):

```bash
python python/servico_nomes.py
python python/servidor_replica.py 7001
python python/servidor_replica.py 7002
java   java/ServidorReplica.java 7101          # réplica Java no mesmo sistema
python python/cliente_transparente.py           # ou: java java/ClienteTransparente.java
```

Agora feche uma réplica com **Ctrl+C** e observe o cliente continuar funcionando. Feche todas e veja a "falha total".

## Limitação proposital

Quando uma réplica cai, ela continua na lista do serviço de nomes. O cliente perde tempo tentando-a toda vez. Corrigir isso é o Exercício 2.

Exercícios: [exercicios.md](exercicios.md)
