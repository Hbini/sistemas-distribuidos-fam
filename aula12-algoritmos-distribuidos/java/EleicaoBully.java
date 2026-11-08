import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

/**
 * Aula 12: eleição de líder pelo algoritmo do Valentão (Bully).
 * Uso: java EleicaoBully.java [n] [detector] [ids caídos...]
 * Ex.: java EleicaoBully.java 5 2 5
 */
public class EleicaoBully {
    static int n, coordenador, mensagens = 0;
    static Set<Integer> caidos = new TreeSet<>();

    static void eleicao(int iniciador, String recuo) {
        List<Integer> maiores = new ArrayList<>(), responderam = new ArrayList<>();
        for (int i = iniciador + 1; i <= n; i++) maiores.add(i);
        System.out.println(recuo + "P" + iniciador + " envia ELEIÇÃO para " + maiores);
        mensagens += maiores.size();
        for (int i : maiores) {
            if (caidos.contains(i)) System.out.println(recuo + "   P" + i + " não responde");
            else { responderam.add(i); System.out.println(recuo + "   P" + i + " responde OK"); }
        }
        mensagens += responderam.size();
        if (responderam.isEmpty()) {
            coordenador = iniciador;
            mensagens += n - 1 - caidos.size();
            System.out.println(recuo + ">>> P" + iniciador + " é o NOVO COORDENADOR e avisa todos");
        } else {
            eleicao(responderam.get(0), recuo + "   ");
        }
    }

    public static void main(String[] args) {
        n = args.length > 0 ? Integer.parseInt(args[0]) : 5;
        int detector = args.length > 1 ? Integer.parseInt(args[1]) : 2;
        if (args.length > 2) for (int i = 2; i < args.length; i++) caidos.add(Integer.parseInt(args[i]));
        else caidos.add(n);
        System.out.println("Processos 1.." + n + " | caídos: " + caidos + " | P" + detector + " detectou a falha\n");
        eleicao(detector, "");
        System.out.println("\nCoordenador: P" + coordenador + " | mensagens (aprox.): " + mensagens);
    }
}
