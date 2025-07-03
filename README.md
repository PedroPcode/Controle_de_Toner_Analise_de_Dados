# Análise de Dados de Controle de Toner

### Objetivo do projeto:
Sistema de monitoramento de toner para impressoras, com alertas de níveis críticos e controle eficiente de consumíveis, visando otimizar a manutenção e reduzir custos operacionais.
📄 [Visualizar apresentação](https://drive.google.com/file/d/1sK0VSvSYdx8aHK8lme8WRZuQBKzt-AHX/view?usp=sharing)

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

#### ⚪ Query 1: Quantas impressoras estão sendo monitoradas por cliente?
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

#### ⚪ Query 4: Quais são os modelos mais utilizados por cliente?
*Solução:*
  - Seleciona os seguintes campos da tabela monitoramento:
    - cliente, serie, endereco_ip (renomeado como ip), apelido (renomeado como local), modelo, e os níveis de toner: preto_percent, ciano_percent, amarelo_percent, magenta_percent.                      
  - Filtra os registros em que qualquer um dos níveis de toner (preto, ciano, amarelo, magenta) esteja abaixo de 10%.

  ```sql
  SELECT 
    cliente, 
    serie, 
    endereco_ip AS ip,
    apelido AS local, 
    modelo, 
    preto_percent AS toner_preto, 
    ciano_percent AS toner_ciano,
    amarelo_percent AS toner_amarelo,
    magenta_percent AS toner_magenta
FROM 
    monitoramento
WHERE 
    preto_percent < 10
    OR ciano_percent < 10
    OR amarelo_percent < 10
    OR magenta_percent < 10;
  ```

#### *Resultado:*
| cliente          | serie    | ip       | local                  | modelo     | toner_preto | toner_ciano | toner_amarelo | toner_magenta 
|------------------|----------|----------|------------------------|------------|-------------|-------------|---------------|---------------
| Theta Enterprises| GBX58607 | 10716.55 | Sala de Treinamento 264| SL-K4250RX | 6           | NULL        | NULL          | NULL          
| Epsilon Ltda     | WAT67467 | 10345.77 | Controladoria 241      | SL-C4062FX | 83          | 8           | 72            | 74            
| BetaCorp         | BUD62927 | 10556.83 | Auditório 204          | SL-X4220RX | 98          | 90          | 15            | 0             
| Theta Enterprises| OGB45371 | 10376.73 | Administrativo 120     | SL-C4062FX | 33          | 33          | 64            | 0             
| Eta Services     | HHQ57897 | 10780.36 | Planejamento 151       | SL-X4220RX | 4           | 44          | 74            | 54            
| DeltaWorks       | AWU15316 | 10884.57 | Compras 297            | SL-X4220RX | 65          | 5           | 56            | 18            
| Zeta Industries  | TKC39683 | 10618.98 | Patrimônio 179         | SL-K4250RX | 0           | NULL        | NULL          | NULL          
| DeltaWorks       | NAD82084 | 10327.20 | Portaria 119           | SL-C4062FX | 5           | 30          | 85            | 83            
| Gamma Solutions  | NIC38441 | 10483.17 | Logística 106          | SL-M4080FX | 2           | NULL        | NULL          | NULL          
| DeltaWorks       | IHN28538 | 10590.85 | Secretaria Executiva 294| SL-X4220RX| 9           | 50          | 77            | 27            
| Gamma Solutions  | NCF47039 | 10889.53 | Expedição 274          | SL-C4062FX | 0           | 56          | 86            | 35            
| Kappa Group      | VHO86539 | 10497.56 | Prédio 3 190           | SL-C4062FX | 4           | 34          | 21            | 4             
| Epsilon Ltda     | NIB24368 | 10214.64 | RH 222                 | SL-X4220RX | 4           | 100         | 1             | 49            
| Eta Services     | NSE58793 | 10688.73 | Recepção 2 152         | SL-K4250RX | 1           | NULL        | NULL          | NULL          
| DeltaWorks       | XBQ43452 | 10286.82 | Suporte Técnico 193    | SL-X4220RX | 49          | 3           | 95            | 97            
| Gamma Solutions  | QPV62008 | 10818.89 | Planejamento 211       | SL-X4220RX | 4           | 87          | 74            | 18            
| Epsilon Ltda     | UQC81894 | 10121.97 | Arquivos 223           | SL-C4062FX | 4           | 38          | 10            | 57            
| AlphaTech        | NWN48993 | 10227.16 | Piso 1 244             | SL-C4062FX | 41          | 81          | 9             | 55            
| BetaCorp         | GPW53684 | 10713.97 | Estoque 231            | SL-M4080FX | 4           | NULL        | NULL          | NULL          
| DeltaWorks       | CBN95904 | 10824.37 | Gerência 186           | SL-X4220RX | 16          | 90          | 24            | 3             
| Eta Services     | NFT70770 | 10260.73 | Logística 170          | SL-C4062FX | 5           | 61          | 30            | 44            
| Kappa Group      | WPS89718 | 10486.76 | Recepção 132           | SL-M4080FX | 6           | NULL        | NULL          | NULL          
| Gamma Solutions  | MVA17655 | 10503.01 | Secretaria 278         | SL-K4250RX | 6           | NULL        | NULL          | NULL          
| AlphaTech        | NVA14843 | 10243.13 | Juridico 199           | SL-C4062FX | 1           | 80          | 76            | 40            
| DeltaWorks       | GDL03094 | 10545.09 | Marketing 265          | SL-K4250RX | 3           | NULL        | NULL          | NULL          
| AlphaTech        | YLU90990 | 10527.03 | Sala VIP 110           | SL-X4220RX | 3           | 82          | 23            | 24            

#### *Insights:*
  - Impressoras com toner abaixo de 10% devem ser priorizadas para reposição.
  - A impressora da BetaCorp apresenta nível crítico em preto (3%).
  - O monitoramento proativo evita falhas operacionais e paradas inesperadas.

#### ⚪ Query 5: Qual a vida útil estimada dos toners atuais?
*Solução:*
  - Seleciona da tabela monitoramento as colunas:
    - serie, endereco_ip (renomeado como ip), modelo, cliente.
  - As colunas que indicam os dias restantes de vida útil de cada toner (dias_restantes_preto, dias_restantes_ciano, dias_restantes_amarelo, dias_restantes_magenta) convertidas para número decimal com TRY_CAST.
- Ordena o resultado pelo número de série (serie).

   ```sql
  SELECT 
    serie,
    endereco_ip AS ip,
    modelo,
    cliente,
    TRY_CAST(dias_restantes_preto AS DECIMAL(10,2)) AS dias_restantes_preto,
    TRY_CAST(dias_restantes_ciano AS DECIMAL(10,2)) AS dias_restantes_ciano,
    TRY_CAST(dias_restantes_amarelo AS DECIMAL(10,2)) AS dias_restantes_amarelo,
    TRY_CAST(dias_restantes_magenta AS DECIMAL(10,2)) AS dias_restantes_magenta
  FROM 
      monitoramento
  ORDER BY 
      serie;
  ```

#### *Resultado:*  
| Série    | IP       | Modelo    | Cliente          | Vida Útil Preto | Vida Útil Ciano | Vida Útil Amarelo | Vida Útil Magenta 
|----------|----------|-----------|------------------|-----------------|-----------------|-------------------|-------------------
| ACE54697 | 10776.48 | SL-K4250RX| Eta Services     | 44              | NULL            | NULL              | NULL              
| AHM68903 | 10548.74 | SL-M4080FX| Gamma Solutions  | 98              | NULL            | NULL              | NULL              
| ANX18310 | 10577.17 | SL-K4250RX| Theta Enterprises| 17              | NULL            | NULL              | NULL              
| AVK35418 | 10802.74 | SL-K4250RX| DeltaWorks       | 97              | NULL            | NULL              | NULL              
| AWR15459 | 10877.10 | SL-X4220RX| Zeta Industries  | 41              | 67              | 35                | 23                
| AWU15316 | 10884.57 | SL-X4220RX| DeltaWorks       | 23              | 14              | 98                | 5                 

#### *Insights:*
  - A vida útil estimada dos toners ajuda no planejamento de reposições e manutenção.
  - Valores NULL indicam que o equipamento não é colorido.
  - Priorizar substituição dos toners com dias restantes baixos para evitar interrupções.
  - Monitorar os clientes e modelos com maior consumo para otimizar estoque e logística.

#### ⚪ Query 6: Quais grupos têm mais impressoras coloridas?
*Solução:*
  - Seleciona o nome do cliente (cliente).
  - Conta o total de impressoras que possuem valor não nulo na coluna ciano_percent (indicando que são coloridas).
  - Agrupa os resultados por cliente para obter o total por cada um.
  - Ordena a lista em ordem decrescente do total de impressoras coloridas.

   ```sql
  SELECT
    cliente,
    COUNT(*) AS total_coloridas
  FROM
      monitoramento
  WHERE
      ciano_percent IS NOT NULL
  GROUP BY
      cliente
  ORDER BY
      total_coloridas DESC;

  ```

#### *Resultado:*  
cliente           | total_coloridas  
--                | --  
Eta Services      | 18  
Epsilon Ltda      | 16  
AlphaTech         | 14  
BetaCorp          | 12  
DeltaWorks        | 11  
Zeta Industries   | 11  
Kappa Group       | 10  
Gamma Solutions   | 9  
Iota Systems      | 7  
Theta Enterprises | 5               

#### *Insights:*
  - Eta Services é o cliente com maior número de impressoras coloridas.
  - A presença forte de clientes como Epsilon Ltda, AlphaTech e BetaCorp indica maior uso de impressoras coloridas nesses grupos.
  - Clientes menores, como Iota Systems e Theta Enterprises, ainda podem expandir sua base de impressoras coloridas.

#### ⚪ Query 7: Quais clientes estão com impressoras sem monitoramento ativo?
*Solução:*
  - Seleciona o nome do cliente (cliente).
  - Conta o total de impressoras que possuem o status 'Sem monitoramento'.
  - Agrupa os resultados por cliente para obter o total por cada um.
  - Ordena a lista em ordem decrescente do total de impressoras sem monitoramento.

   ```sql
  SELECT 
    cliente, 
    COUNT(*) AS total_sem_monitoramento
  FROM
      monitoramento
  WHERE 
      status_monitoramento = 'Sem monitoramento'
  GROUP BY
      cliente
  ORDER BY
      total_sem_monitoramento DESC;
  ```

#### *Resultado:*  
cliente | total_sem_monitoramento  
-- | --  
Gamma Solutions | 7  
Kappa Group | 7  
AlphaTech | 5  
BetaCorp | 5  
Epsilon Ltda | 3  
Theta Enterprises | 3  
Zeta Industries | 3  
Iota Systems | 2  
Eta Services | 2  
DeltaWorks | 1             

#### *Insights:*
  - Gamma Solutions e Kappa Group têm o maior número de impressoras sem monitoramento, o que pode indicar necessidade de revisão.
  - Clientes com menor número de dispositivos sem monitoramento mantêm boa cobertura e acompanhamento.
  - É importante focar esforços para retomar o monitoramento dos dispositivos dessas empresas, garantindo dados atualizados e controle eficaz.

#### ⚪ Query 8: Quantas impressoras coloridas e monocromáticas temos por cliente?
*Solução:*
  - Seleciona o nome do cliente (cliente).
  - Conta o total de impressoras coloridas: onde qualquer dos campos de cor (ciano_percent, amarelo_percent ou magenta_percent) não é nulo.
  - Conta o total de impressoras monocromáticas: onde todos os campos de cor são nulos.
  - Agrupa os resultados por cliente.
  - Ordena a lista em ordem alfabética de cliente.

   ```sql
  SELECT
    cliente,
    SUM(CASE 
            WHEN ciano_percent IS NOT NULL 
              OR amarelo_percent IS NOT NULL 
              OR magenta_percent IS NOT NULL 
            THEN 1 ELSE 0 
        END) AS total_coloridas,
    SUM(CASE 
            WHEN ciano_percent IS NULL 
              AND amarelo_percent IS NULL 
              AND magenta_percent IS NULL 
            THEN 1 ELSE 0 
        END) AS total_mono
  FROM
      monitoramento
  GROUP BY
      cliente
  ORDER BY
      total_coloridas desc;
  ```

#### *Resultado:*  
| cliente           | total_coloridas | total_mono 
| ----------------- | ---------------- | ---------- 
| Eta Services      | 18               | 11          
| Epsilon Ltda      | 16               | 7           
| AlphaTech         | 14               | 11          
| BetaCorp          | 12               | 9           
| DeltaWorks        | 11               | 9           
| Zeta Industries   | 11               | 10          
| Kappa Group       | 10               | 12          
| Gamma Solutions   | 9                | 17          
| Iota Systems      | 7                | 14          
| Theta Enterprises | 5                | 7           
   
           

#### *Insights:*
  - Eta Services lidera com o maior número de impressoras coloridas e também tem uma base sólida de monocromáticas.
  - Gamma Solutions é o oposto: tem mais impressoras monocromáticas do que coloridas.
  - Clientes com equilíbrio entre os dois tipos, como AlphaTech e Zeta Industries, indicam ambientes com necessidades mistas de impressão.

## 📦 Download do Projeto
- 📊 [Download do Dashboard Power BI (.pbix)](./Controle%20de%20Toner%20Projeto%20PedroPcode.pbix)
![image](https://github.com/user-attachments/assets/f0373cc1-9417-4001-9851-c409afb3b733)
