"""
Aula 12: Sincronização de relógios FÍSICOS: algoritmo de BERKELEY.

Cada máquina tem um relógio que adianta ou atrasa um pouco (deriva).
Um processo MESTRE:
  1. pergunta a hora a todos (inclusive a si mesmo);
  2. compensa o tempo de ida e volta (metade do RTT);
  3. ignora valores muito discrepantes (relógio "maluco");
  4. calcula a MÉDIA e envia a cada um o AJUSTE (+ ou -), não a hora absoluta.

Executar: python sincronizacao_berkeley.py
"""

import random

relogios = {"mestre": 3 * 3600 + 0 * 60, "maq-A": 3 * 3600 + 25 * 60,
            "maq-B": 2 * 3600 + 50 * 60, "maq-C": 9 * 3600 + 0 * 60}   # maq-C está muito errada
TOLERANCIA = 60 * 60                                                        # 1 hora


def hhmm(seg: float) -> str:
    seg = int(round(seg))
    return f"{seg // 3600:02d}:{seg % 3600 // 60:02d}:{seg % 60:02d}"


print("Horas antes da sincronização:")
for nome, t in relogios.items():
    print(f"  {nome:<7} {hhmm(t)}")

leituras = {}
for nome, t in relogios.items():
    rtt = 0 if nome == "mestre" else random.uniform(0.2, 0.6)
    leituras[nome] = t + rtt / 2                 # compensa metade do tempo de ida e volta

referencia = leituras["mestre"]
validas = {n: t for n, t in leituras.items() if abs(t - referencia) <= TOLERANCIA}
descartadas = set(leituras) - set(validas)
media = sum(validas.values()) / len(validas)
print(f"\nDescartadas por discrepância: {sorted(descartadas) or 'nenhuma'}")
print(f"Média das válidas: {hhmm(media)}\n")

print("Ajustes enviados pelo mestre:")
for nome in relogios:
    ajuste = media - leituras[nome]
    relogios[nome] += ajuste
    print(f"  {nome:<7} {'+' if ajuste >= 0 else '-'}{hhmm(abs(ajuste))}  -> {hhmm(relogios[nome])}")

print("\nObservação: na prática o relógio nunca 'volta para trás' de uma vez;")
print("ele é desacelerado aos poucos até alcançar a hora certa.")
