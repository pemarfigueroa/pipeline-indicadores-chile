CREATE TABLE indicadores.uf_en_dolares
WITH (
    format = 'PARQUET',
    external_location = 's3://pemar-pipeline-indicadores-dev/gold/uf_en_dolares/'
) AS
WITH cruce AS (
    SELECT u.fecha,
           u.valor AS valor_uf,
           LAST_VALUE(d.valor) IGNORE NULLS OVER (
               ORDER BY u.fecha
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS valor_dolar
    FROM indicadores.silver u
    LEFT JOIN indicadores.silver d
           ON d.fecha = u.fecha
          AND d.indicador = 'dolar'
    WHERE u.indicador = 'uf'
)
SELECT fecha,
       valor_uf,
       valor_dolar,
       ROUND(valor_uf / valor_dolar, 2) AS valor_uf_en_dolar
FROM cruce;