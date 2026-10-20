"""
Genera los datos de entrada del Taller ETL, con errores de calidad intencionales.

Uso (desde la raíz del repositorio):
    python src/generar_datos.py

Crea la carpeta datos/ con: ventas.csv, clientes.json y productos.xlsx.
La semilla aleatoria es fija, por lo que los datos son siempre los mismos.
"""
import json
import os
import random

import pandas as pd

random.seed(42)
os.makedirs("datos", exist_ok=True)

# ---------- PRODUCTOS (Excel) ----------
productos = pd.DataFrame({
    "id_producto": [f"P{i:03d}" for i in range(1, 11)],
    "nombre": ["Portátil", "Mouse", "Teclado", "Monitor 24\"", "Audífonos",
               "Impresora", "Tablet", "Disco SSD 1TB", "Cámara Web", "Router WiFi"],
    "categoria": ["Computo", "Accesorios", "accesorios", "Computo", "Audio",
                  "Oficina", "Computo", "Almacenamiento", "Accesorios ", "Redes"],
    "precio_unitario": [3200000, 45000, 120000, 780000, 150000,
                        650000, 1400000, 380000, 95000, 210000],
})
productos.to_excel("datos/productos.xlsx", index=False, sheet_name="catalogo")

# ---------- CLIENTES (JSON) ----------
nombres = ["Ana Gómez", "Luis Pérez", "María Rodríguez", "Carlos López", "Laura Martínez",
           "Jorge Ramírez", "Sofía Torres", "Andrés Díaz", "Valentina Ruiz", "Felipe Castro",
           "Camila Herrera", "Santiago Moreno", "Daniela Rojas", "Juan Vargas", "Paula Ortiz"]
ciudades = ["Bogotá", "bogota", "Medellín", "MEDELLIN", " Cali", "Barranquilla",
            "Bucaramanga", "Cartagena", "Bogotá ", "Pereira"]
clientes = []
for i, n in enumerate(nombres, start=1):
    clientes.append({
        "id_cliente": i,
        "nombre": n if i % 5 else n.upper(),          # algunos en mayúsculas
        "email": None if i in (4, 11) else f"{n.split()[0].lower()}{i}@correo.com",
        "ciudad": random.choice(ciudades),
        "fecha_registro": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
    })
with open("datos/clientes.json", "w", encoding="utf-8") as f:
    json.dump(clientes, f, ensure_ascii=False, indent=2)

# ---------- VENTAS (CSV) ----------
formatos = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]          # fechas inconsistentes
filas = []
for i in range(1, 501):
    fecha = pd.Timestamp("2025-01-01") + pd.Timedelta(days=random.randint(0, 364))
    cantidad = random.randint(1, 5)
    if i % 37 == 0:
        cantidad = -cantidad                                # cantidades negativas (error)
    filas.append({
        "id_venta": i,
        "fecha": fecha.strftime(random.choice(formatos)),
        "id_cliente": random.randint(1, 16),               # el 16 no existe (huérfano)
        "id_producto": random.choice(productos["id_producto"]),
        "cantidad": cantidad if i % 53 else None,          # nulos
        "descuento": random.choice(["0%", "5%", "10%", "", "15%"]),
        "canal": random.choice(["Web", "web", "Tienda", "TIENDA", "App"]),
    })
ventas = pd.DataFrame(filas)
ventas = pd.concat([ventas, ventas.sample(15, random_state=1)])   # duplicados
ventas = ventas.sample(frac=1, random_state=7)                    # desordenar
ventas.to_csv("datos/ventas.csv", index=False, sep=";", encoding="utf-8")

print("Datos generados en ./datos:")
for f in sorted(os.listdir("datos")):
    print("  -", f)
