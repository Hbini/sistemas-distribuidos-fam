import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Aula 04: gerador de carga que mede vazão e latência.
 * Uso: java GeradorCarga.java 127.0.0.1 8000 20 5
 *      (20 clientes simultâneos, 5 pedidos cada)
 */
public class GeradorCarga {
    public static void main(String[] args) throws Exception {
        String host = args.length > 0 ? args[0] : "127.0.0.1";
        int porta = args.length > 1 ? Integer.parseInt(args[1]) : 8000;
        int clientes = args.length > 2 ? Integer.parseInt(args[2]) : 20;
        int pedidos = args.length > 3 ? Integer.parseInt(args[3]) : 5;

        List<Double> latencias = Collections.synchronizedList(new ArrayList<>());
        List<Thread> threads = new ArrayList<>();
        long inicio = System.nanoTime();
        for (int c = 0; c < clientes; c++) {
            Thread t = new Thread(() -> {
                for (int i = 0; i < pedidos; i++) {
                    long t0 = System.nanoTime();
                    try (Socket s = new Socket(host, porta);
                         PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
                         BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
                        out.println("pedido");
                        in.readLine();
                        latencias.add((System.nanoTime() - t0) / 1e6);
                    } catch (Exception e) {
                        System.out.println("erro: " + e.getMessage());
                    }
                }
            });
            threads.add(t);
            t.start();
        }
        for (Thread t : threads) t.join();
        double duracao = (System.nanoTime() - inicio) / 1e9;

        List<Double> ordenadas = new ArrayList<>(latencias);
        Collections.sort(ordenadas);
        double media = ordenadas.stream().mapToDouble(Double::doubleValue).average().orElse(0);
        double p95 = ordenadas.get((int) (ordenadas.size() * 0.95) - 1);
        System.out.printf("Pedidos: %d em %.2f s%n", ordenadas.size(), duracao);
        System.out.printf("Vazão  : %.1f pedidos/s%n", ordenadas.size() / duracao);
        System.out.printf("Latência média: %.0f ms | p95: %.0f ms%n", media, p95);
    }
}
