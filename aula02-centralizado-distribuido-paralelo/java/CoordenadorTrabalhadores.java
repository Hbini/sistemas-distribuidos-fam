import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Aula 02: cálculo de primos DISTRIBUÍDO entre processos que conversam pela rede.
 *
 * Protocolo de texto bem simples (uma linha por mensagem):
 *   coordenador -> trabalhador : "inicio;fim"
 *   trabalhador -> coordenador : "primos;tempoSegundos;hostname"
 *
 * Como executar (3 terminais):
 *   java CoordenadorTrabalhadores.java trabalhador 6001
 *   java CoordenadorTrabalhadores.java trabalhador 6002
 *   java CoordenadorTrabalhadores.java coordenador 127.0.0.1:6001 127.0.0.1:6002
 *
 * O trabalhador Java é compatível com o coordenador Python e vice-versa?
 * NÃO, de propósito: o Python usa JSON e o Java usa texto "a;b". Isso mostra
 * por que sistemas heterogêneos precisam combinar um PROTOCOLO (exercício 3).
 */
public class CoordenadorTrabalhadores {

    static boolean ehPrimo(int n) {
        if (n < 2) return false;
        if (n % 2 == 0) return n == 2;
        for (int d = 3; (long) d * d <= n; d += 2) if (n % d == 0) return false;
        return true;
    }

    static void trabalhador(int porta) throws Exception {
        try (ServerSocket servidor = new ServerSocket(porta)) {
            System.out.println("[trabalhador:" + porta + "] aguardando tarefas...");
            while (true) {
                try (Socket s = servidor.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
                     PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8)) {
                    String[] partes = in.readLine().split(";");
                    int inicio = Integer.parseInt(partes[0]);
                    int fim = Integer.parseInt(partes[1]);
                    System.out.printf("[trabalhador:%d] recebi [%d, %d)%n", porta, inicio, fim);
                    long t0 = System.nanoTime();
                    int total = 0;
                    for (int n = inicio; n < fim; n++) if (ehPrimo(n)) total++;
                    double tempo = (System.nanoTime() - t0) / 1e9;
                    out.println(total + ";" + tempo + ";" + InetAddress.getLocalHost().getHostName());
                }
            }
        }
    }

    static void coordenador(String[] enderecos) throws Exception {
        int limite = 2_000_000;
        int n = enderecos.length;
        int tamanho = limite / n;
        String[] respostas = new String[n];
        Thread[] threads = new Thread[n];
        long t0 = System.nanoTime();

        for (int i = 0; i < n; i++) {
            final int idx = i;
            threads[i] = new Thread(() -> {
                String[] hp = enderecos[idx].split(":");
                int inicio = idx * tamanho;
                int fim = (idx == n - 1) ? limite : (idx + 1) * tamanho;
                try (Socket s = new Socket(hp[0], Integer.parseInt(hp[1]));
                     PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
                     BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
                    out.println(inicio + ";" + fim);
                    respostas[idx] = in.readLine();
                } catch (Exception e) {
                    respostas[idx] = "0;0;FALHOU(" + e.getMessage() + ")";
                }
            });
            threads[i].start();
        }
        for (Thread t : threads) t.join();

        int total = 0;
        for (int i = 0; i < n; i++) {
            String[] r = respostas[i].split(";");
            total += Integer.parseInt(r[0]);
            System.out.printf("  %-20s host=%-15s primos=%s%n", enderecos[i], r[2], r[0]);
        }
        System.out.printf("%nTotal de primos: %d (tempo total %.2f s)%n", total, (System.nanoTime() - t0) / 1e9);
    }

    public static void main(String[] args) throws Exception {
        if (args.length >= 2 && args[0].equals("trabalhador")) {
            trabalhador(Integer.parseInt(args[1]));
        } else if (args.length >= 2 && args[0].equals("coordenador")) {
            String[] enderecos = new String[args.length - 1];
            System.arraycopy(args, 1, enderecos, 0, enderecos.length);
            coordenador(enderecos);
        } else {
            System.out.println("Uso: trabalhador <porta> | coordenador host:porta [host:porta ...]");
        }
    }
}
