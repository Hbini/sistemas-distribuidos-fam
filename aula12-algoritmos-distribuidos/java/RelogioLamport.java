/**
 * Aula 12: relógios lógicos de Lamport (mesmo roteiro de relogio_lamport.py).
 * Regras: evento/envio C++ ; mensagem leva C ; recepção C = max(C, Cmsg) + 1.
 * Executar: java RelogioLamport.java
 */
public class RelogioLamport {
    static class Processo {
        final String nome; int c = 0;
        Processo(String nome) { this.nome = nome; }
        void local(String d) { c++; System.out.printf("%s: %-26s C=%d%n", nome, d, c); }
        int enviar(String destino, String msg) { c++; System.out.printf("%s: envia '%s' para %-8s C=%d%n", nome, msg, destino, c); return c; }
        void receber(String msg, int carimbo) {
            int antes = c;
            c = Math.max(c, carimbo) + 1;
            System.out.printf("%s: recebe '%s' (carimbo %d)  C = max(%d, %d) + 1 = %d%n", nome, msg, carimbo, antes, carimbo, c);
        }
    }

    public static void main(String[] args) {
        Processo p1 = new Processo("P1"), p2 = new Processo("P2"), p3 = new Processo("P3");
        p1.local("calcula pedido");
        int m1 = p1.enviar("P2", "m1");
        p3.local("lê sensor");
        p3.local("grava log");
        p3.local("atualiza cache");
        int m2 = p3.enviar("P2", "m2");
        p2.receber("m1", m1);
        p2.receber("m2", m2);
        p2.local("processa dados");
        int m3 = p2.enviar("P1", "m3");
        p1.receber("m3", m3);
    }
}
