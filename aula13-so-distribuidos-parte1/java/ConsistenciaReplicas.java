import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * Aula 13: consistência forte x eventual (versão Java de consistencia_forte_eventual.py).
 * Executar: java ConsistenciaReplicas.java
 */
public class ConsistenciaReplicas {
    static final int ATRASO = 500;

    static class Replica {
        final String nome; volatile int saldo = 100; volatile boolean acessivel = true;
        Replica(String n) { nome = n; }
        boolean aplicar(int v) {
            try { Thread.sleep(ATRASO); } catch (InterruptedException ignorada) { }
            if (!acessivel) return false;
            saldo = v; return true;
        }
    }

    static String ler(List<Replica> rs) {
        StringBuilder sb = new StringBuilder("  leituras:");
        for (Replica r : rs) sb.append(" ").append(r.nome).append("=").append(r.saldo);
        return sb.toString();
    }

    static void forte(List<Replica> rs, int v) {
        // fase 1 (preparar): todas precisam estar acessíveis, senão nada é gravado
        if (!rs.stream().allMatch(r -> r.acessivel)) {
            System.out.println("  escrita FORTE de " + v + " RECUSADA (partição)");
            return;
        }
        boolean ok = rs.stream().map(r -> CompletableFuture.supplyAsync(() -> r.aplicar(v)))
                       .toList().stream().allMatch(CompletableFuture::join);
        System.out.println("  escrita FORTE de " + v + (ok ? " confirmada por todas" : " RECUSADA (partição)"));
    }

    static void eventual(List<Replica> rs, int v) {
        rs.get(0).saldo = v;
        for (Replica r : rs.subList(1, rs.size())) CompletableFuture.runAsync(() -> r.aplicar(v));
        System.out.println("  escrita EVENTUAL de " + v + " confirmada na hora (só local)");
    }

    public static void main(String[] args) throws Exception {
        List<Replica> rs = List.of(new Replica("R1"), new Replica("R2"), new Replica("R3"));
        System.out.println("=== FORTE ===");
        forte(rs, 150); System.out.println(ler(rs));
        System.out.println("=== EVENTUAL ===");
        eventual(rs, 200); System.out.println(ler(rs) + "  <- logo após");
        Thread.sleep(ATRASO + 200); System.out.println(ler(rs) + "  <- após propagar");
        System.out.println("=== PARTIÇÃO (R3 isolada) ===");
        rs.get(2).acessivel = false;
        forte(rs, 300); System.out.println(ler(rs));
    }
}
