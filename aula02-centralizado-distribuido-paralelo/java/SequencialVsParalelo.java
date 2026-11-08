import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Aula 02: Sistemas centralizados, distribuídos, paralelos e de alto desempenho.
 *
 * Conta os números primos de 0 até 2.000.000 de duas formas:
 *   1) SEQUENCIAL: uma única thread faz todo o trabalho;
 *   2) PARALELA: o intervalo é dividido entre várias threads (um "pool"),
 *      que rodam ao mesmo tempo nos núcleos da MESMA máquina.
 *
 * Como executar (Java 11 ou superior, não precisa compilar antes):
 *     java SequencialVsParalelo.java
 *     java SequencialVsParalelo.java 4     (força 4 threads)
 */
public class SequencialVsParalelo {

    static boolean ehPrimo(int n) {
        if (n < 2) return false;
        if (n % 2 == 0) return n == 2;
        for (int d = 3; (long) d * d <= n; d += 2) {
            if (n % d == 0) return false;
        }
        return true;
    }

    static int contarPrimos(int inicio, int fim) {
        int total = 0;
        for (int n = inicio; n < fim; n++) {
            if (ehPrimo(n)) total++;
        }
        return total;
    }

    public static void main(String[] args) throws Exception {
        int limite = 2_000_000;
        int nucleos = Runtime.getRuntime().availableProcessors();
        int threads = args.length > 0 ? Integer.parseInt(args[0]) : nucleos;
        System.out.println("Núcleos disponíveis: " + nucleos);

        // 1) Sequencial
        long t0 = System.nanoTime();
        int totalSeq = contarPrimos(0, limite);
        double tSeq = (System.nanoTime() - t0) / 1e9;
        System.out.printf("[SEQUENCIAL] %d primos em %.2f s%n", totalSeq, tSeq);

        // 2) Paralelo: cada thread recebe um pedaço do intervalo
        t0 = System.nanoTime();
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        List<Future<Integer>> parciais = new ArrayList<>();
        int tamanho = limite / threads;
        for (int i = 0; i < threads; i++) {
            final int inicio = i * tamanho;
            final int fim = (i == threads - 1) ? limite : (i + 1) * tamanho;
            parciais.add(pool.submit(() -> contarPrimos(inicio, fim)));
        }
        int totalPar = 0;
        for (Future<Integer> f : parciais) totalPar += f.get(); // espera cada resultado
        pool.shutdown();
        double tPar = (System.nanoTime() - t0) / 1e9;
        System.out.printf("[PARALELO ] %d primos em %.2f s com %d threads%n", totalPar, tPar, threads);

        double speedup = tSeq / tPar;
        System.out.printf("%nSpeedup    = %.2fx%n", speedup);
        System.out.printf("Eficiência = %.0f%%%n", 100 * speedup / threads);
        // Observação: em Java, threads de um mesmo processo rodam de verdade em
        // paralelo. Em Python, por causa do GIL, usamos processos (multiprocessing).
    }
}
