# =====================================================================
# PROYECTO: SISTEMA INTEGRAL DE ANALISIS DE LOTES (FASE 5 - FINAL)
# OBJETIVO: Menú interactivo para registrar y consultar datos en SQL.
# =====================================================================

import sqlite3

def crear_tabla():
    """Función para asegurar que la tabla SQL exista al arrancar."""
    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
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
    conexion.commit()
    conexion.close()

def analizar_lote_nuevo():
    """Función para calcular un lote y guardarlo (Fase 4)."""
    print("\n--- REGISTRAR NUEVO LOTE ---")
    while True:
        try:
            nombre_lote = input("Nombre/Etiqueta del lote: ")
            costo_lote = float(input("¿Costo del lote ($)?: "))
            num_piezas = int(input("¿Total de piezas?: "))
            costo_envio = float(input("¿Costo de envío ($)?: "))
            merma = int(input("¿Piezas de merma?: "))
            break
        except ValueError:
            print("[❌ ERROR] Usa solo números para costos y piezas.")

    inversion_total = costo_lote + costo_envio
    piezas_vendibles = num_piezas - merma

    if piezas_vendibles <= 0:
        print("[⚠️ ALERTA] Negocio inviable por exceso de merma.\n")
        return

    costo_real_unitario = inversion_total / piezas_vendibles
    precio_sugerido = costo_real_unitario / (1 - 0.50)

    # Guardar en SQL
    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO lotes (nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre_lote, inversion_total, piezas_vendibles, costo_real_unitario, precio_sugerido))
    conexion.commit()
    conexion.close()
    
    print(f"\n[✅] ¡Lote '{nombre_lote}' guardado con éxito en la Base de Datos!\n")

def ver_historial():
    """Función para LEER los datos guardados en la base de datos SQL."""
    print("\n=====================================================================")
    print("                 HISTORIAL DE LOTES EN BASE DE DATOS                 ")
    print("=====================================================================")
    
    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    
    # El comando SELECT * FROM nos trae todos los registros de la tabla
    cursor.execute("SELECT id, nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50 FROM lotes")
    filas = cursor.fetchall() # fetchall() recupera todas las filas encontradas
    
    conexion.close()

    if len(filas) == 0:
        print("Aún no hay lotes registrados en el historial.")
    else:
        # Imprimimos los encabezados de nuestra tabla en la terminal
        print(f"{'ID':<4} | {'NOMBRE':<15} | {'INV. TOTAL':<12} | {'PZAS VEND':<10} | {'COSTO U.':<10} | {'P. SUG (50%)':<12}")
        print("-" * 75)
        # Recorremos cada fila de la base de datos y la mostramos acomodada
        for fila in filas:
            print(f"{fila[0]:<4} | {fila[1]:<15} | ${fila[2]:<11.2f} | {fila[3]:<10} | ${fila[4]:<9.2f} | ${fila[5]:<11.2f}")
    print("=====================================================================\n")

# =====================================================================
# FLUJO PRINCIPAL DEL PROGRAMA (EL MENÚ)
# =====================================================================
crear_tabla() # Aseguramos la base de datos al inicio

while True:
    print("=== CONTROL DE INVENTARIO Y MÁRGENES ===")
    print("1. Analizar y Guardar Lote Nuevo")
    print("2. Ver Historial de Lotes Guardados")
    print("3. Salir del Programa")
    
    opcion = input("Selecciona una opción (1-3): ")
    
    if opcion == "1":
        analizar_lote_nuevo()
    elif opcion == "2":
        ver_historial()
    elif opcion == "3":
        print("\n¡Gracias por usar el sistema! Desarrollado para el portafolio. ¡Hasta luego!")
        break
    else:
        print("\n[❌] Opción no válida. Intenta de nuevo.\n")