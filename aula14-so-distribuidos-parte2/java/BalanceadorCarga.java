import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Random;

/**
 * Aula 14: políticas de balanceamento de carga (versão Java de balanceador_carga.py).
 * Executar: java BalanceadorCarga.java
 */
public class BalanceadorCarga {
    public static void main(String[] args) {
        Random r = new Random(42);
        int[] opcoes = {1, 1, 1, 2, 2, 5, 10};
        int[] tarefas = new int[200];
        for (int i = 0; i < tarefas.length; i++) tarefas[i] = opcoes[r.nextInt(opcoes.length)];
        String[] nomes = {"srv-1", "srv-2", "srv-3", "srv-4"};
        double[] velocidade = {1.0, 1.0, 1.0, 0.5};

        for (String politica : new String[]{"aleatória", "round robin", "menor carga"}) {
            double[] livre = new double[4];
            int[] cont = new int[4];
            for (int i = 0; i < tarefas.length; i++) {
                int s;
                if (politica.equals("aleatória")) s = r.nextInt(4);
                else if (politica.equals("round robin")) s = i % 4;
                else {
                    s = 0;
                    for (int k = 1; k < 4; k++)
                        if (livre[k] + tarefas[i] / velocidade[k] < livre[s] + tarefas[i] / velocidade[s]) s = k;
                }
                livre[s] += tarefas[i] / velocidade[s];
                cont[s] += tarefas[i]; // soma do trabalho recebido
            }
            double makespan = 0;
            Map<String, Integer> porServidor = new LinkedHashMap<>();
            for (int k = 0; k < 4; k++) { makespan = Math.max(makespan, livre[k]); porServidor.put(nomes[k], cont[k]); }
            System.out.printf("%-12s makespan = %6.1f s  trabalho por servidor: %s%n", politica, makespan, porServidor);
        }
    }
}
