"""
Aula 13: Recuperação de falhas: CHECKPOINT e ROLLBACK.

Um processamento longo (somar 1.000 lotes) salva o progresso em disco a cada
100 lotes. Se o processo "cair", ao reiniciar ele volta ao último checkpoint
em vez de começar do zero.

Executar duas vezes:
    python checkpoint_rollback.py          (vai "cair" no lote 437)
    python checkpoint_rollback.py          (retoma do lote 400)
    python checkpoint_rollback.py limpar   (apaga o checkpoint)
"""

import json
import os
import sys

ARQUIVO = "checkpoint.json"
FALHA_NO_LOTE = 437

if sys.argv[1:] == ["limpar"]:
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
    print("Checkpoint apagado.")
    sys.exit()

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, encoding="utf-8") as f:
        estado = json.load(f)
    print(f"Checkpoint encontrado: retomando do lote {estado['lote']} (ROLLBACK para o último estado salvo)")
    ja_falhou = True
else:
    estado = {"lote": 0, "soma": 0}
    print("Sem checkpoint: começando do zero")
    ja_falhou = False

for lote in range(estado["lote"], 1000):
    if lote == FALHA_NO_LOTE and not ja_falhou:
        print(f"*** FALHA no lote {lote}! Trabalho desde o último checkpoint foi perdido. ***")
        sys.exit(1)
    estado["soma"] += lote
    estado["lote"] = lote + 1
    if estado["lote"] % 100 == 0:
        # grava em arquivo temporário e renomeia: a troca é atômica, evita checkpoint corrompido
        with open(ARQUIVO + ".tmp", "w", encoding="utf-8") as f:
            json.dump(estado, f)
        os.replace(ARQUIVO + ".tmp", ARQUIVO)
        print(f"  checkpoint salvo no lote {estado['lote']}")

print(f"Concluído! Soma = {estado['soma']} (correto: {sum(range(1000))})")
os.remove(ARQUIVO)
