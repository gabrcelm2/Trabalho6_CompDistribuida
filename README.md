# Comparação de Tecnologias de Invocação de Serviços Remotos

Projeto acadêmico desenvolvido para avaliar e comparar o desempenho de quatro tecnologias de invocação remota (**REST**, **GraphQL**, **SOAP** e **gRPC**) sob diferentes cenários de estresse e carga de usuários. O backend foi desenvolvido em duas linguagens de programação (**Java** e **Python**) para proporcionar um comparativo não apenas de protocolo, mas também de ecossistema.

---

# Descoberta Importante: Tamanho das Respostas gRPC

Durante a análise dos resultados dos testes de carga, foi identificado que a ferramenta utilizada registrava o campo **Average Content Size** das requisições gRPC como **0 bytes**.

Esse resultado não significa que as respostas gRPC não possuíam conteúdo. O valor aparecia como zero porque o cliente de teste utilizado para integrar o gRPC não informava automaticamente à ferramenta o tamanho da resposta recebida.

Diferentemente de REST, GraphQL e SOAP, que normalmente transportam dados textuais em formatos como **JSON** e **XML**, o gRPC utiliza mensagens binárias serializadas com **Protocol Buffers**, transportadas em frames do protocolo **HTTP/2**. Por esse motivo, o tamanho da resposta não foi capturado automaticamente no relatório padrão da ferramenta.

## Como o tamanho foi descoberto

Para descobrir o tamanho real das respostas, foi calculado diretamente no servidor o comprimento do array de bytes produzido após a serialização da mensagem com Protobuf.

Em outras palavras, após criar a resposta gRPC, a mensagem foi serializada e seu tamanho foi obtido por meio do seu comprimento em bytes:

```text
Tamanho da resposta = length(mensagem serializada pelo Protobuf)
```

Esse procedimento permitiu descobrir o peso real dos payloads enviados pelo servidor, mesmo que a ferramenta de teste apresentasse o valor como zero.

## Resultados encontrados

| Operação gRPC         | 100 usuários | 250 usuários | 500 usuários | Tamanho aproximado |
| --------------------- | -----------: | -----------: | -----------: | -----------------: |
| `ListUsers`           | 24.777 bytes | 24.777 bytes | 24.777 bytes |              24 KB |
| `ListSongs`           | 21.154 bytes | 21.154 bytes | 21.154 bytes |              21 KB |
| `ListPlaylistsByUser` |    303 bytes |    303 bytes |    303 bytes |             0,3 KB |

### Interpretação dos resultados

* A operação `ListUsers` retornou uma mensagem serializada de **24.777 bytes**, aproximadamente **24 KB**.
* A operação `ListSongs` retornou uma mensagem serializada de **21.154 bytes**, aproximadamente **21 KB**.
* A operação `ListPlaylistsByUser`, consultando as playlists de apenas um usuário, retornou somente **303 bytes**.

Portanto, o valor **0 bytes** exibido no relatório deve ser interpretado como uma limitação da instrumentação do teste, e não como ausência de dados na resposta gRPC.

---

## 1. Identificação da Equipe

* **Alanis Aguiar Bitencourt - 2315059**
* **Livia Catarina Modesto Macedo - 2315085**
* **Gabriel Costa Castro - 2314515**

---

## 2. Tecnologias de Invocação Remota

No escopo deste projeto, construímos endpoints equivalentes em quatro abordagens diferentes:

### REST (Representational State Transfer)
- **Características**: Padrão arquitetural baseado no protocolo HTTP. Utiliza verbos padrão (GET, POST, PUT, DELETE) e é totalmente sem estado. O formato de comunicação mais comum é o JSON.
- **Vantagens**: Universal, leve, amplamente suportado por navegadores nativamente e altamente escalável. Curva de aprendizado baixa.
- **Desvantagens**: Sofre com problemas de *Over-fetching* (baixar dados a mais do que o necessário) e *Under-fetching* (necessitar de múltiplas requisições para preencher uma tela).

### GraphQL
- **Características**: É uma linguagem de consulta para APIs. Em vez de múltiplos endpoints, expõe um único endpoint (`/graphql`) onde o cliente define no corpo da requisição exatamente a estrutura de dados que deseja receber.
- **Vantagens**: Elimina completamente o over-fetching e under-fetching. Alta flexibilidade para o Frontend montar consultas dinâmicas.
- **Desvantagens**: O processamento pesado fica delegado ao servidor (resolução das *queries*). Muito verboso para operações simples e complexo para cache HTTP clássico.

### SOAP (Simple Object Access Protocol)
- **Características**: Protocolo baseado fortemente em XML. Exige um documento rigoroso (WSDL e XSD) que atua como contrato entre cliente e servidor, especificando regras de transação rígidas e namespaces.
- **Vantagens**: Extremamente seguro e robusto, altamente padronizado, garante a validade do payload pela camada de contrato (schema validation). Muito comum em sistemas bancários e legados.
- **Desvantagens**: Altamente verboso, os payloads XML são muito maiores que JSON, resultando em menor performance de rede e maior gasto de processador no *parsing* de XML.

### gRPC (gRPC Remote Procedure Calls)
- **Características**: Framework de chamadas de procedimento remoto operando diretamente sobre o protocolo HTTP/2. Utiliza *Protocol Buffers* (Protobuf) como linguagem para serializar dados de forma binária em vez de texto puro.
- **Vantagens**: Extremamente rápido e compacto, consumo baixíssimo de largura de banda devido à serialização binária. Suporte bidirecional e multiplexação via HTTP/2.
- **Desvantagens**: Dificuldade de depuração (conteúdo trafegado em binário não pode ser lido por humanos no navegador). Pouco suporte nativo diretamente do client-side de navegadores sem uso de proxies (como gRPC-Web).

---

## 3. Análise Crítica e Testes de Carga

Realizamos testes de carga rigorosos simulando usuários virtuais clicando nas rotas simultaneamente sem "pesos" pré-definidos (rotas consumidas de maneira 100% equiprovável/aleatória). A métrica de verificação de sucesso e estabilidade foi o **Tempo Percentil 95 (P95)** em milissegundos.

### Análise: Python vs Java no Contexto de APIs de Streaming
Durante os testes de estresse (com cenários de 100, 250 e 500 usuários), notamos diferenças arquiteturais profundas:

- **Ecossistema Java (Spring Boot + Tomcat)**: Apresentou excelente eficiência de memória com o uso do `HikariCP` (Pool de Conexões), suportando concorrência alta. Em cargas extremas (500 usuários), as portas atreladas ao servidor web Tomcat (REST, GraphQL e SOAP) sofreram com saturação no Pool e recusa de conexões, enquanto a porta do `gRPC`, suportada pelo servidor interno do `Netty`, permaneceu ilesa e com tempo quase na faixa de `11ms`.
- **Ecossistema Python (FastAPI/Spyne)**: Dada a existência do **GIL (Global Interpreter Lock)** no Python, a desserialização de XML do SOAP resultou no gargalo mais pesado entre todas as opções. No entanto, aplicando a migração das rotas do REST para abordagens baseadas em eventos (`async def`), a eficiência do FastAPI tornou o Python surpreendentemente mais rápido e resistente a falhas massivas, apesar de ainda engasgar na resolução sequencial pesada das complexas rotas do GraphQL.
- **Duelo SOAP x gRPC**: O SOAP exibiu disparado a menor performance nos dois frameworks devido ao overhead altíssimo de validação XSD e serialização das bibliotecas `lxml`. Enquanto isso, o **gRPC operou como o pilar mais escalável** de toda a arquitetura, mostrando praticamente a mesma latência irrelevante (menos de 20ms) tanto em 100 usuários quanto sob ataque pesado.

---

## 4. Gráficos de Resultados

Abaixo seguem os gráficos que demonstram o Tempo de Resposta (P95) das quatro APIs em três intensidades progressivas de carga. As requisições que não puderam ser atendidas dentro do tempo de conexão geraram erros de `ConnectionRefused`, indicando exaustão real de threads de I/O na máquina testada.

### === CENÁRIO 1: 100 Usuários Simultâneos ===

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/7606b44e-ae2e-4dd6-96f4-752efd543007" />

> *Cenário 1: Desempenho interno do ecossistema Python sob carga de 100 usuários. Taxa de erro: **0.0%**.*

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/1a9ee78a-898a-4b53-bd98-1e6bf9cc2398" />

> *Cenário 1: Desempenho interno do ecossistema Java sob carga de 100 usuários. Taxa de erro: **0.0%**.*

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/e7dc2c2d-dfb5-481c-abef-35d1d54f3189" />

> *Cenário 1: Gráfico comparativo lado a lado (Java vs Python). Nota-se a superioridade natural de serialização JSON do Java logo nas faixas iniciais, contrastando com o gRPC que já se mantém irrelevante aos gargalos.*

---

### === CENÁRIO 2: 250 Usuários Simultâneos ===

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/9e1d2a3b-ee83-484a-98af-9242a57685e8" />

> *Cenário 2: Desempenho do Python com 250 usuários. A saturação da conversão assíncrona causa picos notáveis no SOAP e no GraphQL. Taxa de erro observada: **0.0%**.*

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/2cd2e1e1-364f-4f90-8544-31bbf0256875" />

> *Cenário 2: Desempenho do Java sob 250 usuários. O tempo do SOAP sobe bruscamente devido ao alto consumo de CPU instanciando serializadores JAX-WS. Taxa de erro: **0.0%**.*

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/dbb5036e-4826-46b4-9b7d-db55168dfdb2" />

> *Cenário 2: Visão global em 250 usuários. O abismo arquitetural de validação XML se torna o maior entrave da arquitetura.*

---

### === CENÁRIO 3: 500 Usuários Simultâneos (Estresse Total) ===

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/b5c82d98-2bba-453f-9c2c-6c9578bd94b3" />

> *Cenário 3: No extremo de 500 usuários, o ambiente Python começa a sofrer Timeout na barreira de conexão do socket. O gRPC se destaca perante os outros protocolos HTTP/1.1. Taxa de erro (Connection Refused): **~15%**.*

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/0df9fe93-9f14-40df-a9c6-ae83f5c523ea" />

> *Cenário 3: No limite da exaustão do Java, as rotas que dependem do servidor Tomcat congestionam o Worker Pool do servidor provocando recusas de requisição HTTP, com o gRPC se sobressaindo totalmente imune rodando pelo Netty. Taxa de erro: **~10%** nas rotas web tradicionais.*

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/a9eb405b-369b-4f3c-9002-b748d5baec4b" />

> *Cenário 3: Fim da escalada de testes. A conclusão final coroa o gRPC como a solução corporativa ideal sob alta latência para o domínio do aplicativo, suplantando os problemas severos do ecossistema SOAP.*
