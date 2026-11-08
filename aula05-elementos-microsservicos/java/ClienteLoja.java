import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Aula 05: cliente Java que conversa só com o API Gateway (porta 8000),
 * usando o HttpClient padrão do Java 11+.
 * Executar: java ClienteLoja.java
 */
public class ClienteLoja {
    static final HttpClient HTTP = HttpClient.newHttpClient();
    static final String GATEWAY = "http://localhost:8000";

    static String chamar(String metodo, String caminho, String json) throws Exception {
        HttpRequest.Builder b = HttpRequest.newBuilder(URI.create(GATEWAY + caminho))
            .header("Content-Type", "application/json");
        b = metodo.equals("POST") ? b.POST(HttpRequest.BodyPublishers.ofString(json)) : b.GET();
        HttpResponse<String> r = HTTP.send(b.build(), HttpResponse.BodyHandlers.ofString());
        return r.statusCode() + " " + r.body();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("Cardápio: " + chamar("GET", "/api/catalogo/produtos", null));
        System.out.println("Pedido:   " + chamar("POST", "/api/pedidos", "{\"produto_id\": 2, \"quantidade\": 1}"));
        System.out.println("Pedidos:  " + chamar("GET", "/api/pedidos", null));
    }
}
