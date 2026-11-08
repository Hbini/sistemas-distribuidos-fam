import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Aula 04: servidor em três modelos para comparar desempenho.
 *   sequencial : um cliente por vez
 *   thread     : uma thread nova por cliente
 *   pool       : número fixo de threads reaproveitadas
 *   virtual    : virtual threads do Java 21 (milhares de threads leves)
 *
 * Cada pedido simula 200 ms de E/S.
 * Uso: java ServidorModelos.java pool 8000 4
 * Carga: python ../python/gerador_carga.py 127.0.0.1 8000 20 5   (ou GeradorCarga.java)
 */
public class ServidorModelos {
    static final int TEMPO_SERVICO_MS = 200;

    static void atender(Socket s) {
        try (s;
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8)) {
            String pedido = in.readLine();
            Thread.sleep(TEMPO_SERVICO_MS); // simula consulta a banco de dados
            out.println("OK " + pedido);
        } catch (Exception ignorada) { }
    }

    public static void main(String[] args) throws Exception {
        String modo = args.length > 0 ? args[0] : "sequencial";
        int porta = args.length > 1 ? Integer.parseInt(args[1]) : 8000;
        int tamanhoPool = args.length > 2 ? Integer.parseInt(args[2]) : 4;

        ExecutorService executor = switch (modo) {
            case "pool" -> Executors.newFixedThreadPool(tamanhoPool);
            case "virtual" -> Executors.newVirtualThreadPerTaskExecutor(); // requer Java 21
            default -> null;
        };
        try (ServerSocket servidor = new ServerSocket(porta, 1024)) {
            System.out.println("Servidor modo '" + modo + "' na porta " + porta);
            while (true) {
                Socket s = servidor.accept();
                switch (modo) {
                    case "sequencial" -> atender(s);
                    case "thread" -> new Thread(() -> atender(s)).start();
                    default -> executor.submit(() -> atender(s));
                }
            }
        }
    }
}
