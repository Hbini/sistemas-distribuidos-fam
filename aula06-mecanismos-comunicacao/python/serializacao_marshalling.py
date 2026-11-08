"""
Aula 06: Serialização e marshalling.

Para mandar um dado pela rede ele precisa virar uma SEQUÊNCIA DE BYTES.
Aqui o mesmo pedido é convertido de três formas diferentes:

  1. JSON   : texto legível, independente de linguagem (usado em APIs REST)
  2. struct : binário compacto, com layout fixo combinado entre as partes
  3. pickle : formato próprio do Python (NÃO interoperável e inseguro com
              dados de origem desconhecida: nunca use pickle.loads em dados da rede!)

Também mostra o problema de ENDIANNESS (ordem dos bytes): o número 1000 em
big-endian (ordem de rede) e em little-endian (ordem dos processadores x86/ARM).

Executar: python serializacao_marshalling.py
"""

import json
import pickle
import struct

pedido = {"id": 42, "produto": "Coxinha", "quantidade": 3, "preco": 7.5}

print("Objeto original:", pedido, "\n")

# 1) JSON
dados_json = json.dumps(pedido).encode("utf-8")
print(f"[JSON]   {len(dados_json):3d} bytes: {dados_json}")
print("         de volta:", json.loads(dados_json))

# 2) struct (marshalling binário)
# Formato combinado: '!' = ordem de rede (big-endian)
#   I  = inteiro sem sinal de 4 bytes (id)
#   20s = texto de 20 bytes (produto, completado com zeros)
#   H  = inteiro curto de 2 bytes (quantidade)
#   d  = número real de 8 bytes (preço)
FORMATO = "!I20sHd"
dados_bin = struct.pack(FORMATO, pedido["id"], pedido["produto"].encode("utf-8"),
                        pedido["quantidade"], pedido["preco"])
print(f"\n[struct] {len(dados_bin):3d} bytes: {dados_bin.hex(' ')}")
i, prod, qtd, preco = struct.unpack(FORMATO, dados_bin)
print("         de volta:", {"id": i, "produto": prod.rstrip(b"\0").decode(), "quantidade": qtd, "preco": preco})

# 3) pickle
dados_pickle = pickle.dumps(pedido)
print(f"\n[pickle] {len(dados_pickle):3d} bytes (só outro programa Python entende)")

# Endianness
print("\n=== Endianness: o número 1000 em 4 bytes ===")
print("big-endian    (rede, '!'):", struct.pack("!I", 1000).hex(" "))
print("little-endian (x86, '<') :", struct.pack("<I", 1000).hex(" "))
errado = struct.unpack("<I", struct.pack("!I", 1000))[0]
print(f"Se o emissor manda big-endian e o receptor lê como little-endian: 1000 vira {errado:,}!")
print("Por isso protocolos binários fixam a ordem de rede (big-endian).")
