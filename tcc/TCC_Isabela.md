Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
                    Defensor.IA: simplificando o direito do consumidor


                        Isabela Carezia da Silva1; Lauro Marques Vicari2
```

2
  Mestre em Administração Pública pela Fundação João Pinheiro e Bacharel em Ciências Econômicas pela
Universidade Federal de Viçosa, pesquisador na Agroicone. Agroicone, Avenida Angélica, nº 2447 - Conjunto
173 Higienópolis; 01227200 São Paulo, SP, Brasil
*autor correspondente: [isabela.carezia@usp.br](mailto:isabela.carezia@usp.br)

```
                                                                                                   1
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
                    Defensor.IA: simplificando o direito do consumidor
```

Resumo

```
    Este trabalho apresentou o desenvolvimento do Defensor.IA, um “chatbot” jurídico
```

voltado para orientar consumidores sobre seus direitos, especialmente em situações de
superendividamento e práticas abusivas, tendo em vista a crescente necessidade de acesso
simplificado à informação jurídica no Brasil. O objetivo geral foi desenvolver uma ferramenta
que proporcionasse orientação clara e acessível aos consumidores, utilizando uma
abordagem "no-code" e modelos de linguagem, como o GPT-4o. A metodologia empregou a
plataforma Chatling para criar o fluxo de trabalho e integrou a base de conhecimento, a fim
de garantir respostas fundamentadas e atualizadas. Os resultados indicaram que o
Defensor.IA forneceu respostas mais precisas e contextualizadas em comparação ao
ChatGPT-4o-mini, destacando-se pela precisão e adequação ao contexto jurídico.
Concluiu-se que o Defensor.IA é uma ferramenta viável para democratizar o acesso ao
direito do consumidor, promovendo inclusão e equidade no acesso à justiça de forma
simples e eficiente.
Palavras-chave: Chatbot; No-code; LLM; RAG Práticas abusivas; Superendividamento

```
                    Defensor.IA: A Legal Chatbot for Consumer Rights
```

Abstract

```
    This study presented the development of Defensor.IA, a legal chatbot designed to
```

guide consumers regarding their rights, especially in situations of over-indebtedness and
abusive practices, considering the growing need for accessible legal information in Brazil.
The main objective was to develop a tool that could provide clear and accessible guidance to
consumers, using a no-code approach and language models such as GPT-4o. The
methodology involved using the Chatling platform to create the chatbot and the knowledge
base to ensure well-founded and up-to-date responses. The results showed that Defensor.IA
provided more precise and contextualized answers compared to ChatGPT-4o-mini, standing
out for its accuracy and suitability to the legal context. It was concluded that Defensor.IA is a
viable tool to democratize access to consumer rights, promoting inclusion and equity in
access to justice in a simple and efficient manner.
Keywords: Chatbot; No-code; LLM; RAG; Abusive Practices; Over-indebtedness

Introdução

```
     O cenário jurídico e econômico brasileiro enfrenta desafios significativos na proteção
```

do consumidor, especialmente em relação ao superendividamento da população. De acordo
com a Pesquisa Nacional de Endividamento e Inadimplência do Consumidor [PEIC], em
julho de 2024, 78,5% das famílias brasileiras estavam endividadas, com 28,8% enfrentando
dívidas atrasadas e 11,9% incapazes de pagar suas obrigações financeiras. O
superendividamento é caracterizado pela incapacidade do consumidor de arcar com suas
dívidas de consumo sem que isso comprometa seu mínimo existencial (Machado, 2024).
Esses números revelam a fragilidade econômica da população e a vulnerabilidade dos
consumidores perante práticas abusivas e a falta de acesso à educação jurídica e financeira

```
                                                                                           2
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

adequada. Nesse contexto, é fundamental que o acesso à informação legal seja claro e
acessível, permitindo aos consumidores compreenderem e exercerem seus direitos
plenamente.
         Além disso, as cobranças abusivas representam um problema significativo,
agravando o superendividamento. Práticas ilegais, como a aplicação de juros exorbitantes e
ameaças, colocam o consumidor em desvantagem, violando os princípios de boa-fé e
equidade nas relações de consumo (Gotlib, 2016). O Código de Defesa do Consumidor
[CDC], instituído pela Lei nº 8.078 de 1990 e atualizado pela Lei nº 14.181/2021, estabelece
normas para proteger o consumidor, reconhecendo sua vulnerabilidade e prevendo
mecanismos para combater essas práticas, como a nulidade de cláusulas abusivas e a
possibilidade de reparação por danos morais e materiais.
         Um obstáculo para garantir esse direito é a barreira linguística imposta pela
linguagem jurídica técnica, frequentemente caracterizada por termos arcaicos e expressões
em Latim dificultando a compreensão das leis e processos judiciais pelo público leigo, o que
reforça desigualdades e afasta o cidadão comum do acesso efetivo à justiça. Esse tipo de
linguagem perpetua um sistema judiciário inacessível e mantém estruturas de exclusão que
contrariam os princípios constitucionais de igualdade e participação democrática (Pena,
2020).
         No contexto atual, onde a tecnologia desempenha um papel crescente na
disseminação de informações e prestação de serviços, o uso de "chatbots" nas interações
entre empresas e consumidores tornou-se comum. No entanto, uma pesquisa realizada pelo
Procon-SP, em outubro de 2023, mostrou que, embora 82,20% dos consumidores
entrevistados já tenham interagido com "chatbots" durante compras "online", mais da
metade (54,48%) ainda sente a necessidade de buscar atendimento humano, indicando
insatisfação com a capacidade da inteligência artificial em resolver problemas de maneira
autônoma. Além disso, 42,98% dos entrevistados relataram que, em algumas situações,
precisam recorrer ao suporte humano, evidenciando que os "chatbots", embora populares,
frequentemente falham em oferecer soluções completas e eficazes.
         Diante disso, o projeto Defensor.IA surge na interseção entre direito e inteligência
artificial [IA], propondo o desenvolvimento de um "chatbot" especializado em oferecer
orientações      sobre      direito   do    consumidor,        cobranças   abusivas   e   prevenção   ao
endividamento, disponibilizando informações de maneira simples e descomplicada. Para
isso, será utilizada uma abordagem sem código ("no-code"), em que não há uso de código
escrito manualmente em linguagem de programação textual, permitindo que indivíduos com
pouca ou nenhuma experiência em programação desenvolvam soluções e automações
utilizando ferramentas visuais ou interfaces baseadas em fluxos de trabalho. Essa

```
                                                                                                   3
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

abordagem facilita a implementação de tarefas de processamento de linguagem natural ou
"natural language processing" [NLP] de forma mais eficiente (Hirzel, 2022).
         Na construção do Defensor.IA, o uso de "Large Language Models" [LLMs] permite
interpretar e gerar respostas a partir de grandes volumes de dados jurídicos. No entanto,
esses modelos enfrentam desafios, como a possibilidade de gerar informações imprecisas
ou alucinações. A integração com "Retrieval-Augmented Generation" [RAG] combina
recuperação de dados externos com geração de respostas por modelos de linguagem,
permitindo maior precisão e contexto atualizado, o que ajuda a evitar respostas incorretas e
limitações de conhecimento (Fan et al., 2024).
         A relevância acadêmica do projeto é multifacetada, abrangendo aspectos sociais,
tecnológicos e econômicos. No campo social, a pesquisa busca ampliar o acesso à
informação jurídica, empoderando consumidores ao fornecer orientações claras sobre seus
direitos e deveres. Em termos tecnológicos, o projeto pretende colaborar para os avanços
entre [IA] e direito, desenvolvendo soluções mais eficientes e acessíveis. Ao abordar
questões urgentes, como o superendividamento e as práticas abusivas, o Defensor.IA
alinha-se a temas econômicos e sociais fundamentais, promovendo a justiça, a inclusão e
fortalecendo um mercado de crédito mais justo e responsável.
         O problema central abordado por esta pesquisa é: Como desenvolver um “chatbot”
jurídico especializado, utilizando uma interface visual, sem necessidade de codificação, para
oferecer suporte informativo, confiável e contextualizado sobre direitos do consumidor,
endividamento e práticas abusivas?
         Os objetivos deste trabalho incluem: i) desenvolver o Defensor.IA, um "chatbot"
jurídico especializado, utilizando a arquitetura do Chatling para fornecer informações de
maneira clara e objetiva sobre direitos do consumidor, endividamento e práticas abusivas; ii)
detalhar o fluxo de trabalho e explicar os componentes utilizados bem como as
configurações realizadas para seu funcionamento; iii) comparar as respostas geradas pelo
Defensor.IA, destacando a fonte específica da base de conhecimento que fundamenta cada
resposta com o gerado pelo ChatGPT-4o-mini. Por fim, a metodologia, os processos de
desenvolvimento         e    os    resultados      obtidos      serão   documentados   detalhadamente,
assegurando a transparência e a replicabilidade do estudo.
         Assim, o Defensor.IA busca não apenas contribuir para a simplificação das
informações sobre direito do consumidor, mas também avançar o conhecimento sobre a
aplicação da [IA] no campo jurídico, explorando formas de simplificar o desenvolvimento de
sistemas complexos de [NLP] e adaptá-los eficientemente às mais diversas áreas do
conhecimento jurídico.

```
                                                                                                 4
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Material e Métodos

```
     Para o desenvolvimento do projeto Defensor.IA, utilizou-se o Chatling, uma
```

ferramenta visual destinada à construção de "chatbots" que permite a criação de fluxos de
conversação complexos de forma intuitiva e sem programação avançada. Após o "login" e
criação do projeto, a interface inicial do Chatling é exibida (Figura 1), onde estão disponíveis
diversas funcionalidades para configuração e gerenciamento do "chatbot". Nos próximos
tópicos deste capítulo, serão detalhadas as principais funcionalidades dessa interface que
foram utilizadas no desenvolvimento do Defensor.IA.

Figura 1. Interface inicial do Chatling após o "login" e criação do projeto, mostrando o painel
principal de controle e as opções de funcionalidades, como Builder e Knowledge Base, que
foram relevantes para o desenvolvimento do Defensor.IA.
Fonte: Dados originais da pesquisa

```
     Interface "Chatbot Builder"


     Observa-se na interface, a Área de Trabalho ("Canvas"), espaço central onde se
```

adicionam e conectam blocos para estruturar a lógica do chatbot. A barra lateral ("Sidebar")
oferece opções para adicionar novos blocos, definir variáveis e configurar respostas da IA.
Nessa barra, o usuário encontra elementos essenciais como blocos de texto, captação de
resposta, variáveis e lógica condicional.

```
                                                                                          5
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
       Por fim, a barra de ferramentas ("Toolbar") oferece controles para salvar, visualizar
```

e publicar o “chatbot”, permitindo ajustes e testes. Cada componente permite configurar uma
funcionalidade específica, como saudações, coleta de dados do usuário ou respostas
dinâmicas. A estrutura modular facilita a criação e o ajuste, tornando-o uma ferramenta
poderosa para fluxos conversacionais dinâmicos e eficazes.

```
     Configuração da Base de Conhecimento do Defensor.IA


     A configuração da base de conhecimento ("knowledge base") do Defensor.IA
```

envolveu a definição de quatro fontes de dados que servem como principais referências para
o "chatbot" fornecer respostas detalhadas e juridicamente fundamentadas. Essa etapa
incluiu a seleção dos componentes, a inserção dos dados e o processamento das
informações, garantindo que tudo estivesse disponível de forma estruturada (Figura 2).

Figura 2. Interface da base de conhecimento do Defensor.IA no Chatling, mostrando as
fontes de dados carregadas
Fonte: Dados originais da pesquisa

```
     Os componentes utilizados para configurar a base de conhecimento foram "website"
```

e documentos. Na categoria "website" foi fornecido o link do site do governo onde consta o
[CDC], o "crawler" percorreu o site e coletou as informações relevantes. O conteúdo das
páginas foi extraído e convertido em texto bruto, pronto para ser indexado e classificado, de

```
                                                                                          6
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

modo que pudesse ser facilmente acessado pela IA do "chatbot", proporcionando respostas
rápidas e precisas baseadas nas informações legais disponíveis.
         Na categoria "documents", foram carregados os seguintes documentos:            "O
advogado devedor" e "Defenda-se: guia prático de orientações e modelos de petições",
ambas de autoria do Dr. Ronaldo Gotlib, que disponibilizou suas obras em formato “pdf” para
serem      inseridas na base de conhecimento. Também foi inserido o documento
"Endividamento de risco no brasil" do Banco Central do Brasil [BCB]. Esses documentos
foram fundamentais para fornecer ao Defensor.IA informações que ajudem consumidores a
entenderem seus direitos e tomarem medidas legais diante de práticas prejudiciais.
         A etapa de processamento de dados no Chatling ocorre automaticamente após a
adição de URLs, documentos ou outras fontes à base de conhecimento. Embora a
documentação oficial não mencione diretamente as técnicas utilizadas, destaca que o
conteúdo é organizado de forma a ser pesquisável. Esse processo de organização reflete os
princípios das plataformas "Low-Code e No-Code" [LCNC], que visam facilitar a manipulação
de dados complexos.
         Em sistemas [LCNC], técnicas como tokenização e "embeddings" desempenham um
papel crucial. A tokenização divide o texto em pequenas unidades chamadas "tokens", como
palavras e frases, o que facilita a análise e permite estruturar o conteúdo para o
processamento subsequente. Os "embeddings", por sua vez, convertem esses "tokens" em
vetores matemáticos, capturando relações semânticas entre palavras e frases. Isso significa
que o texto é transformado em um formato numérico que os [“LLMs”] podem usar para
identificar contextos e similaridades (Hyun, 2019). No Chatling, essas técnicas permitiram
que o sistema compreenda o conteúdo de maneira mais profunda, reconhecendo padrões e
conexões, o que é essencial para gerar respostas contextualizadas e relevantes para o
usuário.

```
     Fluxo de trabalho do Defensor.IA


     O fluxo começa com o bloco “start”, que é o ponto de entrada da conversa. A partir
```

desse bloco inicial, foi inserido o bloco de envio de mensagem em formato texto,
denominado apresentação, onde o "chatbot" se apresenta e explica que está disponível para
esclarecer dúvidas sobre direito do consumidor.
         Em seguida, foi solicitado o nome do usuário por meio de um campo configurado
com o recurso "Form (Capture Response)", que permite capturar e armazenar a entrada do
usuário na variável nome_usuario. Com essa configuração, o nome é usado em interações
futuras para criar uma experiência personalizada e envolvente. A opção "required",

```
                                                                                      7
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

requisitado está ativa, garantindo que o usuário preencha o campo antes de prosseguir, o
que estabelece um tom de comunicação amigável e pessoal desde o início (Figura 3).

Figura 3. Bloco Apresentação do fluxo do Defensor.IA, onde o “chatbot” se apresenta e
solicita o nome do usuário, armazenando-o na variável nome_usuario. Esse campo foi
configurado para ser obrigatório e permite que o “chatbot” personalize interações futuras,
criando uma comunicação mais próxima e amigável
Fonte: Dados originais da pesquisa

```
     O próximo bloco adicionado foi denominado saudação personalizada, dando
```

continuidade à interação após capturar o nome do usuário. Com base na informação
armazenada na variável nome_usuario, o “chatbot” se dirige ao usuário pelo nome, dizendo:
“Olá, [nome_usuario], como eu posso te ajudar?”. Esse bloco é configurado como "Text
(Send Message)", texto (envio de mensagem), o que permitiu a inserção de uma mensagem
personalizada, criando um vínculo mais próximo e facilitando a interação (Figura 4).

Figura 4. Bloco Saudação personalizada configurado para utilizar o nome do usuário
capturado anteriormente, e colocar-se à disposição para responder a dúvida do usuário.
Fonte: Dados originais da pesquisa

```
                                                                                     8
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     No bloco “Resposta Defensor.IA,” a configuração foi dividida em duas partes.
```

Primeiro, utilizou-se o componente "Capture Text" para registrar a pergunta do usuário,
armazenando-a na variável {pergunta_usuario}. Este componente garantiu que o “chatbot”
recebesse e processasse a dúvida antes de prosseguir. Em seguida, o componente "[AI]
Response" foi configurado para utilizar a base de conhecimento como fonte de respostas,
acessando a variável capturada. O modelo GPT-4o-mini foi escolhido para garantir
respostas de alta qualidade em português, com a temperatura ajustada para utilizar as
configurações globais. A temperatura, nesse contexto, define o nível de aleatoriedade nas
respostas geradas. Uma temperatura mais alta promove maior criatividade, enquanto uma
mais baixa resulta em respostas mais precisas e consistentes (Chatling, 2024). A escolha
das configurações globais de temperatura assegura que as respostas sejam balanceadas,
mantendo um alto nível de coerência e qualidade. (Figura 5).

Figura 5. Fluxo de iteração do Defensor.IA e as configurações realizadas no componente
"[AI] Response". O fluxo começa com a saudação personalizada ao usuário, seguida pela
captura da primeira pergunta, que é processada e respondida pelo modelo utilizando a base
de conhecimento configurada.
Fonte: Dados originais da pesquisa

```
     No campo "[AI] Configuration", foram realizadas configurações específicas para
```

adaptar o comportamento do Defensor.IA às necessidades do projeto. Primeiramente, em
instruções "instructions" (Figura 6), foram definidas diretrizes para garantir que o "chatbot"
utilizasse uma linguagem acessível, evitando jargões jurídicos, e respondesse sempre em
português. A configuração da base de conhecimento ("knowledge base") orientou o

```
                                                                                         9
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

"chatbot" a se basear exclusivamente no conteúdo legal pré-carregado, garantindo
respostas      juridicamente       fundamentadas.          Por       fim,   na   seção   ajustes   ("settings"),
selecionou-se o modelo GPT-4o, ajustando o idioma para português e definindo a
temperatura da [IA] para zero, assegurando um tom consistente e informativo nas respostas.

Figura 6. Configurações de instruções para [IA], detalhando orientações para o "chatbot",
como o uso de linguagem acessível, o foco em conteúdos da base de conhecimento, e a
inclusão de exemplos práticos para facilitar o entendimento do usuário
Fonte: Dados originais da pesquisa

```
     Após a configuração inicial do Defensor.IA, a interface do "chatbot" foi exibida para
```

interação com o usuário. Esta interface, como mostrado na Figura 7, permitiu que o
consumidor inserisse seu nome e fosse prontamente atendido pelo Defensor.IA, que se
apresentou e ofereceu esclarecimentos sobre direitos do consumidor de forma amigável e
acessível. Essa etapa inicial de apresentação foi fundamental para estabelecer uma
comunicação personalizada e acolhedora, garantindo que o usuário se sentisse à vontade
ao buscar suporte jurídico.

```
                                                                                                         10
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 7. Tela de pré-visualização do Defensor.IA no Chatling, apresentando a saudação
inicial do "chatbot" e solicitando o nome do usuário para personalizar a interação. A interface
permite ao usuário inserir seu nome antes de iniciar a consulta sobre direitos do consumidor
Fonte: Dados originais da pesquisa

```
     Testes


     Para a realização do teste, foram elaboradas perguntas sobre direito do consumidor,
```

práticas abusivas e superendividamento, criando um caso fictício para cada um dos temas.
Esses casos foram concebidos com base em questionamentos comuns de consumidores
encontrados em plataformas como o Reclame Aqui, que é uma fonte amplamente utilizada
pelos consumidores para expor suas queixas e buscar soluções. A criação dos casos
fictícios foi fundamentada em situações reais reportadas por consumidores, garantindo que
as perguntas fossem representativas dos desafios enfrentados no cotidiano dos
consumidores.

```
                                                                                         11
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     Em seguida, essas perguntas foram enviadas ao Defensor.IA, desenvolvido
```

especificamente para tratar de temas relacionados aos direitos do consumidor, e ao modelo
ChatGPT-4o-mini, uma versão reduzida e otimizada do GPT-4. A partir desse procedimento,
foi realizada uma análise comparativa das respostas oferecidas por cada um dos modelos,
buscando identificar diferenças quanto à precisão das informações, clareza, adequação ao
contexto jurídico e efetividade das recomendações sugeridas. As respostas e análises serão
apresentadas a seguir.

Resultados e Discussão

```
     Este capítulo apresenta uma análise detalhada dos resultados obtidos a partir da
```

comparação entre as respostas geradas pelo Defensor.IA e pelo ChatGPT-4o-mini. Cada
tema abordado foi selecionado para evidenciar como os modelos se comportam em relação
à precisão das informações, clareza, adequação ao contexto jurídico e efetividade das
recomendações. A estrutura a seguir facilita a compreensão dos desafios enfrentados pelos
consumidores e a avaliação da eficácia dos modelos em fornecer respostas juridicamente
fundamentadas e aplicáveis.

```
     Direito do consumidor básico

     Na análise das respostas oferecidas pelo Defensor.IA (Figura 8) e pelo GPT-4o-mini
```

(Figura 9), observa-se diferenças significativas em relação à precisão das informações,
clareza, adequação ao contexto jurídico e efetividade das recomendações. Ambas as
respostas apresentam pontos fortes e limitações que se destacam conforme o objetivo e as
necessidades do usuário em questão.
         Pergunta realizada: "Comprei uma televisão nova em uma loja de eletrônicos, mas,
ao instalá-la em casa, percebi que a imagem estava distorcida e havia uma linha preta na
lateral da tela. Voltei à loja no dia seguinte, levando a televisão e a nota fiscal, para pedir a
troca, já que o produto veio com defeito. No entanto, o atendente disse que eu precisaria
primeiro levar a televisão para uma assistência técnica autorizada para obter um laudo que
confirmasse o defeito, antes que a loja pudesse realizar a troca. Expliquei que o problema foi
identificado assim que instalei o produto e que estou dentro do prazo legal de 30 dias para
defeitos aparentes, mas a loja insiste que só posso trocá-lo após obter esse laudo. Isso me
parece injusto, já que paguei por um produto novo e em perfeito estado, e agora estou tendo
dificuldade para obter a troca. Gostaria de entender quais são meus direitos neste caso e o
que posso fazer para resolver a situação. Você pode me ajudar?"

```
                                                                                          12
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 8. Interface do Defensor.IA apresentando os direitos básicos do consumidor
relacionados ao tema da troca de produto com defeito, incluindo citação ao Código de
Defesa do Consumidor [CDC] e recomendação de ações práticas.
Fonte: resultados originais da pesquisa

```
                                                                              13
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 9. Resposta do ChatGPT-4o-mini sobre os direitos básicos do consumidor,
mencionando o artigo 39 do CDC e fornecendo orientações gerais sobre como proceder
diante do problema enfrentado.
Fonte: resultados originais da pesquisa

```
                                                                            14
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     Em termos de precisão das informações, o Defensor.IA destaca-se por sua
```

capacidade de fornecer detalhes precisos e abrangentes sobre os direitos do consumidor no
contexto de um produto com defeito. Ele apresenta alternativas claras baseadas na
legislação, abordando aspectos como substituição do produto, devolução do valor pago e
abatimento proporcional. A inclusão de detalhes legais, como o prazo de 30 dias para
reclamar de defeitos em produtos não duráveis, garante que o usuário compreenda suas
opções de forma bem fundamentada. Já o GPT-4o-mini, embora também ofereça uma
resposta precisa, mantém um nível de detalhamento menor, o que pode deixar o consumidor
com dúvidas adicionais sobre os passos que deve tomar.
         No que se refere à clareza, o Defensor.IA utiliza uma estrutura organizada e
numerada, o que facilita a leitura e compreensão do conteúdo. A divisão em tópicos e a
presença de informações estruturadas por categoria ajudam a direcionar o usuário e tornam
o processo de assimilação mais eficiente. Isso é particularmente útil em situações em que o
consumidor precisa tomar decisões rapidamente. O GPT-4o-mini, por outro lado, apresenta
uma resposta mais direta e menos estruturada, o que pode ser vantajoso para aqueles que
desejam uma resposta rápida e não se preocupam tanto com os detalhes adicionais, mas
pode comprometer a clareza em situações mais complexas.
         No aspecto da adequação ao contexto jurídico, o Defensor.IA proporciona um
respaldo mais completo ao mencionar explicitamente disposições legais relevantes do
Código de Defesa do Consumidor. Ele destaca o direito de o consumidor exigir a troca
imediata de produtos essenciais, como no caso de uma televisão, sem a necessidade de
laudo técnico, o que é um ponto importante de proteção ao consumidor. Já o GPT-4o-mini
oferece informações que são juridicamente corretas, mas não aprofunda na especificidade
dos artigos da lei. Essa falta de detalhamento pode reduzir a confiança do consumidor nas
recomendações apresentadas, especialmente se o usuário precisar justificar seus direitos
para a loja ou terceiros.
         Sobre a efetividade das recomendações, o Defensor.IA apresenta um conjunto de
ações práticas, tais como a documentação dos atendimentos, a realização de uma
reclamação formal e a busca de auxílio do Procon. Essas recomendações são
complementadas com prazos legais e especificações sobre o direito do consumidor, o que
torna o aconselhamento mais efetivo para a resolução do problema. O GPT-4o-mini, embora
também ofereça orientações práticas, como buscar o Procon ou registrar uma reclamação,
não apresenta a mesma riqueza de detalhes. Isso pode limitar a capacidade do consumidor
de agir de forma efetiva e organizada para solucionar a questão.
         O Defensor.IA se mostra mais completo ao fornecer uma resposta juridicamente
embasada, estruturada e detalhada, o que o torna particularmente adequado para usuários

```
                                                                                     15
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

que buscam um entendimento aprofundado de seus direitos e desejam agir de forma
proativa e bem-informada. A abordagem do GPT-4o-mini, por ser mais direta, pode ser útil
para quem busca rapidez, mas corre o risco de deixar lacunas importantes, especialmente
no que tange à aplicação prática das informações legais.

```
     Prática abusiva


     A análise comparativa entre as respostas fornecidas pelo Defensor.IA (Figuras 10) e
```

pelo ChatGPT-4o-mini (Figura 11) para uma situação de prática abusiva por parte de uma
empresa de telecomunicações revela diferenças cruciais na abordagem e na profundidade
das respostas fornecidas..
         Pergunta realizada: "Estou passando por uma situação de abuso com uma empresa
de telecomunicações. Fiz uma reclamação sobre cobranças indevidas e, desde então, tenho
recebido ligações diárias ameaçadoras, dizendo que meu nome será negativado se eu não
pagar. Expliquei várias vezes que estou contestando as cobranças, mas eles continuam me
ligando a cada hora, mesmo depois de eu pedir para pararem. O que posso fazer para me
proteger dessas práticas abusivas?"

```
                                                                                      16
```

  Trabalho de Conclusão de Curso apresentado para obtenção do título
  de especialista em Data Science e Analytics - 2025

Figura 10. Interação entre Defensor.IA sobre um caso fictício para uma situação de prática
abusiva e elaboração de petição inicial para o caso em análise.
Fonte: resultados originais da pesquisa

```
                                                                                    17
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 11. Versão consolidada da resposta do Chatgtp-4o-mini para a mesma pergunta. A
imagem foi editada para apresentar a orientação completa e o modelo de petição em uma
única imagem.
Fonte: resultados originais da pesquisa

```
                                                                               18
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     Em termos de precisão, o Defensor.IA oferece uma resposta mais fundamentada,
```

mencionando diretamente os artigos 42 e 71 do Código de Defesa do Consumidor [CDC],
que proíbem práticas abusivas de cobrança e constrangimento. Isso confere ao usuário uma
base jurídica clara, capacitando-o a tomar decisões informadas. Já o GPT-4o-mini apresenta
orientações práticas, como o registro das ligações e a formalização de reclamações no
Procon ou na ANATEL, mas sem citar leis específicas, o que enfraquece a argumentação
legal.
         Em relação à clareza e estrutura, ambos os modelos são claros, mas o Defensor.IA
se destaca por sua organização mais detalhada. As etapas são explicadas de maneira
sequencial e didática, tornando o processo mais fácil de ser seguido, especialmente para
quem não possui familiaridade com o sistema jurídico. O GPT-4o-mini, embora também
claro, opta por uma abordagem mais simples e direta, sem o mesmo nível de profundidade
nas explicações, o que pode ser insuficiente para usuários que precisam de orientações
mais completas.
         No que tange à adequação jurídica, o Defensor.IA é superior, uma vez que suas
recomendações são sustentadas por dispositivos legais específicos do [CDC]. Isso torna a
resposta mais alinhada ao contexto jurídico brasileiro e oferece ao usuário maior segurança
em suas ações. O GPT-4o-mini, embora útil em termos práticos, não faz menção a
dispositivos legais específicos, o que pode limitar a sua aplicabilidade em situações mais
complexas que exijam embasamento jurídico.
         Quanto à efetividade das recomendações, o Defensor.IA propõe ações práticas e
juridicamente embasadas, sugerindo desde o registro de provas até a consideração de uma
ação judicial por danos morais. O modelo inclui ainda a sugestão de multa diária em caso de
descumprimento, o que aumenta a eficácia da defesa. Já o GPT-4o-mini oferece soluções
imediatas e práticas, como o uso de aplicativos para bloqueio de chamadas, mas não
aborda diretamente a questão legal, o que pode ser insuficiente para resolver o problema de
forma definitiva.
         Quando analisamos as petições, o Defensor.IA continua a se destacar. Sua petição é
formal e bem estruturada, com uma clara divisão entre os fatos, o direito e os pedidos. A
citação de artigos do [CDC] reforça a fundamentação legal, tornando a petição mais
consistente e pronta para ser utilizada em um processo judicial. Além disso, a inclusão de
medidas como a multa diária em caso de descumprimento fortalece a defesa. A petição do
GPT-4o-mini, embora bem estruturada, não menciona dispositivos legais específicos, o que
enfraquece a argumentação jurídica. Além disso, a ausência de pedidos como a multa diária
limita a eficácia da petição, que se mantém mais genérica.

```
                                                                                     19
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     Concluindo, o Defensor.IA apresenta uma solução mais completa e juridicamente
```

fundamentada, tanto em suas recomendações quanto na petição gerada. Ele oferece uma
defesa sólida contra práticas abusivas, citando a legislação aplicável e sugerindo ações
detalhadas que cobrem todas as etapas do processo. O GPT-4o-mini, por sua vez, é uma
alternativa mais simples e prática, mas sua falta de profundidade jurídica e de
fundamentação legal limita sua eficácia em cenários mais complexos.

```
     Superendividamento


     Ao analisar as respostas oferecidas pelo Defensor.IA (Figura 12) e pelo GPT-4o-mini
```

(Figura 13) sobre o tema do superendividamento, várias semelhanças e diferenças
importantes surgem, tanto na abordagem quanto na profundidade das recomendações
fornecidas. A análise foi focada na precisão, clareza e estrutura, adequação jurídica e
efetividade das respostas.
         Pergunta realizada: "Estou enfrentando dificuldades com dívidas. Tenho várias
pendências de cartão de crédito e empréstimos pessoais, e os juros só aumentam. Estou
desempregada e minha renda atual não cobre nem o básico. As empresas de cobrança
continuam me pressionando e oferecendo novas dívidas para ‘cobrir’ as antigas, o que só
piora minha situação. Quais são meus direitos no caso de superendividamento e como
posso renegociar minhas dívidas de forma justa?"

```
                                                                                      20
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 12. Orientações detalhadas sobre superendividamento e baseadas na Lei
14.181/2021, demonstrando conhecimento jurídico aprofundado e assistência relevante ao
consumidor.
Fonte: resultados originais da pesquisa

```
                                                                                21
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 13. Resposta gerada pelo ChatGPT sobre superendividamento, fornecendo
conselhos gerais sobre gestão de dívidas, mas sem fundamentação legal específica.
Fonte: resultados originais da pesquisa

```
                                                                           22
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
       No que diz respeito a precisão, ambas as respostas fornecem informações
```

relevantes e corretas sobre o superendividamento. O Defensor.IA menciona diretamente a
Lei 14.181/2021, conhecida como Lei do Superendividamento, e detalha como essa
legislação oferece proteção ao consumidor, especialmente no que diz respeito à
renegociação justa das dívidas, à proibição de práticas abusivas e à solicitação de um plano
de pagamento que respeite a capacidade financeira do consumidor. Essa abordagem
jurídica mais detalhada do Defensor.IA confere maior precisão à resposta, uma vez que
vincula as orientações diretamente à legislação aplicável. O GPT-4o-mini também menciona
a Lei 14.181/2021, mas de forma menos detalhada, não explorando tanto as especificidades
da legislação. Contudo, ele faz uma referência útil ao Código de Defesa do Consumidor, que
também é relevante em casos de renegociação de dívidas, ainda que não seja o foco
principal quando se trata de superendividamento. A precisão da resposta do GPT-4o-mini é
adequada, mas não tão abrangente quanto à do Defensor.IA no que tange à exploração da
legislação específica.
         Quando se avalia a clareza e estrutura, o Defensor.IA se destaca por organizar as
informações em tópicos sequenciais e bem delineados, o que facilita a compreensão do
usuário. As etapas são apresentadas de forma lógica e progressiva, desde a renegociação
das dívidas até a busca de apoio jurídico, passando por recomendações práticas como
organização financeira e negociação com credores. Além disso, o Defensor.IA oferece um
exemplo prático que ilustra como a Lei 14.181/2021 pode ser aplicada, consolidando
diferentes dívidas em um único plano de pagamento com parcelas compatíveis com a renda
do usuário. Esse exemplo torna a explicação mais acessível e concreta, ajudando o usuário
a visualizar a aplicação da lei em sua própria situação. O GPT-4o-mini, por sua vez, também
utiliza uma estrutura de tópicos que facilita a leitura, mas sua abordagem é um pouco mais
linear e genérica. A organização das etapas, como priorizar dívidas e documentar
negociações, é útil e prática, mas não é tão detalhada ou didática quanto a do Defensor.IA,
especialmente para quem necessita de orientações mais específicas.
         Em relação à adequação jurídica, o Defensor.IA se destaca ao mencionar
explicitamente a Lei 14.181/2021, oferecendo uma base legal sólida para que o consumidor
possa entender seus direitos no âmbito do superendividamento. Essa menção à legislação
específica dá mais segurança ao usuário, pois fica claro que as recomendações estão
respaldadas por uma base legal adequada. Além disso, o Defensor.IA menciona que o
consumidor pode buscar apoio nos órgãos de proteção ao consumidor, ainda que não
mencione especificamente o Procon. O GPT-4o-mini, por outro lado, faz referência direta ao
Procon, o que pode ser útil para usuários que precisam de um direcionamento mais claro
sobre onde buscar suporte. No entanto, a abordagem mais aberta do Defensor.IA permite

```
                                                                                      23
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

que o usuário escolha entre diversas opções de defesa ao consumidor, o que também pode
ser positivo em contextos variados.
         Quanto à efetividade das recomendações, o Defensor.IA apresenta um conjunto de
ações bem estruturadas para lidar com o superendividamento. Ele incentiva o usuário a
organizar suas finanças, negociar com os credores e buscar ajuda jurídica caso não consiga
chegar a um acordo diretamente. Além disso, a recomendação de consolidar dívidas em um
único plano de pagamento é uma solução prática que pode facilitar a vida do consumidor.
No entanto, como mencionado, o Defensor.IA não menciona diretamente o Procon, o que
pode ser visto como uma limitação em termos de fornecimento de recursos práticos
adicionais. Por outro lado, o GPT-4o-mini faz essa menção ao Procon, além de sugerir
consultoria financeira e assistência jurídica, o que amplia o leque de opções de suporte para
o consumidor. As orientações práticas do GPT-4o-mini também são eficazes, mas faltam
detalhes mais aprofundados sobre como essas negociações devem ser formalizadas e
acompanhadas, o que pode comprometer a aplicação das recomendações em cenários
mais complexos.
         Em conclusão, o Defensor.IA oferece uma resposta mais juridicamente embasada e
detalhada, especialmente no que se refere à Lei 14.181/2021. Sua abordagem é mais
completa      para     consumidores         que      enfrentam       situações   de   superendividamento,
proporcionando um caminho claro e estruturado para lidar com as dívidas de forma justa e
equilibrada. Já o GPT-4o-mini, apesar de ser uma ferramenta útil, oferece uma solução mais
genérica e prática, com ênfase em recursos como o Procon e consultorias financeiras, mas
sem o mesmo grau de detalhamento jurídico.

```
     Outra pergunta realizada dentro do mesmo tema: "O que é superendividamento?
```

Quais são as leis que tratam sobre superendividamento e o que fazer para melhorar essa
situação?"
         Observou-se diferenças significativas na forma como cada modelo abordou as
questões,      principalmente        em     relação     à    fundamentação       jurídica   e   clareza   das
recomendações fornecidas (Figura 14 e 15).

```
                                                                                                       24
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 14. Resposta do Defensor.IA sobre superendividamento, incluindo definição
detalhada do conceito e direitos garantidos pela Lei 14.181/2021
Fonte: resultados originais da pesquisa

```
                                                                          25
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Figura 15. Resposta do Chatgpt-4o-mini sobre superendividamento, fornecendo uma
explicação geral sobre o conceito e sugerindo renegociação direta com os credores, sem
mencionar legislação específica
Fonte: resultados originais da pesquisa

```
                                                                                26
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

```
     Ao comparar as respostas oferecidas pelo Defensor.IA e pelo GPT-4o-mini,
```

observa-se diferenças significativas em relação à precisão das informações, clareza,
adequação ao contexto jurídico e efetividade das recomendações. Ambas as respostas
apresentam pontos fortes e limitações que se destacam conforme o objetivo e as
necessidades do usuário em questão.
         Em relação a precisão, ambas as respostas fornecem uma definição correta do
superendividamento, mas com particularidades que distinguem os dois modelos. O
Defensor.IA aborda o superendividamento como um processo estrutural e contínuo que vai
além da inadimplência ocasional, destacando que o problema pode afetar a saúde financeira
e psicológica dos indivíduos. Essa explicação é mais abrangente, pois destaca os impactos
a longo prazo e as influências externas, como o contexto socioeconômico, como a pandemia
de Covid-19, que podem agravar o superendividamento. Em contraste, o GPT-4o-mini
oferece uma definição mais direta e prática, focando na incapacidade de pagar dívidas, sem
se aprofundar tanto nas causas e consequências do fenômeno. A definição mais enxuta do
GPT-4o-mini é útil para uma compreensão rápida, mas pode deixar lacunas em termos de
compreensão dos fatores subjacentes e da gravidade da situação.
         No que diz respeito à clareza e estrutura, o Defensor.IA organiza suas respostas de
maneira clara, delineando aspectos importantes do superendividamento, como a
incapacidade de pagamento, o impacto familiar e a natureza contínua do problema. Essa
divisão facilita a compreensão e fornece uma visão mais completa do tema. Além disso, o
Defensor.IA complementa a explicação com medidas práticas para melhorar a situação,
dividindo essas ações de maneira sequencial e organizada. O GPT-4o-mini também
organiza suas informações em tópicos claros, com uma estrutura simples e objetiva, mas
sem a mesma profundidade na explicação dos impactos do superendividamento. A falta de
uma estrutura mais detalhada sobre os efeitos psicológicos e sociais do problema pode
fazer com que sua explicação pareça menos abrangente.
         Em termos de adequação jurídica, ambos os modelos mencionam a Lei 14.181/2021,
mas a abordagem do Defensor.IA se mostra mais completa ao explicar que essa lei trouxe
mudanças no Código de Defesa do Consumidor e no Estatuto do Idoso para proteger os
superendividados. Ele também destaca pontos-chave da legislação, como a proibição de
práticas abusivas e a exigência de transparência por parte dos credores. O GPT-4o-mini,
embora mencione a mesma lei, não menciona que ela trouxe mudanças para o Código de
Defesa do Consumidor ou para o Estatuto do Idoso. Sua explicação foca mais na
renegociação de dívidas e no direito à informação, mas sem o mesmo grau de detalhamento
sobre a legislação e suas implicações. Nesse aspecto, o Defensor.IA fornece um contexto

```
                                                                                       27
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

jurídico mais relevante, ajudando o usuário a entender melhor os direitos legais e como
utilizá-los.
         No que tange à efetividade das recomendações, ambos os modelos sugerem
medidas práticas para lidar com o superendividamento, como organização das finanças,
elaboração de um orçamento e renegociação de dívidas. No entanto, o Defensor.IA oferece
uma abordagem mais detalhada e organizada, destacando a importância da educação
financeira, planejamento e o papel de profissionais, como advogados ou serviços de
proteção ao consumidor. Essa sequência de passos é clara e prática, proporcionando ao
usuário um caminho estruturado para enfrentar o superendividamento. O GPT-4o-mini, por
sua vez, também fornece recomendações úteis, como a priorização de dívidas e a consulta
a profissionais, mas não oferece o mesmo nível de detalhamento ou estrutura para guiar o
usuário através do processo. A falta de explicações mais detalhadas sobre como essas
etapas devem ser implementadas pode limitar a eficácia das suas recomendações.
         Em síntese, o Defensor.IA oferece uma explicação mais completa e estruturada do
problema, além de medidas práticas mais detalhadas para ajudar o usuário. O GPT-4o-mini,
embora também eficaz, adota uma abordagem mais direta e simples, útil para usuários que
buscam uma explicação rápida e objetiva, mas sem o mesmo nível de profundidade jurídica
e organizacional. Dependendo da complexidade da situação do usuário, o Defensor.IA pode
ser mais adequado para aqueles que necessitam de um suporte mais abrangente, enquanto
o GPT-4o-mini é uma opção válida para quem busca orientações imediatas e diretas.
         Este capítulo encerra-se destacando os motivos pelos quais o Defensor.IA se
mostrou mais eficaz em fornecer respostas juridicamente contextualizadas, principalmente
devido ao uso de "Retrieval-Augmented Generation" [RAG] para a integração de dados
específicos do domínio jurídico. O RAG combina recuperação de documentos com modelos
generativos, o que permite ao Defensor.IA buscar documentos relevantes em uma base de
conhecimento e utilizá-los para gerar respostas mais precisas e contextualmente
adequadas.
         Segundo Magesh et al. (2024), a utilização de modelos baseados em RAG contribui
significativamente para minimizar problemas de alucinação e aumentar a precisão das
respostas, o que melhora a confiança do usuário nas informações fornecidas. No contexto
jurídico, é especialmente valioso por sua capacidade de reduzir alucinações (respostas
imprecisas), uma vez que fundamenta suas respostas em documentos legais reais, como
jurisprudência ou legislação. Essa abordagem diminui o risco de o modelo gerar respostas
incorretas ou enganosas, o que é crucial na prática jurídica, onde informações imprecisas
podem ter consequências significativas. Assim, oferece uma maneira mais segura e

```
                                                                                        28
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

confiável de aplicar IA no direito, ajudando a evitar erros e a fornecer informações
atualizadas e juridicamente corretas.

Considerações Finais

```
     O presente trabalho apresentou o desenvolvimento do Defensor.IA, um "chatbot"
```

voltado para a orientação jurídica no contexto do direito do consumidor, com foco na
prevenção do superendividamento e na identificação de práticas abusivas. A abordagem
"no-code" permitiu a criação do "chatbot" por meio de ferramentas visuais, sem a
necessidade de codificação manual, facilitando o desenvolvimento. A integração com
modelos de linguagem, como o GPT-4o, possibilitou a geração de respostas claras e
fundamentadas juridicamente.
         Os resultados indicaram que o Defensor.IA é eficaz em fornecer respostas precisas,
contextualizadas e adequadas ao direito do consumidor, superando o ChatGPT-4o-mini em
diversos aspectos. O uso do "Retrieval-Augmented Generation" [RAG] foi um diferencial
importante, garantindo a utilização de informações atualizadas e juridicamente embasadas,
minimizando problemas de alucinação.
         Conclui-se que o Defensor.IA contribui para a simplificação do acesso à informação
jurídica, oferecendo suporte acessível e eficaz para consumidores em situação de
vulnerabilidade. A aplicação de inteligência artificial no campo jurídico demonstrou ser viável
de forma ética, responsável e com grande potencial de impacto social positivo.
         Assim, o trabalho atingiu seus objetivos, comprovando a viabilidade de desenvolver
soluções tecnológicas eficientes que facilitam a compreensão e o acesso ao direito do
consumidor, promovendo maior inclusão e equidade no acesso à justiça.

Referências

BRASIL. Lei nº 8.078, de 11 de setembro de 1990. Código de Defesa do Consumidor.
Disponível em: [https://www.planalto.gov.br/ccivil_03/leis/l8078.htm](https://www.planalto.gov.br/ccivil_03/leis/l8078.htm). Acesso em: 04 maio
2024.

CHATLING. 2024. Set AI Model. Disponível em: [https://docs.chatling.ai/ai/set-ai-model](https://docs.chatling.ai/ai/set-ai-model).
Acesso em: 21 set. 2024.

FAN, W.; DING, Y.; NING, L.; WANG, S.; LI, H.; YIN, D.; CHUA, T. S.; LI, Q. 2024. A survey
on rag meeting llms: Towards retrieval-augmented large language models. In: Proceedings of
the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, p. 6491-6501.
Disponível em: [https://arxiv.org/abs/2405.06211](https://arxiv.org/abs/2405.06211). Acesso em: 15 jul. 2024.

FUNDAÇÃO PROCON-SP. 2023. Relatório técnico da pesquisa comportamental
“Inteligência Artificial no Atendimento ao Consumidor”. São Paulo: EPDC - Escola de

```
                                                                                        29
```

Trabalho de Conclusão de Curso apresentado para obtenção do título
de especialista em Data Science e Analytics - 2025

Proteção e Defesa do Consumidor. Disponível em:
[https://www.procon.sp.gov.br/wp-content/uploads/2023/10/RELAT_PESQ_COMP_IA_2023.p](https://www.procon.sp.gov.br/wp-content/uploads/2023/10/RELAT_PESQ_COMP_IA_2023.p)
df. Acesso em: 17 set. 2024.

GOTLIB, R. 2016. Financeiramente Feliz: Como superar as dificuldades, enfrentar a
indústria da cobrança, sair do sufoco das dívidas e fazer sua vida prosperar. Editora Gotlib,
Rio de Janeiro, RJ, Brasil. Produção de ebook: S2 Books.

HIRZEL, M. 2023. Low-code programming models. Communications of the ACM, v. 66, n.
10, p. 76-85. Disponível em: [https://arxiv.org/abs/2205.02282](https://arxiv.org/abs/2205.02282). Acesso em: 05 mai. 2024.

HYUN, C. Y. 2019. Design and Implementation of a Low-Code/No-Code System.
International Journal of Advanced Smart Convergence, v. 8, n. 4, p. 188-193. Disponível em:
[https://doi.org/10.7236/IJASC.2019.8.4.188](https://doi.org/10.7236/IJASC.2019.8.4.188). Acesso em: 10 mai. 2024.

MACHADO, R. 2024. Superendividamento: a tutela do mínimo existencial à luz do direito
civil-constitucional. 1. ed. Processo. E-book. Disponível em:
[https://middleware-bv.am4.com.br/SSO/pecege/9786553781375](https://middleware-bv.am4.com.br/SSO/pecege/9786553781375). Acesso em: 20 jun. 2024.

PENA, T. M. G. 2020. A simplificação da linguagem jurídica como fator de democratização
do direito e inclusão social. Revista do Tribunal Regional do Trabalho da 24. Região, n. 5, p.
109-129. Disponível em: [https://juslaboris.tst.jus.br/handle/20.500.12178/185567](https://juslaboris.tst.jus.br/handle/20.500.12178/185567). Acesso
em: 05 abr. 2024.

PESQUISA NACIONAL DE ENDIVIDAMENTO E INADIMPLÊNCIA DO CONSUMIDOR
[PEIC]. 2024. Relatório de julho de 2024. Confederação Nacional do Comércio de Bens,
Serviços e Turismo. Disponível em:
[https://portal-bucket.azureedge.net/wp-content/2024/07/Analise_Peic_julho_2024.pdf](https://portal-bucket.azureedge.net/wp-content/2024/07/Analise_Peic_julho_2024.pdf).
Acesso em: 16 ago. 2024.

```
                                                                                        30
```

