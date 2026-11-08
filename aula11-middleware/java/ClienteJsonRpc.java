import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Aula 11: cliente JAVA chamando um servidor JSON-RPC escrito em PYTHON.
 * O padrão JSON-RPC 2.0 é o "acordo" que permite a interoperabilidade.
 * Executar: python ../python/jsonrpc_servidor.py   e depois   java ClienteJsonRpc.java
 */
public class ClienteJsonRpc {
    static final HttpClient HTTP = HttpClient.newHttpClient();
    static int id = 0;

    static String chamar(String metodo, String paramsJson) throws Exception {
        String corpo = "{\"jsonrpc\": \"2.0\", \"method\": \"" + metodo + "\", \"params\": " + paramsJson + ", \"id\": " + (++id) + "}";
        HttpRequest req = HttpRequest.newBuilder(URI.create("http://127.0.0.1:9801"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(corpo)).build();
        return HTTP.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("moedas()            -> " + chamar("moedas", "[]"));
        System.out.println("converter(10, USD)  -> " + chamar("converter", "[10, \"USD\"]"));
        System.out.println("converter(10, JPY)  -> " + chamar("converter", "[10, \"JPY\"]"));
    }
}
