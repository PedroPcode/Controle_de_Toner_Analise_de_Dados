# Análise de Dados de Controle de Toner

### Objetivo do projeto:
Sistema de monitoramento de toner para impressoras, com alertas de níveis críticos e controle eficiente de consumíveis, visando otimizar a manutenção e reduzir custos operacionais.

### Fonte dos Dados:
Dados gerados aleatoriamente via Python e armazenados em banco SQL Server para simular o monitoramento de toner.

### Estrutura do Dataset:
O dataset principal é uma tabela chamada monitoramento que contém informações sobre impressoras e níveis de toner, com as seguintes colunas principais:
  - serie: Número de série da impressora
  - endereco_ip: IP do dispositivo
  - apelido: Nome ou apelido da impressora
  - fabricante e modelo: Dados do equipamento
  - cliente: Cliente responsável
  - data_coleta e data_monitoramento: Datas das verificações
  - Níveis de toner (preto_percent, ciano_percent, magenta_percent, amarelo_percent) e seus respectivos modelos e estimativas de dias restantes
  - status_monitoramento: Situação atual do monitoramento

## Perguntas a serem Respondidas

#### ⚪ **Query 1: Quantas impressoras estão sendo monitoradas por cliente?
*Solução:*
  - Seleciona o nome do cliente (cliente).
  - Conta o total de impressoras (COUNT(*)) que possuem o status Monitorando.
  - Agrupa os resultados por cliente para obter o total por cada um.
  - Ordena a lista em ordem decrescente do total de impressoras monitoradas.

  ```sql
  SELECT 
    cliente, 
    COUNT(*) AS total_monitoradas
FROM 
    monitoramento
WHERE 
    status_monitoramento = 'Monitorando'
GROUP BY 
    cliente
ORDER BY 
    total_monitoradas DESC;
  ```

#### *Resultado:*  
cliente           | total_monitoradas  
----------------- | -----------------  
Eta Services      | 27  
AlphaTech         | 20  
Epsilon Ltda      | 20  
DeltaWorks        | 19  
Gamma Solutions   | 19  
Iota Systems      | 19  
Zeta Industries   | 18  
BetaCorp          | 16  
Kappa Company     | 15  
Theta Enterprises | 9  

#### *Insights:*
  - Eta Services é o maior cliente com 27 impressoras monitoradas.
  - AlphaTech e Epsilon Ltda também têm grande volume (20 cada).
  - Base de clientes diversificada, com oportunidades para crescimento em clientes menores.


#### ⚪ Query 2: Quantas impressoras por cliente estão com toner abaixo de 10%?
*Solução:*
  - Filtra as impressoras da tabela monitoramento onde qualquer cor de toner (preto, ciano, amarelo ou magenta) está abaixo de 10%.
  - Agrupa o resultado por cliente.
  - Conta o total de impressoras com toner baixo por cliente.
  - Ordena a lista do maior para o menor número de impressoras críticas.

  ```sql
  SELECT 
    cliente,
    COUNT(*) AS impressoras_com_toner_baixo
FROM 
    monitoramento
WHERE 
    preto_percent < 10
    OR ciano_percent < 10
    OR amarelo_percent < 10
    OR magenta_percent < 10
GROUP BY 
    cliente
ORDER BY 
    impressoras_com_toner_baixo DESC;
  ```

#### *Resultado:*
cliente | impressoras_com_toner_baixo  
-- | --  
DeltaWorks | 9  
AlphaTech | 8  
BetaCorp | 7  
Eta Services | 6  
Gamma Solutions | 6  
Kappa Group | 5  
Epsilon Ltda | 5  
Theta Enterprises | 3  
Zeta Industries | 3  
Iota Systems | 2  

#### *Insights:*
  - DeltaWorks tem o maior número de impressoras com toner baixo, indicando necessidade de atenção imediata.
  - AlphaTech e BetaCorp também possuem impressoras críticas que podem afetar o desempenho.
  - Clientes com menor número de impressoras críticas representam oportunidades para manutenção preventiva.


























