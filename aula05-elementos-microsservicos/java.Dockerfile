# Serviço de estoque em Java, executado direto do código-fonte (Java 21).
FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY java/ServicoEstoque.java /app/
CMD ["java", "ServicoEstoque.java"]
