# Slides da apresentação – modelo “nota 10” (referência Isabella)

Guia para montar o PowerPoint no **mesmo espírito** da apresentação de referência: faixa azul no título, rodapé com **número do slide** + logo **MBA USP ESALQ**, corpo **leve em texto** e **forte em imagem/diagrama**, uma **frase de rodapé** com o “takeaway” quando fizer sentido.

**Seu tema:** priorização de backlog em app bancário a partir de avaliações da loja, com grafo temporal e IA.

---

## Slide 1 – Capa


| Elemento           | Conteúdo sugerido                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| Fundo              | Azul institucional (como a referência)                                                                |
| Título             | Priorização de backlog em apps bancários: feedback da loja, grafo de conhecimento e IA                |
| Subtítulo opcional | Uma linha humana: *Organizar a voz do usuário para decidir o que corrigir primeiro*                   |
| Créditos           | **Aluna:** Simone Rossetti Nobre Naxara · **Orientadora:** Dra. Anna Carolina Martins · MBA USP/ESALQ |
| Rodapé             | Slide **1** · logo MBA                                                                                |


**Fala (20 s):** Apresentar nome, tema e que o foco é **qualidade além da esteira**, com dados reais de produção (loja de app).

---

## Slide 2 – Contexto geral *(espelha “Contexto geral” da Isabella: dado + conceito)*


| Lado         | Conteúdo                                                                                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Esquerda** | Pequena **tabela ou destaque numérico**: FEBRABAN – mobile banking **>75%** das transações (2025). Opcional: uma linha sobre impacto de falha (confiança, continuidade). |
| **Direita**  | **Diagrama simples** (3 caixas): *Canal digital* → *Expectativa do cliente* → *Qualidade como risco de negócio*. Ícones: celular, pessoa, escudo/check.                  |


**Takeaway rodapé:** *No Brasil, app bancário é canal principal; qualidade mal endereçada vira risco.*

---

## Slide 3 – Problema *(espelha slide “Problema”: causa + evidência)*


| Lado         | Conteúdo                                                                                                                                                                                                 |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Esquerda** | **Dois círculos ou setas:** *Testes na esteira* vs *Produção real* – no meio: *lacuna* (dispositivos, rede, versões, uso imprevisível). Ou: *Nota 1–5* vs *Texto rico* – no meio: *decisão superficial*. |
| **Direita**  | **Um gráfico simples** (barras ou ícones com percentuais do seu texto): ex. volume de avaliações no recorte; ou **3 dores típicas** em caixas: performance, autenticação, Pix – *sem* parágrafo longo.   |


**Takeaway rodapé:** *A loja é termômetro em produção, mas o texto precisa virar priorização acionável.*

---

## Slide 4 – Solução proposta *(espelha “Solução proposta”: pilares → produto)*

**Layout:** Da esquerda para a direita, **6 “pilares”** (ícone + palavra curta) convergindo para o **resultado**.

Sugestão de pilares (adaptáveis):

1. **Avaliações da loja** (ícone: estrela/comentário)
2. **Polaridade** (ícone: nuvem de sentimento) – BERTweet
3. **Extração de problemas** (ícone: etiqueta) – GPT-4o
4. **Grafo temporal** (ícone: rede) – Neo4j
5. **Capacidades de negócio** (ícone: organograma leve) – 15 *BusinessCapabilities*
6. **Documento de priorização** (ícone: lista priorizada)

**Centro/direita:** Nome do “produto do TCC” em uma caixa – ex. **Priorização orientada a evidência** ou **Backlog a partir da voz do usuário** (sem precisar ser marca registrada).

**Takeaway rodapé:** *Feedback público vira estrutura ligada a versão e à área do negócio.*

---

## Slide 5 – Ferramentas e stack *(espelha “Ferramenta utilizada”)*


| Lado         | Conteúdo                                                                                                                                                           |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Esquerda** | **Imagem:** logos limpos (Python, Hugging Face, Neo4j, OpenAI) **ou** recorte da **Figura 1** (pipeline) do TCC.                                                   |
| **Direita**  | 3–4 linhas: *Duas etapas – classificação com Transformer; extração estruturada com LLM; persistência em grafo; saída para priorização.* Evite lista de parâmetros. |


**Takeaway rodapé:** *Arquitetura híbrida: o que é barato roda primeiro; o que é fino roda só no que importa.*

---

## Slide 6 – Dados *(espelha “Base de conhecimento para RAG” – no seu caso: fonte de dados)*


| Conteúdo                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Print estilizado ou **mockup** de loja (Google Play) + app **CAIXA**.                                                                               |
| Caixas: **2.451** avaliações no arquivo; recorte **5–18 jan. 2026**; **100** negativas representativas após triagem para o experimento de extração. |
| Uma linha: *Dados públicos; sem conteúdo sigiloso da instituição.*                                                                                  |


**Takeaway rodapé:** *Base real de produção, com recorte explícito para o estudo.*

---

## Slide 7 – Fluxo de trabalho *(espelha fluxo visual no-code – aqui: seu pipeline)*

**Imagem principal:** **Figura 1** do TCC (pipeline completo), em boa resolução.

**Legenda curta (opcional na lateral):** Coleta → polaridade → filtro → GPT-4o + reflexão → grafo → métricas / priorização.

**Takeaway rodapé:** *Do comentário bruto ao vínculo versão–problema–capacidade.*

---

## Slide 8 – Cenários de teste e validações *(espelha “Cenários de testes e validações”)*

**Topo:** Fluxo simples: *Comentários* → *Anotação dupla / “gold”* → *Métricas de classificação* · *Validação manual da extração*.

**Base:** **Balança ou duas colunas:**  

- **Esquerda:** BERTweet (melhor para português informal)  
- **Direita:** DistilBERT multilíngue  
Critérios em ícones: **Acurácia** · **F1** · **ROC AUC** (não precisa dos números no slide; você fala).

Opcional: segunda linha com *Escolha do GPT-4o* após comparar modelos (sua Figura 3 no TCC).

**Takeaway rodapé:** *Validação em duas frentes: polaridade e mapeamento para capacidade de negócio.*

---

## Slide 9 – Resultados: polaridade *(espelha slide de resultados comparativos)*

**Layout:** Duas imagens lado a lado – **Figura 4** (métricas) e trecho da **Figura 5** (matrizes), ou só uma composta.

**Rodapé (frase):** *BERTweet ~96% acurácia no conjunto de referência – triagem confiável para o restante do fluxo.*

---

## Slide 10 – Resultados: escolha do modelo de extração

**Imagem:** **Figura 3** (comparação GPT – painéis A e B).

**Rodapé:** *GPT-4o equilibrou acerto e custo; mapeamento refinado na validação manual.*

---

## Slide 11 – Resultados: estrutura do grafo e achado 91 × 85

**Imagem:** **Figura 2** (`fig2_fluxo_grafo.png`) – fluxo App → Versão → Episódio → Issue → Capacidade.

**Caixa de destaque (grande, legível):** **91 vínculos** · **85 issues** · *79 com uma capacidade + 6 com duas* → *problemas que **cruzam** frentes (ex.: senha ↔ autenticação e segurança).*

**Rodapé:** *O “extra” de ligações não é erro: é a transversalidade típica do app bancário aparecendo no modelo.*

---

## Slide 12 – Resultados: o que pesa no negócio

**Imagem:** **Figura 6** ou **Figura 7** (distribuição por capacidade / top issues).

**Rodapé:** *Performance e estabilidade ~23,5% das issues – alinhado ao que o cliente mais enxerga.*

---

## Slide 13 – Discussão dos resultados *(espelha tabela da Isabella)*

**Tabela 4 colunas** (linhas curtas):


| Foco             | O que o trabalho mostra             | Limitação honesta                            | Mensagem para gestão                                        |
| ---------------- | ----------------------------------- | -------------------------------------------- | ----------------------------------------------------------- |
| Transversalidade | 91 vs 85; senha em duas capacidades | Amostra de 100 comentários                   | Priorizar com **coordenação** entre áreas, não só “um dono” |
| Mapeamento       | ~63,6% acurácia após refinamento    | Linguagem informal / gírias                  | Base para backlog; evolui com dicionário e validação        |
| Polaridade       | Alta acurácia BERTweet              | Não substitui análise humana em caso crítico | Triagem para não perder reclamação séria                    |


**Rodapé:** *Ciência com pé no chão: números úteis, com ressalvas explícitas.*

---

## Slide 14 – Conclusão *(espelha ícone + parágrafo curto)*

Seis frases máximas (como a referência), cada uma com **um ícone**:

1. **Produção importa** – complemento aos testes de esteira.
2. **Texto da loja** – insumo estruturado, não só nota.
3. **Grafo temporal** – versão, problema e capacidade no mesmo quadro.
4. **Transversalidade** – o modelo **deixa visível** quando uma queixa puxa mais de uma área.
5. **Gestão de qualidade** – linguagem comum para produto, engenharia e QA.
6. **Próximos passos** – ampliar amostra; validar com negócio; integração futura com defeitos internos (sob governança).

---

## Slide 15 – Referências *(espelha slide enxuto)*

4–7 referências **só as âncoras** (FEBRABAN, ISTQB, um artigo de grafo/PLN, Fávero & Belfiore, etc.). Texto pequeno; o resto fica no TCC escrito.

---

## Slide 16 – Encerramento


| Elemento | Conteúdo                                        |
| -------- | ----------------------------------------------- |
| Fundo    | Azul                                            |
| Centro   | **OBRIGADA** + ícone simples (ou só tipografia) |
| Abaixo   | Aluna e orientadora                             |
| Rodapé   | **16** · logo MBA                               |


---

## Dicas rápidas (para chegar perto da nota 10)

1. **Nunca** um slide só com parágrafo longo – se precisar de texto, quebre em **duas colunas** ou **ícones**.
2. **Um slide = uma ideia**; o detalhe técnico fica para a **pergunta da banca**.
3. **Frase de rodapé** nos resultados: a banca lembra o que você quer que ela leve para casa.
4. Ensaiar **91 e 85** em **15 segundos** (conta 79 + 6×2).
5. Manter **Figura 2** e **Figura 1** em alta resolução; contraste bom para projetor.

---

*Este arquivo é um roteiro de **estrutura visual**; o roteiro falado detalhado continua em `APRESENTACAO_TCC_20min.md`.*