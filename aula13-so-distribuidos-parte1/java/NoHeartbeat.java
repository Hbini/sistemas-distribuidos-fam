import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;

/**
 * Aula 13: nó que envia heartbeat UDP, compatível com detector_falhas_heartbeat.py.
 * Executar: java NoHeartbeat.java servidor-Java [ip_do_monitor]
 */
public class NoHeartbeat {
    public static void main(String[] args) throws Exception {
        String nome = args.length > 0 ? args[0] : "no-java";
        InetAddress monitor = InetAddress.getByName(args.length > 1 ? args[1] : "127.0.0.1");
        try (DatagramSocket sock = new DatagramSocket()) {
            System.out.println("[" + nome + "] heartbeat a cada 1 s (Ctrl+C simula falha)");
            byte[] msg = ("VIVO " + nome).getBytes(StandardCharsets.UTF_8);
            while (true) {
                sock.send(new DatagramPacket(msg, msg.length, monitor, 9900));
                Thread.sleep(1000);
            }
        }
    }
}
