import java.util.Arrays;

/**
 * Aula 12: relógios vetoriais e detecção de concorrência.
 * Executar: java RelogioVetorial.java
 */
public class RelogioVetorial {
    static final int N = 3;

    static class Processo {
        final int i; int[] v = new int[N];
        Processo(int i) { this.i = i; }
        int[] local(String nome) { v[i]++; System.out.println("P" + (i + 1) + ": " + nome + " " + Arrays.toString(v)); return v.clone(); }
        int[] receber(String nome, int[] w) {
            for (int k = 0; k < N; k++) v[k] = Math.max(v[k], w[k]);
            v[i]++;
            System.out.println("P" + (i + 1) + ": " + nome + " " + Arrays.toString(v) + "  (recebeu " + Arrays.toString(w) + ")");
            return v.clone();
        }
    }

    static boolean menorOuIgual(int[] a, int[] b) {
        for (int k = 0; k < N; k++) if (a[k] > b[k]) return false;
        return true;
    }

    static String relacao(String na, int[] a, String nb, int[] b) {
        if (menorOuIgual(a, b) && !Arrays.equals(a, b)) return na + " -> " + nb;
        if (menorOuIgual(b, a) && !Arrays.equals(a, b)) return nb + " -> " + na;
        return na + " || " + nb + "  (concorrentes)";
    }

    public static void main(String[] args) {
        Processo p1 = new Processo(0), p2 = new Processo(1), p3 = new Processo(2);
        int[] a = p1.local("a"), b = p1.local("b (envia a P2)");
        int[] c = p2.local("c"), d = p2.receber("d", b);
        int[] e = p3.local("e"), f = p2.local("f (envia a P3)"), g = p3.receber("g", f);
        System.out.println();
        System.out.println(relacao("a", a, "d", d));
        System.out.println(relacao("c", c, "e", e));
        System.out.println(relacao("e", e, "g", g));
    }
}
