import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Aula 07: cliente JAVA do broker pub/sub Python (broker_pubsub.py).
 * Mostra que publicadores e assinantes podem ser de linguagens diferentes.
 *
 *   java ClientePubSub.java sub cardapio
 *   java ClientePubSub.java pub cardapio Hoje tem feijoada
 */
public class ClientePubSub {
    public static void main(String[] args) throws Exception {
        String modo = args[0], topico = args[1];
        try (Socket s = new Socket("127.0.0.1", 9300);
             PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
            if (modo.equals("sub")) {
                out.println("SUB " + topico);
                System.out.println("Assinando '" + topico + "'...");
                String linha;
                while ((linha = in.readLine()) != null) {
                    String[] p = linha.split(" ", 3);
                    System.out.println("[" + p[1] + "] " + p[2]);
                }
            } else {
                StringBuilder msg = new StringBuilder();
                for (int i = 2; i < args.length; i++) msg.append(i > 2 ? " " : "").append(args[i]);
                out.println("PUB " + topico + " " + msg);
                System.out.println("Broker respondeu: " + in.readLine());
            }
        }
    }
}
