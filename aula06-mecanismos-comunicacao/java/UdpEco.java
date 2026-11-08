import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.Random;

/**
 * Aula 06: UDP em Java, com perda simulada de 30% no servidor.
 * Compatível com udp_vs_tcp.py (mesma porta 9200 e mesmo formato).
 *
 * Executar:
 *   java UdpEco.java servidor
 *   java UdpEco.java cliente
 */
public class UdpEco {
    static final int PORTA = 9200;

    public static void main(String[] args) throws Exception {
        if (args.length > 0 && args[0].equals("servidor")) {
            Random sorte = new Random();
            try (DatagramSocket sock = new DatagramSocket(PORTA)) {
                System.out.println("[udp-java] servidor na porta " + PORTA);
                byte[] buf = new byte[1024];
                while (true) {
                    DatagramPacket p = new DatagramPacket(buf, buf.length);
                    sock.receive(p);
                    String msg = new String(p.getData(), 0, p.getLength(), StandardCharsets.UTF_8);
                    if (sorte.nextDouble() < 0.30) {
                        System.out.println("(perdido) " + msg);
                        continue;
                    }
                    byte[] resp = ("eco: " + msg).getBytes(StandardCharsets.UTF_8);
                    sock.send(new DatagramPacket(resp, resp.length, p.getAddress(), p.getPort()));
                }
            }
        } else {
            try (DatagramSocket sock = new DatagramSocket()) {
                sock.setSoTimeout(300); // UDP não avisa perdas: precisamos de timeout
                int recebidas = 0;
                for (int i = 0; i < 50; i++) {
                    byte[] msg = ("mensagem " + i).getBytes(StandardCharsets.UTF_8);
                    sock.send(new DatagramPacket(msg, msg.length, InetAddress.getLoopbackAddress(), PORTA));
                    try {
                        sock.receive(new DatagramPacket(new byte[1024], 1024));
                        recebidas++;
                    } catch (SocketTimeoutException e) {
                        System.out.println("mensagem " + i + ": perdida");
                    }
                }
                System.out.println("Respostas recebidas: " + recebidas + "/50");
            }
        }
    }
}
