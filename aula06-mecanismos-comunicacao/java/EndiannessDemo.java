import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.HexFormat;

/**
 * Aula 06: ordem dos bytes (endianness) e marshalling com ByteBuffer.
 * Executar: java EndiannessDemo.java
 */
public class EndiannessDemo {
    public static void main(String[] args) {
        HexFormat hex = HexFormat.ofDelimiter(" ");
        byte[] big = ByteBuffer.allocate(4).order(ByteOrder.BIG_ENDIAN).putInt(1000).array();
        byte[] little = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(1000).array();
        System.out.println("1000 em big-endian    (rede): " + hex.formatHex(big));
        System.out.println("1000 em little-endian (x86) : " + hex.formatHex(little));
        int errado = ByteBuffer.wrap(big).order(ByteOrder.LITTLE_ENDIAN).getInt();
        System.out.println("Lendo big-endian como little-endian: " + errado);
        System.out.println("Ordem nativa desta máquina: " + ByteOrder.nativeOrder());

        // Marshalling do mesmo pedido do exemplo Python ("!I20sHd")
        ByteBuffer buf = ByteBuffer.allocate(34);           // big-endian por padrão
        byte[] nome = new byte[20];
        byte[] txt = "Coxinha".getBytes(java.nio.charset.StandardCharsets.UTF_8);
        System.arraycopy(txt, 0, nome, 0, txt.length);
        buf.putInt(42).put(nome).putShort((short) 3).putDouble(7.5);
        System.out.println("\nPedido empacotado (34 bytes): " + hex.formatHex(buf.array()));
        System.out.println("Compare com a saída de serializacao_marshalling.py: são IDÊNTICOS.");
    }
}
