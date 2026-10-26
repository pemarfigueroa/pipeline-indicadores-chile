CREATE DATABASE indicadores;

CREATE EXTERNAL TABLE indicadores.silver (
    fecha date,
    valor double
)
PARTITIONED BY (
    indicador string,
    `year` int
)
STORED AS PARQUET
LOCATION 's3://pemar-pipeline-indicadores-dev/silver/';

MSCK REPAIR TABLE indicadores.silver;
