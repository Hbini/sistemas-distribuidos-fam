import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Aula 08: servidor de chat em Java, mesmo protocolo do chat_servidor.py
 * (clientes Python e Java podem conversar entre si). Porta 9600.
 * Executar: java ChatServidor.java
 */
public class ChatServidor {
    static final Map<PrintWriter, String> CLIENTES = new ConcurrentHashMap<>();

    static void difundir(String texto, PrintWriter exceto) {
        for (PrintWriter out : CLIENTES.keySet()) {
            if (out != exceto) out.println(texto);
        }
    }

    static void atender(Socket s) {
        PrintWriter out = null;
        String apelido = "anônimo";
        try (s; BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
            out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
            String primeira = in.readLine();
            if (primeira != null && !primeira.isBlank()) apelido = primeira.trim();
            CLIENTES.put(out, apelido);
            difundir("*** " + apelido + " entrou no chat ***", null);
            String linha;
            while ((linha = in.readLine()) != null) {
                if (linha.equals("/quem")) out.println("*** online: " + String.join(", ", CLIENTES.values()));
                else if (!linha.isBlank()) difundir("[" + apelido + "] " + linha, out);
            }
        } catch (Exception ignorada) {
        } finally {
            if (out != null) CLIENTES.remove(out);
            difundir("*** " + apelido + " saiu ***", null);
        }
    }

    public static void main(String[] args) throws Exception {
        try (ServerSocket srv = new ServerSocket(9600)) {
            System.out.println("Chat Java na porta 9600");
            while (true) {
                Socket s = srv.accept();
                new Thread(() -> atender(s)).start();
            }
        }
    }
}
