import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.MulticastSocket;
import java.net.NetworkInterface;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * Aula 09: membro de um grupo IP MULTICAST em Java.
 * Compatível com multicast_grupo.py (grupo 224.1.1.1, porta 5007).
 * Executar: java MulticastMembro.java Carla
 */
public class MulticastMembro {
    static final String GRUPO = "224.1.1.1";
    static final int PORTA = 5007;

    public static void main(String[] args) throws Exception {
        String nome = args.length > 0 ? args[0] : "membro-java";
        InetAddress grupo = InetAddress.getByName(GRUPO);
        MulticastSocket sock = new MulticastSocket(PORTA);
        // Entra no grupo usando a interface de rede padrão
        NetworkInterface interfaceRede = sock.getNetworkInterface();
        sock.joinGroup(new InetSocketAddress(grupo, PORTA), interfaceRede);
        sock.setTimeToLive(1);

        Thread receptora = new Thread(() -> {
            byte[] buf = new byte[1024];
            while (true) {
                try {
                    DatagramPacket p = new DatagramPacket(buf, buf.length);
                    sock.receive(p);
                    System.out.println(new String(p.getData(), 0, p.getLength(), StandardCharsets.UTF_8)
                        + "   (de " + p.getAddress().getHostAddress() + ")");
                } catch (Exception e) { return; }
            }
        });
        receptora.setDaemon(true);
        receptora.start();

        enviar(sock, grupo, "*** " + nome + " entrou no grupo");
        System.out.println(nome + " no grupo " + GRUPO + ":" + PORTA + ". Digite mensagens:");
        Scanner teclado = new Scanner(System.in);
        while (teclado.hasNextLine()) enviar(sock, grupo, "[" + nome + "] " + teclado.nextLine());
    }

    static void enviar(MulticastSocket sock, InetAddress grupo, String texto) throws Exception {
        byte[] dados = texto.getBytes(StandardCharsets.UTF_8);
        sock.send(new DatagramPacket(dados, dados.length, grupo, PORTA));
    }
}
