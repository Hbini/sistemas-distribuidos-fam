import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Aula 09: nó P2P em Java com busca por inundação. Mesmo protocolo do no_p2p.py,
 * então nós Java e Python podem formar UMA MESMA rede P2P.
 *
 * Uso: java NoP2P.java <porta> <arquivos separados por vírgula ou -> <vizinhos separados por vírgula>
 * Ex.: java NoP2P.java 8106 filme.mp4 127.0.0.1:8101
 */
public class NoP2P {
    final int porta;
    final String endereco;
    final Set<String> arquivos;
    final List<String> vizinhos;
    final Set<String> vistas = ConcurrentHashMap.newKeySet();

    NoP2P(int porta, Set<String> arquivos, List<String> vizinhos) {
        this.porta = porta; this.arquivos = arquivos; this.vizinhos = vizinhos;
        this.endereco = "127.0.0.1:" + porta;
    }

    void iniciar() throws Exception {
        ServerSocket srv = new ServerSocket(porta);
        Thread t = new Thread(() -> {
            while (true) {
                try (Socket s = srv.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8))) {
                    String linha = in.readLine();
                    if (linha != null) new Thread(() -> tratar(linha.trim())).start();
                } catch (Exception ignorada) { }
            }
        });
        t.setDaemon(true);
        t.start();
    }

    void tratar(String linha) {
        String[] p = linha.split(" ");
        if (p[0].equals("BUSCA")) {
            String id = p[1], arquivo = p[3], origem = p[4];
            int ttl = Integer.parseInt(p[2]);
            if (!vistas.add(id)) return;                 // já vi esta busca
            if (arquivos.contains(arquivo)) enviar(origem, "ACHEI " + id + " " + arquivo + " " + endereco);
            if (ttl > 1) for (String v : vizinhos) enviar(v, "BUSCA " + id + " " + (ttl - 1) + " " + arquivo + " " + origem);
        } else if (p[0].equals("ACHEI")) {
            System.out.println("[" + endereco + "] '" + p[2] + "' encontrado em " + p[3]);
        }
    }

    void enviar(String destino, String msg) {
        String[] hp = destino.split(":");
        try (Socket s = new Socket()) {
            s.connect(new InetSocketAddress(hp[0], Integer.parseInt(hp[1])), 2000);
            new PrintWriter(s.getOutputStream(), true, StandardCharsets.UTF_8).println(msg);
        } catch (Exception ignorada) { }
    }

    void buscar(String arquivo) {
        String id = UUID.randomUUID().toString().substring(0, 8);
        vistas.add(id);
        System.out.println("[" + endereco + "] buscando '" + arquivo + "'...");
        for (String v : vizinhos) enviar(v, "BUSCA " + id + " 4 " + arquivo + " " + endereco);
    }

    public static void main(String[] args) throws Exception {
        int porta = Integer.parseInt(args[0]);
        Set<String> arqs = args.length > 1 && !args[1].equals("-") ? new HashSet<>(Arrays.asList(args[1].split(","))) : new HashSet<>();
        List<String> viz = args.length > 2 ? Arrays.asList(args[2].split(",")) : List.of();
        NoP2P no = new NoP2P(porta, arqs, viz);
        no.iniciar();
        System.out.println("Nó Java " + no.endereco + " com " + arqs + "; vizinhos " + viz + ". Digite um arquivo para buscar:");
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) {
            String a = teclado.nextLine().trim();
            if (!a.isEmpty()) no.buscar(a);
        }
    }
}
