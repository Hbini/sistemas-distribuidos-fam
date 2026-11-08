# Aula 14: Sistemas Operacionais Distribuídos (Parte 2): arquivos distribuídos, escalonamento e segurança

| Conceito | Python | Java |
|---|---|---|
| Sistema de arquivos distribuído com cache e versão | `servidor_arquivos_distribuido.py` + `cliente_arquivos_cache.py` | |
| Escalonamento e balanceamento de carga | `balanceador_carga.py` | `BalanceadorCarga.java` |
| Segurança: integridade e autenticidade (HMAC) | `integridade_hmac.py` | `MensagemHmac.java` (gera o mesmo HMAC) |

## Sistema de arquivos distribuído

```
  cliente A (cache)                     servidor de arquivos
  "cat leiame.txt"  -- versão? ---->    leiame.txt v1
                    <--- v1 ---------
  versão igual ao cache: usa a cópia local (não baixa de novo)
```

Transparências envolvidas: acesso (comandos iguais aos locais), localização (o cliente não sabe em que disco está) e, com o cache, desempenho.

## Como executar

```bash
python python/servidor_arquivos_distribuido.py
python python/cliente_arquivos_cache.py        # abra dois clientes
#   SAD> ls
#   SAD> cat leiame.txt     (1ª vez baixa, 2ª vez usa cache)
#   SAD> echo notas.txt prova dia 20

python python/balanceador_carga.py
java   java/BalanceadorCarga.java

python python/integridade_hmac.py
java   java/MensagemHmac.java
```

Exercícios: [exercicios.md](exercicios.md)
