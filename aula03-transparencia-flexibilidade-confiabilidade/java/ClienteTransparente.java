import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Aula 03: cliente com transparência de localização, replicação e falha.
 *
 * O método calcular() esconde do restante do programa:
 *   - ONDE estão os servidores (pergunta ao serviço de nomes);
 *   - QUANTAS cópias existem (recebe uma lista de réplicas);
 *   - QUE alguma delas caiu (tenta a próxima automaticamente).
 *
 * Uso: java ClienteTransparente.java
 * (antes, suba servico_nomes.py e algumas réplicas, em Python ou em Java)
 */
public class ClienteTransparente {

    static final String HOST_NOMES = "127.0.0.1";

    static String enviarLinha(String host, int porta, String mensagem, int timeoutMs) throws Exception {
        try (Socket s = new Socket()) {
            s.connect(new InetSocketAddress(host, porta), timeoutMs);
            s.setSoTimeout(timeoutMs);
            PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
            BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
            out.println(mensagem);
            return in.readLine();
        }
    }

    static List<String> resolver(String nome) throws Exception {
        String r = enviarLinha(HOST_NOMES, 5000, "RESOLVER " + nome, 3000);
        if (r == null || r.equals("VAZIO")) return new ArrayList<>();
        return new ArrayList<>(Arrays.asList(r.split(",")));
    }

    static String calcular(String op, double a, double b) throws Exception {
        List<String> replicas = resolver("calculadora");
        Collections.shuffle(replicas); // distribui a carga
        for (String endereco : replicas) {
            String[] hp = endereco.split(":");
            try {
                return enviarLinha(hp[0], Integer.parseInt(hp[1]), op + " " + a + " " + b, 2000);
            } catch (Exception e) {
                System.out.println("   (aviso interno: " + endereco + " não respondeu, tentando outra)");
            }
        }
        throw new IllegalStateException("nenhuma réplica disponível");
    }

    public static void main(String[] args) throws Exception {
        String[] ops = {"SOMA", "MULT", "SUB", "DIV"};
        for (int i = 0; i < 20; i++) {
            String op = ops[i % ops.length];
            try {
                System.out.println(op + " 8 2 = " + calcular(op, 8, 2));
            } catch (IllegalStateException e) {
                System.out.println("FALHA TOTAL: " + e.getMessage());
            }
            Thread.sleep(1000);
        }
    }
}
