import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.IntStream;

/**
 * Aula 06: chamada síncrona x assíncrona em Java com CompletableFuture.
 * Executar: java SincronaAssincrona.java
 */
public class SincronaAssincrona {
    static String servicoLento(String pedido) {
        try { Thread.sleep(1000); } catch (InterruptedException ignorada) { }
        return "resposta para " + pedido;
    }

    public static void main(String[] args) {
        long t0 = System.nanoTime();
        for (int i = 0; i < 3; i++) System.out.println("  " + servicoLento("pedido " + i));
        System.out.printf("Síncrona: %.1f s%n%n", (System.nanoTime() - t0) / 1e9);

        t0 = System.nanoTime();
        List<CompletableFuture<String>> futuros = IntStream.range(0, 3)
            .mapToObj(i -> CompletableFuture.supplyAsync(() -> servicoLento("pedido " + i)))
            .toList();
        System.out.println("  cliente: pedidos enviados, sigo trabalhando...");
        futuros.forEach(f -> f.thenAccept(r -> System.out.println("  callback recebeu: " + r)));
        CompletableFuture.allOf(futuros.toArray(new CompletableFuture[0])).join();
        System.out.printf("Assíncrona: %.1f s%n", (System.nanoTime() - t0) / 1e9);
    }
}
