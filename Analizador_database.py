# =====================================================================
# PROYECTO: ANALIZADOR CON BASE DE DATOS SQL (FASE 4)
# OBJETIVO: Guardar el historial de lotes en una base de datos real.
# =====================================================================

import sqlite3  # Importamos el módulo nativo de Python para SQL

print("=========================================")
print("   SISTEMA DE MARGENES CON SQL (F4)   ")
print("=========================================\n")

# 1. BLINDAJE Y ENTRADA DE DATOS (Fase 3)
while True:
    try:
        nombre_lote = input("Dale un nombre o etiqueta a este lote (Ej: Tenis_Nike, Camisas_Boss): ")
        costo_lote = float(input("¿Cuánto cuesta el lote completo ($)? "))
        num_piezas = int(input("¿Cuántas piezas trae el lote en total? "))
        costo_envio = float(input("¿Cuánto te cobran de envío ($)? "))
        merma = int(input("¿Cuántas piezas estimas de MERMA?: "))
        break
    except ValueError:
        print("\n[❌ ERROR] ¡Introduce solo números en los costos y piezas!\n")

# 2. PROCESAMIENTO Y LOGICA DE NEGOCIO
inversion_total = costo_lote + costo_envio
piezas_vendibles = num_piezas - merma

if piezas_vendibles <= 0:
    print("\n[⚠️ ALERTA] Negocio inviable. Revisa tus piezas y merma.")
else:
    costo_real_unitario = inversion_total / piezas_vendibles
    
    # Precios sugeridos (Margen del 50% como estándar para el ejemplo)
    precio_sugerido = costo_real_unitario / (1 - 0.50)

    # =================================================================
    # ⚙️ MÁGIA DE BASE DE DATOS (CONEXIÓN SQL)
    # =================================================================
    
    # Conectamos al archivo de la base de datos (si no existe, Python lo crea en automático)
    conexion = sqlite3.connect("mi_negocio.db")
    
    # El 'cursor' es el que nos permite ejecutar comandos SQL dentro de la base de datos
    cursor = conexion.cursor()
    
    # Creamos la tabla usando lenguaje SQL puro si es la primera vez que corre el programa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            inversion_total REAL,
            piezas_vendibles INTEGER,
            costo_unitario REAL,
            precio_sugerido_50 REAL
        )
    """)
    
    # Insertamos los datos del lote que acabamos de calcular dentro de la tabla SQL
    cursor.execute("""
        INSERT INTO lotes (nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre_lote, inversion_total, piezas_vendibles, costo_real_unitario, precio_sugerido))
    
    # Guardamos los cambios (COMMIT) y cerramos la conexión para proteger el archivo
    conexion.commit()
    conexion.close()
    
    # 3. SALIDA EN PANTALLA
    print("\n=========================================")
    print("      ¡DATOS GUARDADOS EN LA BASE DE DATOS! ")
    print("=========================================")
    print(f"Lote registrado con éxito como: '{nombre_lote}'")
    print(f"Costo real por pieza vendible: ${costo_real_unitario:.2f}")
    print(f"Precio sugerido (50% margen): ${precio_sugerido:.2f}")
    print("=========================================")