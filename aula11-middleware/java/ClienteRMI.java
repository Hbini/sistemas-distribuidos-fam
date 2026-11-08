import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Map;

/**
 * Aula 11: cliente Java RMI. Procura o objeto pelo NOME no registry e chama
 * seus métodos como se fosse um objeto local. Nenhum socket aparece no código.
 * Executar: java ClienteRMI.java [ip_do_servidor]
 */

// Observação: com 'java Arquivo.java' a classe com main precisa ser a PRIMEIRA do arquivo.
public class ClienteRMI {
    public static void main(String[] args) throws Exception {
        String host = args.length > 0 ? args[0] : "127.0.0.1";
        Registry registry = LocateRegistry.getRegistry(host, 1099);
        Lanchonete lanchonete = (Lanchonete) registry.lookup("Lanchonete");   // recebe o STUB

        System.out.println("Classe do objeto recebido: " + lanchonete.getClass().getName() + " (é um proxy!)");
        System.out.println("Preço da coxinha: " + lanchonete.precoDe("coxinha"));
        System.out.println("Total: " + lanchonete.calcularTotal(Map.of("coxinha", 2, "suco", 1)));
        System.out.println(lanchonete.fazerPedido("Ana", "pastel"));
    }
}

// Cópia da interface remota (o contrato precisa ser o mesmo nos dois lados).
interface Lanchonete extends Remote {
    double precoDe(String item) throws RemoteException;
    double calcularTotal(Map<String, Integer> itens) throws RemoteException;
    String fazerPedido(String cliente, String item) throws RemoteException;
}
