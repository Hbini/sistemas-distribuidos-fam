import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * Aula 08: cliente de chat em Java (uma thread lê o teclado, outra recebe).
 * Executar: java ChatCliente.java <apelido> [ip]
 */
public class ChatCliente {
    public static void main(String[] args) throws Exception {
        String apelido = args.length > 0 ? args[0] : "aluno-java";
        String host = args.length > 1 ? args[1] : "127.0.0.1";
        Socket s = new Socket(host, 9600);
        PrintWriter out = new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
        out.println(apelido);

        Thread receptora = new Thread(() -> {
            try {
                String linha;
                while ((linha = in.readLine()) != null) System.out.println(linha);
            } catch (Exception ignorada) { }
            System.out.println("Conexão encerrada.");
        });
        receptora.setDaemon(true);
        receptora.start();

        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String msg = teclado.nextLine();
            if (msg.equals("/sair")) break;
            out.println(msg);
        }
        s.close();
    }
}
