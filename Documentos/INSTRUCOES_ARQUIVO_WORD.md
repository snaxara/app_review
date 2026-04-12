# Instruções - Arquivo Word Formatado USP/ESALQ

## Arquivo Gerado

O arquivo `TCC_FORMATADO_USP_ESALQ.docx` foi gerado automaticamente a partir do documento Markdown, com formatação conforme normas USP/ESALQ.

## Formatação Aplicada

✅ **Fonte**: Times New Roman 12pt  
✅ **Espaçamento**: 1,5 entre linhas  
✅ **Margens**: 3cm superior/inferior, 2cm esquerda/direita  
✅ **Numeração de páginas**: No rodapé, centralizada  
✅ **Títulos de seção**: Formatados em negrito, alinhados à esquerda  
✅ **Subtítulos**: Formatados em negrito, alinhados à esquerda  

## Ajustes Necessários no Word

### 1. Inserir Imagens

As imagens precisam ser inseridas manualmente. Os locais estão marcados com `[IMAGEM A SER INSERIDA]`.

**Para cada imagem:**
1. Localize o marcador `[IMAGEM A SER INSERIDA]`
2. Delete o texto do marcador
3. Insira a imagem através de: Inserir > Imagens > Este Dispositivo
4. Centralize a imagem
5. Ajuste o tamanho se necessário

**Imagens a inserir:**
- Figura 1: Pipeline de processamento (`imagens_tcc/pipeline_processamento.png`)
- Figura 2: Comparação de modelos de polarização (`imagens_tcc/comparacao_modelos_sentimentos.png`)
- Figura 3: Matrizes de confusão (`imagens_tcc/matriz_confusao_sentimentos.png`)
- Figura 4: Comparação de modelos GPT (`imagens_tcc/comparacao_modelos_gpt.png`)
- Figura 5: Distribuição de Issues (`imagens_tcc/distribuicao_issues_capabilities.png`)
- Figura 6: Top 10 Issues (`imagens_tcc/top_10_issues.png`)
- Figura 7: Distribuição por nível/tipo/valor (`imagens_tcc/distribuicao_nivel_tipo_valor.png`)
- Figura 8: Degree Centrality (`imagens_tcc/sna_degree_centrality.png`)
- Figura 9: Métricas SNA combinadas (`imagens_tcc/sna_metricas_combinadas.png`)

### 2. Ajustar Formatação de Tabelas

As tabelas foram geradas com estilo "Table Grid". Conforme as normas USP/ESALQ:

**Tabelas devem ter:**
- ✅ Título acima da tabela (já formatado)
- ✅ Fonte abaixo da tabela (já formatada)
- ⚠️ **Ajustar bordas**: Remover bordas laterais (esquerda e direita), mantendo apenas superior e inferior

**Para ajustar cada tabela:**
1. Clique na tabela
2. Vá em: Design de Tabela > Bordas > Opções de Bordas
3. Remova as bordas esquerda e direita
4. Mantenha apenas as bordas superior e inferior

### 3. Verificar Quadros

Os quadros (como a estrutura do Knowledge Graph) foram formatados com bordas em todos os lados. Verifique se está conforme suas preferências.

### 4. Verificar Referências

As referências foram mantidas conforme o formato do documento original. Verifique se estão em ordem alfabética e formato correto.

### 5. Verificar Numeração

A numeração de páginas foi adicionada automaticamente no rodapé. Verifique se está funcionando corretamente.

## Regerar o Arquivo

Para regerar o arquivo Word após alterações no Markdown:

```bash
python scripts/gerar_word_tcc.py
```

O arquivo será gerado em: `Documentos/TCC_FORMATADO_USP_ESALQ.docx`

## Observações

- O script preserva a estrutura do documento original
- Formatação markdown (negrito, itálico) foi convertida para formatação Word
- Listas foram convertidas para listas formatadas do Word
- Tabelas foram convertidas para tabelas do Word
- Código/quadros foram formatados com fonte monoespaçada e bordas

## Próximos Passos

1. Abrir o arquivo Word gerado
2. Inserir todas as imagens nos locais marcados
3. Ajustar formatação das tabelas (remover bordas laterais)
4. Revisar formatação geral
5. Verificar numeração de páginas
6. Fazer revisão final do conteúdo
