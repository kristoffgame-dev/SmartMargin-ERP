# =====================================================================
# PROYECTO: ANALIZADOR INTERACTIVO DE LOTES DE MERCANCÍA (FASE 1)
# OBJETIVO: Calcular costos reales y márgenes de ganancia para menudeo.
# =====================================================================

print("=========================================")
print("   BIENVENIDO AL SISTEMA DE MARGENES   ")
print("=========================================\n")

# 1. ENTRADA DE DATOS (Capturando la información del negocio)
# Usamos float() e int() para transformar el texto que escribe el usuario en números.
costo_lote = float(input("¿Cuánto cuesta el lote completo ($)? "))
num_piezas = int(input("¿Cuántas piezas trae el lote? "))
costo_envio = float(input("¿Cuánto te cobran de envío ($)? "))

# 2. PROCESAMIENTO (La matemática del Libro Diario)
# Sumamos el envío al costo del lote y lo dividimos entre las piezas para sacar el costo real puesto en casa.
inversion_total = costo_lote + costo_envio
costo_real_unitario = inversion_total / num_piezas

# 3. CÁLCULO DE MÁRGENES (Usando la fórmula que aprendimos)
# Fórmula: Costo / (1 - Margen en decimal)
precio_margen_40 = costo_real_unitario / (1 - 0.40)
precio_margen_50 = costo_real_unitario / (1 - 0.50)
precio_margen_60 = costo_real_unitario / (1 - 0.60)

# 4. SALIDA DE DATOS (Mostrando los resultados en el Libro Mayor)
print("\n=========================================")
print("           REPORTE DE ANALISIS           ")
print("=========================================")
print(f"-> Inversión Total Real (Lote + Envío): ${inversion_total:.2f}")
print(f"-> Costo Real por Pieza (Puesto en Casa): ${costo_real_unitario:.2f}")
print("-----------------------------------------")
print("PRECIOS DE VENTA SUGERIDOS PARA MENUDEO:")
print(f"[*] Para ganar el 40% de margen: Vender en ${precio_margen_40:.2f}")
print(f"[*] Para ganar el 50% de margen: Vender en ${precio_margen_50:.2f}")
print(f"[*] Para ganar el 60% de margen: Vender en ${precio_margen_60:.2f}")
print("=========================================")