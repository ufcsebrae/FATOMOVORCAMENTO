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
        
        WITH ultimos_dois_dias AS (
            SELECT DISTINCT data_atualizacao
            FROM orcado
            ORDER BY data_atualizacao DESC
            OFFSET 0 ROWS FETCH NEXT 2 ROWS ONLY
        ),
        dias AS (
            SELECT 
                MAX(data_atualizacao) AS data_atual,
                MIN(data_atualizacao) AS data_anterior
            FROM ultimos_dois_dias
        ),
        orcado_dia_atual AS (
            SELECT IDORCAMENTO, SEQITMORCA, CODCCUSTO, VALORORCADO, data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_atual
        ),
        orcado_dia_anterior AS (
            SELECT IDORCAMENTO, SEQITMORCA, CODCCUSTO, VALORORCADO, data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_anterior
        ),
        Comparacao AS (
            SELECT 
                COALESCE(a.IDORCAMENTO, b.IDORCAMENTO) AS IDORCAMENTO,
                COALESCE(a.SEQITMORCA, b.SEQITMORCA) AS SEQITMORCA,
                COALESCE(a.CODCCUSTO, b.CODCCUSTO) AS CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                ISNULL(a.VALORORCADO, 0) - ISNULL(b.VALORORCADO, 0) AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado_dia_atual a
            FULL OUTER JOIN orcado_dia_anterior b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
        )

        SELECT *
        FROM Comparacao
        WHERE ISNULL(DIFERENCA, 0) <> 0
        ORDER BY IDORCAMENTO, SEQITMORCA, CODCCUSTO, DATA_ATUAL DESC;

    """,

    "CC": """
        WITH dias AS (
            SELECT 
                MAX(data_atualizacao) AS data_atual,
                DATEADD(DAY, -1, MAX(data_atualizacao)) AS data_anterior
            FROM orcado
        ),
        orcado_dia_atual AS (
            SELECT 
                IDORCAMENTO,
                SEQITMORCA,
                CODCCUSTO,
                VALORORCADO,
                data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_atual
        ),
        orcado_dia_anterior AS (
            SELECT 
                IDORCAMENTO,
                SEQITMORCA,
                CODCCUSTO,
                VALORORCADO,
                data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_anterior
        ),
        Comparacao AS (
            SELECT 
                COALESCE(a.IDORCAMENTO, b.IDORCAMENTO) AS IDORCAMENTO,
                COALESCE(a.SEQITMORCA, b.SEQITMORCA) AS SEQITMORCA,
                COALESCE(a.CODCCUSTO, b.CODCCUSTO) AS CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                ISNULL(a.VALORORCADO, 0) - ISNULL(b.VALORORCADO, 0) AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado_dia_atual a
            FULL OUTER JOIN orcado_dia_anterior b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
        )

        SELECT
            UPPER(B.CAMPOLIVRE) AS PROJETO,
            UPPER(C.CAMPOLIVRE) AS ACAO,
            A.CODCCUSTO, 
            SUM(DIFERENCA) AS TOTAL_DIFERENCA
        FROM Comparacao A
        LEFT JOIN (
            SELECT CODCCUSTO, CAMPOLIVRE 
            FROM HubDados.CorporeRM.GCCUSTO 
            WHERE LEN(CODCCUSTO) = 5
        ) B
            ON LEFT(A.CODCCUSTO, 5) COLLATE SQL_Latin1_General_CP1_CI_AI = B.CODCCUSTO
        LEFT JOIN (
            SELECT CODCCUSTO, CAMPOLIVRE 
            FROM HubDados.CorporeRM.GCCUSTO 
            WHERE LEN(CODCCUSTO) = 12
        ) C
            ON A.CODCCUSTO COLLATE SQL_Latin1_General_CP1_CI_AI = C.CODCCUSTO

        WHERE ISNULL(DIFERENCA, 0) <> 0
        GROUP BY C.CAMPOLIVRE, B.CAMPOLIVRE, A.CODCCUSTO
        ORDER BY A.CODCCUSTO, TOTAL_DIFERENCA DESC;
    """,

    "ID": """
        
        WITH dias AS (
            SELECT 
                MAX(data_atualizacao) AS data_atual,
                DATEADD(DAY, -1, MAX(data_atualizacao)) AS data_anterior
            FROM orcado
        ),
        orcado_dia_atual AS (
            SELECT IDORCAMENTO, SEQITMORCA, CODCCUSTO, VALORORCADO, data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_atual
        ),
        orcado_dia_anterior AS (
            SELECT IDORCAMENTO, SEQITMORCA, CODCCUSTO, VALORORCADO, data_atualizacao
            FROM orcado o
            JOIN dias d ON o.data_atualizacao = d.data_anterior
        ),
        Comparacao AS (
            SELECT 
                COALESCE(a.IDORCAMENTO, b.IDORCAMENTO) AS IDORCAMENTO,
                COALESCE(a.SEQITMORCA, b.SEQITMORCA) AS SEQITMORCA,
                COALESCE(a.CODCCUSTO, b.CODCCUSTO) AS CODCCUSTO,
                a.VALORORCADO AS VALOR_DIA_ATUAL,
                b.VALORORCADO AS VALOR_DIA_ANTERIOR,
                ISNULL(a.VALORORCADO, 0) - ISNULL(b.VALORORCADO, 0) AS DIFERENCA,
                a.data_atualizacao AS DATA_ATUAL,
                b.data_atualizacao AS DATA_ANTERIOR
            FROM orcado_dia_atual a
            FULL OUTER JOIN orcado_dia_anterior b
                ON a.IDORCAMENTO = b.IDORCAMENTO
                AND a.SEQITMORCA = b.SEQITMORCA
                AND a.CODCCUSTO = b.CODCCUSTO
        )

        SELECT 
            IDORCAMENTO, 
            SUM(DIFERENCA) AS TOTAL_DIFERENCA
        FROM Comparacao
        WHERE ISNULL(DIFERENCA, 0) <> 0
        GROUP BY IDORCAMENTO
        ORDER BY TOTAL_DIFERENCA DESC;
    """
}
