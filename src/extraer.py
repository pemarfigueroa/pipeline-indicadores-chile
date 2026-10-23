import requests
import json
import time
from pathlib import Path

# Defino los parametros del proceso
indicador = "dolar"
year = 2026
url = f"https://mindicador.cl/api/{indicador}/{str(year)}"

# Raíz del proyecto: este archivo está en src/, así que subimos un nivel
raiz = Path(__file__).resolve().parent.parent

# Ruta destino en Bronze
archivo_bronze = (raiz / "data" / "bronze"
                  / f"indicador={indicador}"
                  / f"year={str(year)}"
                  / f"{year}_{indicador}.json"
                  )


def extraer(url, intentos=3, espera=10):
    """Llama a la API con reintentos. Devuelve el JSON como diccionario."""
    for intento in range(1, intentos):
        try:
            # me conecto a la API
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()  # error si el status <> 2XX
            return resp.json()
        except requests.exceptions.RequestException as error:
            print(f"Intento {intento} de {intentos} falló: {error}")
            if intento < intentos:
                time.sleep(espera*intento)
    raise RuntimeError(
        f"No se pudo extraer {url} después de {intentos} intentos")


def guardar_json(datos, ruta):
    """Guarda el diccionario como JSON, creando las carpetas que falten."""
    # Se crean las carpetas si estas no existen
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="UTF-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    datos = extraer(url)
    print(f"Registros recibidos: {len(datos['serie'])}.")
    guardar_json(datos, archivo_bronze)
    print(f"Guardado en: {archivo_bronze}.")
