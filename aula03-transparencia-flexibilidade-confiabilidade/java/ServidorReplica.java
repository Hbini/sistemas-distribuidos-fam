import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.function.DoubleBinaryOperator;

/**
 * Aula 03: réplica do serviço "calculadora" escrita em Java.
 *
 * Usa EXATAMENTE o mesmo protocolo de texto da versão Python, por isso uma
 * réplica Java pode se registrar no serviço de nomes Python (servico_nomes.py)
 * e atender clientes Python. Isso é TRANSPARÊNCIA DE ACESSO e mostra a
 * ABERTURA (flexibilidade) do sistema: qualquer linguagem que siga o protocolo entra.
 *
 * Uso: java ServidorReplica.java 7101 [hostDoServicoDeNomes]
 */
public class ServidorReplica {

    // FLEXIBILIDADE: nova operação = nova linha no mapa.
    static final Map<String, DoubleBinaryOperator> OPERACOES = Map.of(
        "SOMA", (a, b) -> a + b,
        "SUB", (a, b) -> a - b,
        "MULT", (a, b) -> a * b,
        "DIV", (a, b) -> a / b
    );

    static void registrar(String hostNomes, int porta) throws Exception {
        try (Socket s = new Socket(hostNomes, 5000);
             PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
            out.println("REGISTRAR calculadora 127.0.0.1 " + porta);
            System.out.println("[replica-java-" + porta + "] registro: " + in.readLine());
        }
    }

    static void atender(Socket s, String identidade) {
        try (s;
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8)) {
            String linha;
            while ((linha = in.readLine()) != null) {
                String resposta;
                try {
                    String[] p = linha.trim().split("\\s+");
                    double r = OPERACOES.get(p[0].toUpperCase())
                                        .applyAsDouble(Double.parseDouble(p[1]), Double.parseDouble(p[2]));
                    resposta = r + " (atendido por " + identidade + ")";
                } catch (Exception e) {
                    resposta = "ERRO " + e.getClass().getSimpleName();
                }
                System.out.println("[" + identidade + "] " + linha + " -> " + resposta);
                out.println(resposta);
            }
        } catch (Exception ignorada) {
            // cliente desconectou
        }
    }

    public static void main(String[] args) throws Exception {
        int porta = Integer.parseInt(args[0]);
        String hostNomes = args.length > 1 ? args[1] : "127.0.0.1";
        String identidade = "replica-java-" + porta + "@" + InetAddress.getLocalHost().getHostName();
        try (ServerSocket servidor = new ServerSocket(porta)) {
            registrar(hostNomes, porta);
            System.out.println("[" + identidade + "] pronta");
            while (true) {
                Socket s = servidor.accept();
                new Thread(() -> atender(s, identidade)).start();
            }
        }
    }
}
