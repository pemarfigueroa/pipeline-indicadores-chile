import json
import pyarrow

import pandas as pd

from pathlib import Path

indicador = "uf"
year = 2026

raiz = Path(__file__).resolve().parent.parent

# Ruta json en Bronze
archivo_bronze = (raiz / "data" / "bronze"
                  / f"indicador={indicador}"
                  / f"year={str(year)}"
                  / f"{year}_{indicador}.json"
                  )

archivo_silver = (raiz / "data" / "silver"
                  / f"indicador={indicador}"
                  / f"year={str(year)}"
                  / f"{year}_{indicador}.parquet"
                  )


def extrae_bronze(file_bronz):
    with open(file_bronz, "r", encoding="utf-8") as archivo:
        dict_uf = json.load(archivo)
    return dict_uf


def trf_fechas(dict_bronze):
    df = pd.DataFrame(dict_bronze["serie"])
    df["fecha"] = pd.to_datetime(df["fecha"], utc=True).dt.tz_convert(
        "America/Santiago").dt.date
    return df


def ordena_df(df, campo_orden, orden=True):
    df_ordenado = df.sort_values(
        campo_orden, ascending=orden).reset_index(drop=True)
    return df_ordenado


def guarda_silver(df, ruta):
    """Guarda el dataframe en Silver, creando las carpetas que falten."""
    # Se crean las carpetas si estas no existen
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)


if __name__ == "__main__":
    dict_uf = extrae_bronze(archivo_bronze)
    df = trf_fechas(dict_uf)
    df["indicador"] = indicador
    df = ordena_df(df, "fecha")
    guarda_silver(df, archivo_silver)
    dfp = pd.read_parquet(archivo_silver)
    print(dfp.head())
    print(dfp.dtypes)
