import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * Aula 08: cliente de eco em Java (funciona com eco_servidor.py e EcoServidor.java).
 * Executar: java EcoCliente.java [ip]
 */
public class EcoCliente {
    public static void main(String[] args) throws Exception {
        String host = args.length > 0 ? args[0] : "127.0.0.1";
        try (Socket s = new Socket(host, 9500); Scanner teclado = new Scanner(System.in)) {
            OutputStream out = s.getOutputStream();
            InputStream in = s.getInputStream();
            byte[] buffer = new byte[1024];
            System.out.println("Conectado. Digite mensagens (linha vazia para sair).");
            while (teclado.hasNextLine()) {
                String msg = teclado.nextLine();
                if (msg.isEmpty()) break;
                out.write(msg.getBytes(StandardCharsets.UTF_8));
                int n = in.read(buffer);
                System.out.println(new String(buffer, 0, n, StandardCharsets.UTF_8));
            }
        }
    }
}
