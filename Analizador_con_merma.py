# =====================================================================
# PROYECTO: ANALIZADOR INTERACTIVO DE LOTES DE MERCANCÍA (FASE 2)
# OBJETIVO: Calcular costos reales incluyendo la MERMA del lote.
# =====================================================================

print("=========================================")
print("   SISTEMA DE MARGENES CON MERMA (F2)   ")
print("=========================================\n")

# 1. ENTRADA DE DATOS
costo_lote = float(input("¿Cuánto cuesta el lote completo ($)? "))
num_piezas = int(input("¿Cuántas piezas trae el lote en total? "))
costo_envio = float(input("¿Cuánto te cobran de envío ($)? "))
# Nueva pregunta para el colmillo de negocio:
merma = int(input("¿Cuántas piezas estimas de MERMA (defectuosas/no vendibles)?: "))

# 2. PROCESAMIENTO MODIFICADO (Lógica de negocio)
inversion_total = costo_lote + costo_envio

# Restamos la merma de las piezas totales para saber cuántas piezas SÍ van a generar dinero
piezas_vendibles = num_piezas - merma

# El costo real por pieza ahora se divide SOLO entre las piezas que sí vas a vender
costo_real_unitario = inversion_total / piezas_vendibles

# 3. CÁLCULO DE MÁRGENES (Sobre el nuevo costo real)
precio_margen_40 = costo_real_unitario / (1 - 0.40)
precio_margen_50 = costo_real_unitario / (1 - 0.50)
precio_margen_60 = costo_real_unitario / (1 - 0.60)

# 4. SALIDA DE DATOS
print("\n=========================================")
print("           REPORTE DE ANALISIS           ")
print("=========================================")
print(f"-> Inversión Total Real (Lote + Envío): ${inversion_total:.2f}")
print(f"-> Total piezas en lote: {num_piezas} | Piezas vendibles: {piezas_vendibles}")
print(f"-> Costo Real por Pieza VENDIBLE: ${costo_real_unitario:.2f}")
print("-----------------------------------------")
print("PRECIOS SIFERENCIADOS PARA RECUPERAR MERMA:")
print(f"[*] Para ganar el 40% de margen: Vender en ${precio_margen_40:.2f}")
print(f"[*] Para ganar el 50% de margen: Vender en ${precio_margen_50:.2f}")
print(f"[*] Para ganar el 60% de margen: Vender en ${precio_margen_60:.2f}")
print("=========================================")