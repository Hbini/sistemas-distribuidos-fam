import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Aula 09: ordem total com sequenciador (simulação), versão Java de
 * ordem_total_sequenciador.py. Executar: java OrdemTotal.java
 */
public class OrdemTotal {
    record Msg(int seq, String op) { }

    static class Membro {
        final String nome; final boolean comSeq;
        int saldo = 0, proximo = 1;
        final List<String> entregues = new ArrayList<>();
        final PriorityQueue<Msg> pendentes = new PriorityQueue<>((a, b) -> a.seq() - b.seq());

        Membro(String nome, boolean comSeq) { this.nome = nome; this.comSeq = comSeq; }

        synchronized void receber(Msg m) {
            if (!comSeq) { entregar(m.op()); return; }
            pendentes.add(m);
            while (!pendentes.isEmpty() && pendentes.peek().seq() == proximo) {
                entregar(pendentes.poll().op());
                proximo++;
            }
        }

        void entregar(String op) {
            if (op.startsWith("saldo = ")) saldo = Integer.parseInt(op.substring(8));
            else if (op.startsWith("saldo += ")) saldo += Integer.parseInt(op.substring(9));
            else saldo *= Integer.parseInt(op.substring(9));
            entregues.add(op);
        }
    }

    static void experimento(boolean comSeq) throws Exception {
        String[] ops = {"saldo = 100", "saldo += 10", "saldo *= 2"};
        List<Membro> membros = new ArrayList<>();
        for (int i = 1; i <= 4; i++) membros.add(new Membro("réplica " + i, comSeq));
        ScheduledExecutorService rede = Executors.newScheduledThreadPool(8);
        Random r = new Random();
        for (int seq = 1; seq <= ops.length; seq++) {
            Msg m = new Msg(seq, ops[seq - 1]);
            for (Membro mb : membros) rede.schedule(() -> mb.receber(m), r.nextInt(300), TimeUnit.MILLISECONDS);
            Thread.sleep(50);
        }
        rede.shutdown();
        rede.awaitTermination(2, TimeUnit.SECONDS);
        System.out.println("\n=== " + (comSeq ? "COM sequenciador" : "SEM sequenciador") + " ===");
        for (Membro mb : membros) System.out.printf("%s: saldo = %4d | ordem: %s%n", mb.nome, mb.saldo, mb.entregues);
    }

    public static void main(String[] args) throws Exception {
        experimento(false);
        experimento(true);
    }
}
