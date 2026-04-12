// ============================================================
// QUERY: ENTIDADES E SUAS BUSINESS CAPABILITIES ASSOCIADAS
// Retorna tabela com entidades e suas capacidades de negócio
// ============================================================

// 1. QUERY BÁSICA: Entidades e suas BusinessCapability
MATCH (e)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WHERE 'Issue' IN labels(e)
RETURN 
    e.name AS Entidade,
    labels(e) AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS Nivel,
    bc.capability_type AS TipoCapacidade,
    bc.business_value AS ValorNegocio,
    r.t_valid AS DataValidade,
    r.sentiment AS Sentimento,
    count(r) AS TotalRelacionamentos
ORDER BY bc.name, e.name

// ============================================================
// 2. QUERY DETALHADA: Com contagem de episódios relacionados
// ============================================================
MATCH (e)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
OPTIONAL MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
WHERE 'Issue' IN labels(e)
WITH e, bc, r, count(DISTINCT ep) AS total_episodios
RETURN 
    e.name AS Entidade,
    labels(e) AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS Nivel,
    total_episodios AS TotalEpisodios,
    r.sentiment AS Sentimento,
    r.t_valid AS DataValidade
ORDER BY bc.name, total_episodios DESC, e.name

// ============================================================
// 3. QUERY RESUMIDA: Apenas entidades e capabilities (sem duplicatas)
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WHERE 'Issue' IN labels(e)
RETURN DISTINCT
    e.name AS Entidade,
    head(labels(e)) AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS Nivel
ORDER BY bc.name, e.name

// ============================================================
// 4. QUERY POR TIPO DE ENTIDADE: Apenas Issues
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WHERE 'Issue' IN labels(e)
RETURN 
    'Issue' AS TipoEntidade,
    e.name AS Entidade,
    bc.name AS BusinessCapability,
    bc.level AS Nivel,
    count(*) AS TotalRelacionamentos
ORDER BY bc.name, e.name

// ============================================================
// 5. QUERY COM ESTATÍSTICAS: Entidades mais frequentes por Capability
// ============================================================
MATCH (e)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
OPTIONAL MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
WHERE 'Issue' IN labels(e)
WITH e, bc, count(DISTINCT ep) AS total_episodios, count(r) AS total_relacionamentos
RETURN 
    bc.name AS BusinessCapability,
    e.name AS Entidade,
    'Issue' AS Tipo,
    total_episodios AS EpisodiosRelacionados,
    total_relacionamentos AS TotalRelacionamentos
ORDER BY bc.name, total_episodios DESC, e.name

// ============================================================
// 6. QUERY PARA EXPORTAR PARA CSV/TABELA
// Formato mais limpo para visualização em tabela
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WHERE 'Issue' IN labels(e)
RETURN DISTINCT
    e.name AS Entidade,
    'Issue' AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS NivelCapacidade,
    bc.capability_type AS TipoCapacidade,
    bc.business_value AS ValorNegocio
ORDER BY bc.name, e.name

// ============================================================
// 6b. QUERY COM COMENTÁRIO (CONTEÚDO DO EPISÓDIO)
// Inclui o texto do comentário relacionado à entidade
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
WHERE 'Issue' IN labels(e)
RETURN DISTINCT
    e.name AS Entidade,
    'Issue' AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS NivelCapacidade,
    bc.capability_type AS TipoCapacidade,
    bc.business_value AS ValorNegocio,
    ep.content AS Comentario,
    ep.review_date AS DataComentario,
    ep.review_version AS VersaoApp
ORDER BY bc.name, e.name, ep.review_date DESC

// ============================================================
// 6c. QUERY COM COMENTÁRIO (AGRUPA MÚLTIPLOS COMENTÁRIOS)
// Se uma entidade aparece em múltiplos comentários, agrupa todos
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
WHERE 'Issue' IN labels(e)
WITH e, bc,
     collect(DISTINCT ep.content) AS comentarios,
     count(DISTINCT ep) AS total_comentarios
RETURN DISTINCT
    e.name AS Entidade,
    'Issue' AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS NivelCapacidade,
    bc.capability_type AS TipoCapacidade,
    bc.business_value AS ValorNegocio,
    total_comentarios AS TotalComentarios,
    comentarios AS Comentarios
ORDER BY bc.name, total_comentarios DESC, e.name

// ============================================================
// 6d. QUERY COM COMENTÁRIO (UM COMENTÁRIO POR LINHA)
// Versão expandida: cada linha mostra entidade + capability + um comentário
// Útil para análise detalhada
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
WHERE 'Issue' IN labels(e)
RETURN
    e.name AS Entidade,
    'Issue' AS Tipo,
    bc.name AS BusinessCapability,
    bc.level AS NivelCapacidade,
    ep.content AS Comentario,
    ep.review_date AS DataComentario,
    ep.review_version AS VersaoApp,
    ep.id AS EpisodeID
ORDER BY bc.name, e.name, ep.review_date DESC

// ============================================================
// 7. QUERY COM VERSÕES: Entidades, Capabilities e Versões relacionadas
// ============================================================
MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
OPTIONAL MATCH (e)-[rv:RELATED_TO_VERSION]->(v:Version)
WHERE 'Issue' IN labels(e)
RETURN DISTINCT
    e.name AS Entidade,
    'Issue' AS Tipo,
    bc.name AS BusinessCapability,
    collect(DISTINCT v.name) AS VersoesRelacionadas,
    sum(rv.count) AS TotalOcorrenciasVersoes
ORDER BY bc.name, e.name
