import java.io.DataInputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Aula 06: cliente JAVA para o servidor binário escrito em PYTHON.
 *
 * O Python empacotou com struct.pack("!I20sHd", ...). Para desempacotar em Java:
 *   I   (4 bytes)  -> readInt()
 *   20s (20 bytes) -> readFully(byte[20])
 *   H   (2 bytes)  -> readUnsignedShort()
 *   d   (8 bytes)  -> readDouble()
 * DataInputStream sempre lê em BIG-ENDIAN, que é exatamente a "ordem de rede" ('!').
 *
 * Executar: python ../python/servidor_binario.py   e depois   java ClienteBinario.java
 */
public class ClienteBinario {
    public static void main(String[] args) throws Exception {
        try (Socket s = new Socket("127.0.0.1", 9100);
             DataInputStream in = new DataInputStream(s.getInputStream())) {
            int id = in.readInt();
            byte[] nome = new byte[20];
            in.readFully(nome);
            int quantidade = in.readUnsignedShort();
            double preco = in.readDouble();
            String produto = new String(nome, StandardCharsets.UTF_8).replace("\0", "");
            System.out.printf("id=%d produto=%s quantidade=%d preço=%.2f%n", id, produto, quantidade, preco);
        }
    }
}
