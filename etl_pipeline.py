"""
Pipeline ETL - TecnoAndes (versión empaquetada del taller).

Uso (desde la raíz del repositorio, después de generar los datos):
    python src/etl_pipeline.py

Lee las fuentes de datos/, aplica las transformaciones y carga el modelo
estrella en salida/tecnoandes_dw.db (SQLite).
"""
import json
import logging
import os
import sqlite3
import unicodedata

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("etl")

DATOS, SALIDA = "datos", "salida"
DB = os.path.join(SALIDA, "tecnoandes_dw.db")
MAPA_CIUDADES = {"bogota": "Bogotá", "medellin": "Medellín", "cali": "Cali",
                 "barranquilla": "Barranquilla", "bucaramanga": "Bucaramanga",
                 "cartagena": "Cartagena", "pereira": "Pereira"}


# ----------------------------- EXTRACCIÓN -----------------------------
def extraer():
    ventas = pd.read_csv(f"{DATOS}/ventas.csv", sep=";", encoding="utf-8")
    with open(f"{DATOS}/clientes.json", encoding="utf-8") as f:
        clientes = pd.DataFrame(json.load(f))
    productos = pd.read_excel(f"{DATOS}/productos.xlsx", sheet_name="catalogo")
    log.info("Extraídos: ventas=%d clientes=%d productos=%d", len(ventas), len(clientes), len(productos))
    return ventas, clientes, productos


# ---------------------------- TRANSFORMACIÓN ----------------------------
def _normalizar(t):
    t = str(t).strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def _parsear_fecha(s):
    r = pd.Series(pd.NaT, index=s.index)
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]:
        m = r.isna()
        r[m] = pd.to_datetime(s[m], format=fmt, errors="coerce")
    return r


def transformar(ventas, clientes, productos):
    v, c, p = ventas.copy(), clientes.copy(), productos.copy()

    v = v.drop_duplicates(subset="id_venta")
    v["fecha"] = _parsear_fecha(v["fecha"])

    malos = v["cantidad"].isna() | (v["cantidad"] <= 0) | v["fecha"].isna()
    rechazos = v[malos].assign(motivo="cantidad o fecha inválida")
    v = v[~malos].copy()
    v["cantidad"] = v["cantidad"].astype(int)

    v["descuento"] = v["descuento"].fillna("0%").replace("", "0%").str.rstrip("%").astype(float) / 100
    v["canal"] = v["canal"].str.strip().str.capitalize()

    c["ciudad"] = c["ciudad"].map(_normalizar).map(MAPA_CIUDADES)
    c["nombre"] = c["nombre"].str.title()
    c["email"] = c["email"].fillna("sin_email@desconocido.com")
    c["fecha_registro"] = pd.to_datetime(c["fecha_registro"])
    p["categoria"] = p["categoria"].str.strip().str.capitalize()

    huerf = ~v["id_cliente"].isin(c["id_cliente"]) | ~v["id_producto"].isin(p["id_producto"])
    rechazos = pd.concat([rechazos, v[huerf].assign(motivo="llave foránea inexistente")])
    v = v[~huerf]

    df = v.merge(p[["id_producto", "precio_unitario"]], on="id_producto")
    df["subtotal"] = df["cantidad"] * df["precio_unitario"]
    df["total"] = df["subtotal"] - (df["subtotal"] * df["descuento"]).round(0)
    df["id_fecha"] = df["fecha"].dt.strftime("%Y%m%d").astype(int)

    # Validaciones: si alguna falla, el pipeline se detiene
    assert df["id_venta"].is_unique, "id_venta duplicado"
    assert (df["total"] <= df["subtotal"]).all(), "total mayor que subtotal"
    assert c["ciudad"].notna().all(), "ciudad sin mapear"

    dim_fecha = pd.DataFrame({"fecha": pd.date_range("2025-01-01", "2025-12-31")})
    dim_fecha["id_fecha"] = dim_fecha["fecha"].dt.strftime("%Y%m%d").astype(int)
    dim_fecha["anio"] = dim_fecha["fecha"].dt.year
    dim_fecha["mes"] = dim_fecha["fecha"].dt.month
    dim_fecha["trimestre"] = dim_fecha["fecha"].dt.quarter
    dim_fecha["dia_semana"] = dim_fecha["fecha"].dt.day_name()

    fact = df[["id_venta", "id_fecha", "id_cliente", "id_producto", "canal",
               "cantidad", "precio_unitario", "descuento", "subtotal", "total"]]
    log.info("Transformado: %d ventas válidas, %d rechazos", len(fact), len(rechazos))
    return {"dim_cliente": c, "dim_producto": p, "dim_fecha": dim_fecha,
            "fact_ventas": fact, "rechazos": rechazos}


# -------------------------------- CARGA --------------------------------
def cargar(tablas):
    os.makedirs(SALIDA, exist_ok=True)
    with sqlite3.connect(DB) as con:
        for nombre, t in tablas.items():
            t.to_sql(nombre, con, if_exists="replace", index=False)
            log.info("Cargada %-12s %5d filas", nombre, len(t))


def main():
    log.info("=== Inicio ETL ===")
    cargar(transformar(*extraer()))
    log.info("=== Fin ETL: %s ===", DB)


if __name__ == "__main__":
    main()
