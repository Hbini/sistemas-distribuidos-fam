import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 * Aula 14: HMAC-SHA256 em Java. Com a MESMA chave do integridade_hmac.py,
 * gera exatamente o MESMO HMAC: Python e Java conseguem verificar as
 * mensagens um do outro.
 * Executar: java MensagemHmac.java
 */
public class MensagemHmac {
    static final byte[] CHAVE = "segredo-da-turma-SD".getBytes(StandardCharsets.UTF_8);

    static String assinar(String msg) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(CHAVE, "HmacSHA256"));
        return HexFormat.of().formatHex(mac.doFinal(msg.getBytes(StandardCharsets.UTF_8)));
    }

    static boolean verificar(String msg, String assinatura) throws Exception {
        // MessageDigest.isEqual compara em tempo constante
        return MessageDigest.isEqual(assinar(msg).getBytes(), assinatura.getBytes());
    }

    public static void main(String[] args) throws Exception {
        String original = "transferir 100 para Ana";
        String tag = assinar(original);
        System.out.println("HMAC: " + tag + "  (compare com a saída do Python)");
        System.out.println("Original: " + (verificar(original, tag) ? "VÁLIDA" : "ADULTERADA"));
        System.out.println("Alterada: " + (verificar("transferir 9000 para Mallory", tag) ? "VÁLIDA" : "ADULTERADA"));
    }
}
