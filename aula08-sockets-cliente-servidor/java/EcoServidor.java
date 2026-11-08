import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Aula 08: servidor de eco TCP em Java, passo a passo.
 *   new ServerSocket(porta)  = socket() + bind() + listen()
 *   accept()                 = espera um cliente e devolve um Socket exclusivo para ele
 * Compatível com eco_cliente.py (porta 9500).
 * Executar: java EcoServidor.java
 */
public class EcoServidor {
    public static void main(String[] args) throws Exception {
        try (ServerSocket servidor = new ServerSocket(9500)) {
            System.out.println("Servidor de eco Java na porta 9500");
            while (true) {
                try (Socket cliente = servidor.accept()) {   // bloqueia até alguém conectar
                    System.out.println("Cliente conectado: " + cliente.getRemoteSocketAddress());
                    InputStream in = cliente.getInputStream();
                    OutputStream out = cliente.getOutputStream();
                    byte[] buffer = new byte[1024];
                    int lidos;
                    while ((lidos = in.read(buffer)) != -1) {  // -1 = cliente fechou
                        String texto = new String(buffer, 0, lidos, StandardCharsets.UTF_8);
                        System.out.println("  recebido: " + texto);
                        out.write(("ECO: " + texto.toUpperCase()).getBytes(StandardCharsets.UTF_8));
                    }
                }
                System.out.println("Cliente desconectou");
            }
        }
    }
}
