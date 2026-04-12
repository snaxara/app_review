// ============================================================
// QUERIES PARA MÉTRICAS DE SOCIAL NETWORK ANALYSIS (SNA)
// Baseado em Pinheiro (2011) e Newman (2010)
// ============================================================

// 1. DEGREE CENTRALITY - Issues
// Número de BusinessCapabilities conectadas a cada Issue
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH i, count(bc) AS degree
RETURN i.name AS Issue, 
       degree AS DegreeCentrality,
       'Issue' AS NodeType
ORDER BY degree DESC
LIMIT 20

// 2. DEGREE CENTRALITY - BusinessCapabilities
// Número de Issues conectadas a cada BusinessCapability
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH bc, count(i) AS degree
RETURN bc.name AS BusinessCapability,
       degree AS DegreeCentrality,
       bc.level AS Level,
       bc.business_value AS BusinessValue,
       'BusinessCapability' AS NodeType
ORDER BY degree DESC

// 3. BETWEENNESS CENTRALITY (Aproximado) - Issues
// Issues que conectam múltiplas BusinessCapabilities diferentes
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH i, collect(DISTINCT bc) AS connected_caps
RETURN i.name AS Issue,
       size(connected_caps) AS BetweennessCentrality,
       [cap IN connected_caps | cap.name] AS ConnectedCapabilities
ORDER BY BetweennessCentrality DESC
LIMIT 20

// 4. CLOSENESS CENTRALITY (Aproximado) - Issues
// Issues que estão próximas de muitas outras Issues através de BusinessCapabilities compartilhadas
MATCH (i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(i2:Issue)
WHERE i1 <> i2
WITH i1, count(DISTINCT i2) AS reachable_issues
RETURN i1.name AS Issue,
       reachable_issues AS ReachableNodes,
       CASE WHEN reachable_issues > 0 THEN 1.0 / reachable_issues ELSE 0 END AS ClosenessCentrality
ORDER BY ClosenessCentrality DESC
LIMIT 20

// 5. CLUSTERING COEFFICIENT - Issues
// Conforme definição de Newman (2010): mede a proporção de conexões entre vizinhos
// C_i = (2 * número de conexões entre vizinhos) / (k_i * (k_i - 1))
// Varia de 0 a 1, onde 1 indica que todos os vizinhos estão conectados entre si
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH i, collect(DISTINCT bc) AS connected_caps, size(collect(DISTINCT bc)) AS k
WHERE k > 1
// Encontrar vizinhos (outras Issues que compartilham pelo menos uma BusinessCapability)
MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(neighbor:Issue)
WHERE neighbor <> i
WITH i, k, collect(DISTINCT neighbor) AS neighbors_list
WITH i, k, size(neighbors_list) AS num_neighbors, neighbors_list
// Contar conexões entre vizinhos (quantos pares de vizinhos compartilham BusinessCapabilities)
UNWIND range(0, size(neighbors_list) - 1) AS idx1
UNWIND range(idx1 + 1, size(neighbors_list) - 1) AS idx2
WITH i, k, num_neighbors, neighbors_list[idx1] AS n1, neighbors_list[idx2] AS n2
MATCH (n1)-[:RELATES_TO_CAPABILITY]->(shared_bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(n2)
WITH i, k, num_neighbors, count(DISTINCT {n1: n1, n2: n2}) AS edges_between_neighbors
WITH i, k, num_neighbors, edges_between_neighbors,
     CASE 
       WHEN num_neighbors > 1 THEN 2.0 * edges_between_neighbors / (num_neighbors * (num_neighbors - 1))
       ELSE 0.0
     END AS clustering
RETURN i.name AS Issue,
       k AS Degree,
       num_neighbors AS Neighbors,
       edges_between_neighbors AS EdgesBetweenNeighbors,
       clustering AS ClusteringCoefficient
ORDER BY clustering DESC
LIMIT 20

// 6. DENSIDADE DA REDE
// Densidade = número de links / número máximo possível de links
MATCH (i:Issue)
WITH count(i) AS total_issues
MATCH (bc:BusinessCapability)
WITH total_issues, count(bc) AS total_capabilities
MATCH (i:Issue)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH total_issues, total_capabilities, count(r) AS total_links
RETURN total_issues AS TotalIssues,
       total_capabilities AS TotalCapabilities,
       total_links AS TotalLinks,
       (total_issues * total_capabilities) AS MaxPossibleLinks,
       CASE WHEN (total_issues * total_capabilities) > 0 
            THEN 1.0 * total_links / (total_issues * total_capabilities)
            ELSE 0 END AS Density

// 7. IDENTIFICAÇÃO DE COMUNIDADES (Label Propagation Aproximado)
// Agrupa Issues que compartilham muitas BusinessCapabilities
MATCH (i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(i2:Issue)
WHERE i1 <> i2
WITH i1, i2, count(bc) AS shared_caps
WHERE shared_caps >= 1
WITH i1, collect({issue: i2.name, shared: shared_caps}) AS neighbors
RETURN i1.name AS Issue,
       size(neighbors) AS CommunitySize,
       neighbors[0..5] AS TopNeighbors
ORDER BY CommunitySize DESC
LIMIT 20

// 8. VISUALIZAÇÃO DE REDE COM CENTRALIDADE
// Visualiza o grafo com tamanho dos nós proporcional ao degree centrality
MATCH (i:Issue)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH i, bc, count(r) AS link_count
MATCH (i)
WITH i, collect({cap: bc.name, count: link_count}) AS capabilities
WITH i, size(capabilities) AS degree
MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
RETURN i, bc, degree
ORDER BY degree DESC

// 9. TOP ISSUES POR INFLUÊNCIA ESTRUTURAL
// Combina múltiplas métricas de centralidade para identificar issues mais influentes
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
WITH i, count(bc) AS degree_centrality, collect(DISTINCT bc) AS connected_caps
MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
MATCH (other:Issue)-[:RELATES_TO_CAPABILITY]->(bc)
WHERE other <> i
WITH i, degree_centrality, size(connected_caps) AS betweenness, count(DISTINCT other) AS reachable
OPTIONAL MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i)
WITH i, degree_centrality, betweenness, reachable, count(DISTINCT ep) AS episode_count
RETURN i.name AS Issue,
       degree_centrality AS DegreeCentrality,
       betweenness AS BetweennessCentrality,
       reachable AS ReachableIssues,
       episode_count AS TotalEpisodes,
       (degree_centrality + betweenness + reachable + episode_count) AS InfluenceScore
ORDER BY InfluenceScore DESC
LIMIT 20

// 10. BUSINESS CAPABILITIES MAIS CRÍTICAS (Combinação de Métricas)
// Identifica capabilities críticas combinando degree centrality e número de episódios
MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
OPTIONAL MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i)
WITH bc, count(DISTINCT i) AS total_issues, count(DISTINCT ep) AS total_episodes
RETURN bc.name AS BusinessCapability,
       total_issues AS DegreeCentrality,
       total_episodes AS TotalEpisodes,
       bc.level AS Level,
       bc.business_value AS BusinessValue,
       (total_issues * 2 + total_episodes) AS CriticalityScore
ORDER BY CriticalityScore DESC
