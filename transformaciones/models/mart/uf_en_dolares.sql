{{ config(materialized='table') }}
SELECT UF.fecha,
       UF.valor_uf,
       DOL.valor_dolar,
       ROUND(valor_uf / valor_dolar, 2) valor_uf_en_dolar
  FROM {{ ref('stg_uf') }} UF
  ASOF LEFT JOIN {{ ref('stg_dolar') }} DOL
             ON  UF.fecha >= DOL.fecha
 ORDER BY UF.fecha