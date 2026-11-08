import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Aula 12: exclusão mútua distribuída de Ricart e Agrawala (simulação com threads).
 * Cada processo só se comunica por mensagens (filas). Ninguém usa trava compartilhada
 * para decidir quem entra; o AtomicBoolean serve apenas para DETECTAR uma violação.
 * Executar: java RicartAgrawala.java
 */
public class RicartAgrawala {
    static final int N = 3;
    static final List<BlockingQueue<int[]>> CAIXAS = new ArrayList<>();   // {tipo, carimbo, origem}; tipo 0=PEDIDO 1=OK
    static final AtomicBoolean EM_USO = new AtomicBoolean(false);

    static void enviar(int destino, int[] msg) {
        new Thread(() -> {
            try { Thread.sleep(ThreadLocalRandom.current().nextInt(10, 50)); } catch (InterruptedException ignorada) { }
            CAIXAS.get(destino).add(msg);
        }).start();
    }

    static class Processo extends Thread {
        final int pid;
        int relogio = 0, oks = 0, meuCarimbo = 0;
        String estado = "LIBERADO";
        final List<Integer> adiados = new ArrayList<>();
        CountDownLatch liberado;

        Processo(int pid) { this.pid = pid; setDaemon(true); }

        boolean meuPedidoAntes(int carimbo, int origem) {
            return meuCarimbo < carimbo || (meuCarimbo == carimbo && pid < origem);
        }

        @Override public void run() {
            while (true) {
                try {
                    int[] m = CAIXAS.get(pid).take();
                    synchronized (this) {
                        relogio = Math.max(relogio, m[1]) + 1;
                        if (m[0] == 0) {
                            boolean adiar = estado.equals("DENTRO") || (estado.equals("QUERENDO") && meuPedidoAntes(m[1], m[2]));
                            if (adiar) { adiados.add(m[2]); System.out.println("   P" + pid + " ADIA resposta a P" + m[2]); }
                            else enviar(m[2], new int[]{1, relogio, pid});
                        } else if (++oks == N - 1) {
                            liberado.countDown();
                        }
                    }
                } catch (InterruptedException e) { return; }
            }
        }

        void usarImpressora(String doc) throws InterruptedException {
            synchronized (this) {
                estado = "QUERENDO"; oks = 0; relogio++; meuCarimbo = relogio;
                liberado = new CountDownLatch(1);
            }
            System.out.println("P" + pid + " quer imprimir " + doc + " (carimbo " + meuCarimbo + ")");
            for (int o = 0; o < N; o++) if (o != pid) enviar(o, new int[]{0, meuCarimbo, pid});
            liberado.await();
            synchronized (this) { estado = "DENTRO"; }
            if (!EM_USO.compareAndSet(false, true)) throw new IllegalStateException("VIOLAÇÃO da exclusão mútua!");
            System.out.println(">>> P" + pid + " ENTROU e imprime " + doc);
            Thread.sleep(300);
            EM_USO.set(false);
            System.out.println("<<< P" + pid + " SAIU");
            List<Integer> paraResponder;
            synchronized (this) { estado = "LIBERADO"; paraResponder = new ArrayList<>(adiados); adiados.clear(); }
            for (int o : paraResponder) enviar(o, new int[]{1, relogio, pid});
        }
    }

    public static void main(String[] args) throws Exception {
        List<Processo> ps = new ArrayList<>();
        for (int i = 0; i < N; i++) { CAIXAS.add(new LinkedBlockingQueue<>()); }
        for (int i = 0; i < N; i++) { Processo p = new Processo(i); ps.add(p); p.start(); }
        String[] docs = {"boleto.pdf", "nota_fiscal.pdf", "relatorio.pdf"};
        List<Thread> clientes = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            final int k = i;
            Thread t = new Thread(() -> { try { ps.get(k).usarImpressora(docs[k]); } catch (InterruptedException ignorada) { } });
            clientes.add(t); t.start();
        }
        for (Thread t : clientes) t.join();
        System.out.println("\nTodos imprimiram, um por vez.");
    }
}
