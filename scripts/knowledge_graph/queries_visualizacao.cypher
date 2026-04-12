// ============================================================
// QUERIES PARA VISUALIZAÇÃO NO NEO4J BROWSER
// ============================================================

// 1. VISUALIZAÇÃO COMPLETA: App -> Versões -> Issues -> BusinessCapability
// Use esta query para ver o grafo completo com tamanhos proporcionais
MATCH (app:App)
MATCH (app)<-[:BELONGS_TO]-(version:Version)
MATCH (episode:Episode)-[:HAS_VERSION]->(version)
MATCH (episode)-[:CONTAINS_ENTITY]->(issue:Issue)
MATCH (issue)-[r:RELATED_TO_VERSION]->(version)
MATCH (issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
RETURN app, version, episode, issue, bc, r
ORDER BY r.count DESC

// 2. VERSÃO COM MAIS PROBLEMAS (para alertas)
// Mostra versões problemáticas com contagem de issues
MATCH (version:Version)-[:BELONGS_TO]->(app:App)
MATCH (issue)-[r:RELATED_TO_VERSION]->(version)
WITH app, version, sum(r.count) as total_issues
ORDER BY total_issues DESC
RETURN app, version, total_issues
LIMIT 10

// 2b. DETALHES DAS ISSUES POR VERSÃO (use após query 2)
// Substitua '25.9.1.3' pela versão desejada
MATCH (version:Version {name: '25.9.1.3'})
MATCH (issue)-[r:RELATED_TO_VERSION]->(version)
WHERE 'Issue' IN labels(issue)
RETURN issue.name as issue_name, r.count as count
ORDER BY r.count DESC

// 3. ISSUES MAIS FREQUENTES POR VERSÃO
// Agrupa issues por versão com contagem
MATCH (issue:Issue)-[r:RELATED_TO_VERSION]->(version:Version)
WHERE r.count > 1
RETURN issue.name as issue_name, version.name as version, r.count as occurrences
ORDER BY r.count DESC

// 4. BUSINESS CAPABILITY COM MAIS PROBLEMAS
// Mostra quais capacidades têm mais issues relacionados
MATCH (issue:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH bc, count(issue) as total_issues
ORDER BY total_issues DESC
LIMIT 10
MATCH (issue:Issue)-[:RELATES_TO_CAPABILITY]->(bc)
RETURN bc, issue, count(*) as occurrences
ORDER BY occurrences DESC

// 5. VISUALIZAÇÃO POR VERSÃO ESPECÍFICA
// Substitua '25.9.1.3' pela versão desejada
MATCH (version:Version {name: '25.9.1.3'})
MATCH (episode:Episode)-[:HAS_VERSION]->(version)
MATCH (episode)-[:CONTAINS_ENTITY]->(issue:Issue)
MATCH (issue)-[r:RELATED_TO_VERSION]->(version)
MATCH (issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
RETURN version, episode, issue, bc, r
ORDER BY r.count DESC

// 6. CONTAGEM DE EPISÓDIOS POR VERSÃO
// Para ver quantos comentários cada versão tem
MATCH (version:Version)
OPTIONAL MATCH (episode:Episode)-[:HAS_VERSION]->(version)
WITH version, count(episode) as episodes_count
ORDER BY episodes_count DESC
RETURN version.name as version, episodes_count

// 7. ISSUES AGRUPADAS (sem duplicatas)
// Mostra todas as issues únicas e suas conexões
MATCH (issue:Issue)
OPTIONAL MATCH (issue)-[r:RELATED_TO_VERSION]->(version:Version)
OPTIONAL MATCH (issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
RETURN issue, version, bc, r
ORDER BY r.count DESC

// 8. ALERTA: VERSÕES COM MUITOS PROBLEMAS
// Versões com mais de 5 issues diferentes
MATCH (version:Version)
MATCH (issue:Issue)-[r:RELATED_TO_VERSION]->(version)
WITH version, count(DISTINCT issue) as distinct_issues, sum(r.count) as total_occurrences
WHERE distinct_issues >= 5
RETURN version.name as version, distinct_issues, total_occurrences
ORDER BY total_occurrences DESC

// 9. ISSUES SEM BUSINESS CAPABILITY (para correção)
// Encontra issues que não foram linkadas a nenhuma capacidade
MATCH (issue:Issue)
WHERE NOT (issue)-[:RELATES_TO_CAPABILITY]->()
RETURN issue.name as issue_name, issue.summary as summary
ORDER BY issue_name
