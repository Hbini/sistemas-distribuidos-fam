import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.Map;

/**
 * Aula 11: Middleware de OBJETOS DISTRIBUÍDOS: Java RMI (Remote Method Invocation).
 *
 * Diferença para RPC: em vez de chamar uma FUNÇÃO remota, o cliente chama um
 * MÉTODO de um OBJETO que vive em outra JVM. O RMI gera automaticamente o
 * STUB (proxy no cliente) e faz o marshalling por serialização Java.
 *
 * Peças:
 *   1. interface remota (contrato) que estende Remote
 *   2. implementação no servidor
 *   3. REGISTRY: serviço de nomes do RMI (porta 1099), onde o objeto é publicado
 *
 * Executar: java ServidorRMI.java      e depois   java ClienteRMI.java
 */

// Observação: com 'java Arquivo.java' a classe com main precisa ser a PRIMEIRA do arquivo.
public class ServidorRMI {
    public static void main(String[] args) throws Exception {
        Registry registry = LocateRegistry.createRegistry(1099);   // 3. sobe o serviço de nomes
        registry.rebind("Lanchonete", new LanchoneteImpl());       // publica o objeto com um NOME
        System.out.println("Objeto remoto 'Lanchonete' publicado no RMI Registry (porta 1099)");
    }
}

// 1. Contrato. O cliente tem uma cópia idêntica desta interface.
interface Lanchonete extends Remote {
    double precoDe(String item) throws RemoteException;
    double calcularTotal(Map<String, Integer> itens) throws RemoteException;
    String fazerPedido(String cliente, String item) throws RemoteException;
}

// 2. Implementação: o objeto "de verdade", que só existe no servidor.
class LanchoneteImpl extends UnicastRemoteObject implements Lanchonete {
    private final Map<String, Double> cardapio = Map.of("coxinha", 7.5, "pastel", 9.0, "suco", 6.0);
    private int numeroPedido = 0;

    LanchoneteImpl() throws RemoteException { super(); }

    public double precoDe(String item) {
        System.out.println("[servidor] precoDe(" + item + ")");
        return cardapio.getOrDefault(item, 0.0);
    }

    public double calcularTotal(Map<String, Integer> itens) {
        System.out.println("[servidor] calcularTotal(" + itens + ")");
        return itens.entrySet().stream().mapToDouble(e -> cardapio.getOrDefault(e.getKey(), 0.0) * e.getValue()).sum();
    }

    public synchronized String fazerPedido(String cliente, String item) {
        numeroPedido++;
        System.out.println("[servidor] pedido " + numeroPedido + ": " + item + " para " + cliente);
        return "Pedido #" + numeroPedido + " (" + item + ") registrado para " + cliente;
    }
}
