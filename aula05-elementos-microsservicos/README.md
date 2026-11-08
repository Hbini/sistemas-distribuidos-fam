# Aula 05: Elementos básicos de um SD e Microsserviços

## A loja de lanches em microsserviços

```
                       +-------------+
   cliente_loja  --->  | API Gateway |  porta 8000 (única porta exposta)
                       +------+------+
              +---------------+----------------+
              v               v                v
       +-----------+    +-----------+    +-----------+
       | catálogo  |    |  estoque  |    |  pedidos  | ---> chama catálogo e estoque
       |  Python   |    |   JAVA    |    |  Python   |
       |  :8001    |    |   :8002   |    |   :8003   |
       +-----------+    +-----------+    +-----------+
        dados próprios   dados próprios   dados próprios
```

## Elementos básicos de um SD presentes no exemplo

| Elemento | Onde aparece |
|---|---|
| Nós / processos | cada serviço é um processo independente (um container no Docker) |
| Rede e protocolo de comunicação | HTTP sobre TCP |
| Formato de dados (representação) | JSON |
| Nomeação / descoberta | URLs por variável de ambiente; no Docker, nomes de serviço viram nomes DNS |
| Interface (contrato) | as rotas REST de cada serviço |
| Tratamento de falhas | o gateway e o serviço de pedidos devolvem 503 quando um serviço está fora do ar |
| Concorrência | `ThreadingHTTPServer` (Python) e pool de threads + `synchronized` (Java) |

## Características de microsserviços demonstradas

* **Responsabilidade única:** cada serviço cuida de um assunto.
* **Dados próprios:** nenhum serviço lê os dados do outro diretamente.
* **Heterogeneidade:** estoque em Java, o restante em Python.
* **Implantação independente:** cada serviço tem seu container.
* **API Gateway:** ponto único de entrada.
* **Health check:** rota `/saude` em todos os serviços.

## Como executar

### Opção A: sem Docker (4 terminais)

```bash
python python/servico_catalogo.py
java   java/ServicoEstoque.java
python python/servico_pedidos.py
python python/api_gateway.py
# depois, em outro terminal:
python python/cliente_loja.py        # ou: java java/ClienteLoja.java
```

### Opção B: com Docker

```bash
docker compose up --build
python python/cliente_loja.py
docker compose down
```

### Experimento de falha

Com tudo rodando, pare o serviço de estoque (Ctrl+C ou `docker compose stop estoque`) e faça um pedido. O catálogo continua funcionando, mas pedidos retornam 503: a falha fica **isolada**, ao contrário de um monólito, em que um erro derruba tudo.

Exercícios: [exercicios.md](exercicios.md)
