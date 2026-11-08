"""
Aula 14: Segurança em sistemas distribuídos: INTEGRIDADE e AUTENTICIDADE com HMAC.

Problema: uma mensagem "transferir 100 para Ana" atravessa a rede. Um atacante
no meio do caminho pode alterá-la para "transferir 9000 para Mallory".

HMAC = hash da mensagem misturado com uma CHAVE SECRETA que só emissor e
receptor conhecem. Quem não tem a chave não consegue gerar um HMAC válido.

Executar: python integridade_hmac.py
Compatível com java/MensagemHmac.java (mesma chave e mesmo algoritmo).
"""
import hashlib
import hmac

CHAVE = b"segredo-da-turma-SD"     # em produção: guardada em cofre, nunca no código!


def assinar(mensagem: str) -> str:
    return hmac.new(CHAVE, mensagem.encode("utf-8"), hashlib.sha256).hexdigest()


def verificar(mensagem: str, assinatura: str) -> bool:
    # compare_digest evita ataque de tempo (timing attack)
    return hmac.compare_digest(assinar(mensagem), assinatura)


original = "transferir 100 para Ana"
tag = assinar(original)
print(f"Mensagem : {original}\nHMAC     : {tag}\n")

print("Receptor verifica a mensagem original:", "VÁLIDA" if verificar(original, tag) else "ADULTERADA")
alterada = "transferir 9000 para Mallory"
print(f"Atacante altera para '{alterada}' e mantém o HMAC:",
      "VÁLIDA" if verificar(alterada, tag) else "ADULTERADA (rejeitada)")

sha_simples = hashlib.sha256(alterada.encode()).hexdigest()
print("Atacante recalcula um SHA-256 simples (sem chave):",
      "VÁLIDA" if verificar(alterada, sha_simples) else "ADULTERADA (rejeitada)")
print("\nObservação: HMAC garante integridade e autenticidade, NÃO sigilo.")
print("Para sigilo, a comunicação precisa ser criptografada (TLS).")
