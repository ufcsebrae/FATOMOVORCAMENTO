queries = {
    "orcado": """
        SELECT 
            A.IDORCAMENTO,
            A.SEQITMORCA,
            VALORORCADO,
            B.CODCCUSTO 
        FROM CorporeRM.TITMCONTORCAMENTARIO A 
        INNER JOIN (
            SELECT 
                IDORCAMENTO,
                CODCCUSTO,
                ANOORCAMENTO 
            FROM CorporeRM.TCONTORCAMENTARIO 
            WHERE ANOORCAMENTO = 2025
        ) B ON A.IDORCAMENTO = B.IDORCAMENTO
        ORDER BY A.IDORCAMENTO, SEQITMORCA ASC
    """,
    
    "diferencas": """   
        WITH Comparacao AS (
            SELECT 
                a.IDORCAMENTO,
                a.SEQITMORCA,
                a.CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                a.VALORORCADO - b.VALORORCADO AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado a
            JOIN orcado b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
                AND a.data_atualizacao = DATEADD(DAY, 1, b.data_atualizacao)
        )
        
        SELECT *
        FROM Comparacao 
        WHERE DIFERENCA <> 0
        AND DATA_ATUAL = (SELECT MAX(DATA_ATUAL) FROM Comparacao)
        ORDER BY IDORCAMENTO, SEQITMORCA, CODCCUSTO, DATA_ATUAL DESC
    """,
    
    "CC": """
        WITH Comparacao AS (
            SELECT 
                a.IDORCAMENTO,
                a.SEQITMORCA,
                a.CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                a.VALORORCADO - b.VALORORCADO AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado a
            JOIN orcado b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
                AND a.data_atualizacao = DATEADD(DAY, 1, b.data_atualizacao)
        )
        
        SELECT
			UPPER(B.CAMPOLIVRE) AS PROJETO,
			UPPER(C.CAMPOLIVRE) AS ACAO,
            A.CODCCUSTO, 
            SUM(DIFERENCA) AS TOTAL_DIFERENCA
        FROM Comparacao A
		INNER JOIN (SELECT CODCCUSTO,CAMPOLIVRE FROM HubDados.CorporeRM.GCCUSTO WHERE lEN(CODCCUSTO) = 5) B
		ON LEFT(A.CODCCUSTO,5) COLLATE SQL_Latin1_General_CP1_CI_AI = B.CODCCUSTO
		INNER JOIN (SELECT CODCCUSTO,CAMPOLIVRE FROM HubDados.CorporeRM.GCCUSTO WHERE lEN(CODCCUSTO) = 12) C
		ON A.CODCCUSTO COLLATE SQL_Latin1_General_CP1_CI_AI = C.CODCCUSTO


        WHERE DIFERENCA <> 0
        AND DATA_ATUAL = (SELECT MAX(DATA_ATUAL) FROM Comparacao)
        GROUP BY C.CAMPOLIVRE,B.CAMPOLIVRE,A.CODCCUSTO
        ORDER BY TOTAL_DIFERENCA DESC
    """,
    
    "ID": """
        WITH Comparacao AS (
            SELECT 
                a.IDORCAMENTO,
                a.SEQITMORCA,
                a.CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                a.VALORORCADO - b.VALORORCADO AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado a
            JOIN orcado b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
                AND a.data_atualizacao = DATEADD(DAY, 1, b.data_atualizacao)
        )
        
        SELECT 
            IDORCAMENTO, 
            SUM(DIFERENCA) AS TOTAL_DIFERENCA
        FROM Comparacao
        WHERE DIFERENCA <> 0
        AND DATA_ATUAL = (SELECT MAX(DATA_ATUAL) FROM Comparacao)
        GROUP BY IDORCAMENTO
        ORDER BY TOTAL_DIFERENCA DESC
    """
}