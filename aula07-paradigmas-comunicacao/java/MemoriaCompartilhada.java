import java.util.concurrent.atomic.AtomicInteger;

/**
 * Aula 07: memória compartilhada entre THREADS e a condição de corrida.
 * Três versões do mesmo contador incrementado por 4 threads, 1.000.000 de vezes cada:
 *   1) int comum           -> perde incrementos
 *   2) synchronized        -> correto (trava / monitor)
 *   3) AtomicInteger       -> correto (operação atômica de hardware, compare-and-swap)
 *
 * Executar: java MemoriaCompartilhada.java
 */
public class MemoriaCompartilhada {
    static int contador = 0;
    static int contadorSync = 0;
    static final AtomicInteger contadorAtomico = new AtomicInteger();
    static final int N = 1_000_000;

    static synchronized void incrementarSync() { contadorSync++; }

    static void rodar(Runnable r) throws InterruptedException {
        Thread[] ts = new Thread[4];
        for (int i = 0; i < 4; i++) { ts[i] = new Thread(r); ts[i].start(); }
        for (Thread t : ts) t.join();
    }

    public static void main(String[] args) throws Exception {
        rodar(() -> { for (int i = 0; i < N; i++) contador++; });
        System.out.printf("int comum     : %,d (esperado 4.000.000)%n", contador);
        rodar(() -> { for (int i = 0; i < N; i++) incrementarSync(); });
        System.out.printf("synchronized  : %,d%n", contadorSync);
        rodar(() -> { for (int i = 0; i < N; i++) contadorAtomico.incrementAndGet(); });
        System.out.printf("AtomicInteger : %,d%n", contadorAtomico.get());
    }
}
