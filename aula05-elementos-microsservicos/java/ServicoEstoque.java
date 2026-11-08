import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Aula 05: Microsserviço ESTOQUE escrito em JAVA (porta 8002).
 *
 * Convive com os serviços Python (catálogo, pedidos, gateway) porque todos
 * conversam por HTTP + JSON. Esta é uma das vantagens dos microsserviços:
 * cada serviço pode usar a linguagem e o banco de dados mais adequados
 * (heterogeneidade / "poliglotismo").
 *
 * Usa apenas a biblioteca padrão do JDK (com.sun.net.httpserver).
 *
 * Rotas:
 *   GET  /saude
 *   GET  /estoque/{id}
 *   POST /estoque/{id}/baixar     corpo: {"quantidade": 2}
 *
 * Executar: java ServicoEstoque.java
 */
public class ServicoEstoque {

    // Dados PRÓPRIOS do serviço. ConcurrentHashMap porque várias threads atendem ao mesmo tempo.
    static final Map<Integer, Integer> ESTOQUE = new ConcurrentHashMap<>(Map.of(1, 20, 2, 15, 3, 30, 4, 0));
    static final Pattern QTD = Pattern.compile("\"quantidade\"\\s*:\\s*(\\d+)");

    static void responder(HttpExchange troca, int status, String json) throws IOException {
        byte[] dados = json.getBytes(StandardCharsets.UTF_8);
        troca.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        troca.sendResponseHeaders(status, dados.length);
        try (OutputStream os = troca.getResponseBody()) {
            os.write(dados);
        }
    }

    static void tratar(HttpExchange troca) throws IOException {
        String metodo = troca.getRequestMethod();
        String[] partes = troca.getRequestURI().getPath().replaceAll("^/+|/+$", "").split("/");
        System.out.println("[estoque-java] " + metodo + " " + troca.getRequestURI());
        try {
            if (partes[0].equals("saude")) {
                responder(troca, 200, "{\"status\": \"ok\", \"servico\": \"estoque\", \"linguagem\": \"java\"}");
                return;
            }
            int id = Integer.parseInt(partes[1]);
            if (!ESTOQUE.containsKey(id)) {
                responder(troca, 404, "{\"erro\": \"produto sem cadastro de estoque\"}");
            } else if (metodo.equals("GET") && partes.length == 2) {
                responder(troca, 200, "{\"produto_id\": " + id + ", \"quantidade\": " + ESTOQUE.get(id) + "}");
            } else if (metodo.equals("POST") && partes.length == 3 && partes[2].equals("baixar")) {
                String corpo = new String(troca.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                Matcher m = QTD.matcher(corpo);
                int qtd = m.find() ? Integer.parseInt(m.group(1)) : 1;
                // synchronized: verificar e baixar precisa ser ATÔMICO (evita vender o que não existe)
                synchronized (ESTOQUE) {
                    int atual = ESTOQUE.get(id);
                    if (atual < qtd) {
                        responder(troca, 409, "{\"erro\": \"estoque insuficiente\", \"disponivel\": " + atual + "}");
                        return;
                    }
                    ESTOQUE.put(id, atual - qtd);
                }
                responder(troca, 200, "{\"produto_id\": " + id + ", \"restante\": " + ESTOQUE.get(id) + "}");
            } else {
                responder(troca, 404, "{\"erro\": \"rota não encontrada\"}");
            }
        } catch (RuntimeException e) {
            responder(troca, 400, "{\"erro\": \"requisição inválida\"}");
        }
    }

    public static void main(String[] args) throws Exception {
        int porta = Integer.parseInt(System.getenv().getOrDefault("PORTA", "8002"));
        HttpServer servidor = HttpServer.create(new InetSocketAddress(porta), 0);
        servidor.createContext("/", ServicoEstoque::tratar);
        servidor.setExecutor(Executors.newFixedThreadPool(8));
        servidor.start();
        System.out.println("[estoque-java] ouvindo na porta " + porta);
    }
}
