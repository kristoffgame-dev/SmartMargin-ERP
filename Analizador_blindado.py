# =====================================================================
# PROYECTO: ANALIZADOR INTERACTIVO DE LOTES (FASE 3 - BLINDADO)
# OBJETIVO: Evitar que el programa truene si el usuario escribe letras.
# =====================================================================

print("=========================================")
print("   SISTEMA DE MARGENES BLINDADO (F3)   ")
print("=========================================\n")

# Usamos un ciclo infinito 'while True' que solo se detendrá cuando los datos sean correctos
while True:
    try:
        # El programa INTENTA ejecutar estas líneas
        costo_lote = float(input("¿Cuánto cuesta el lote completo ($)? "))
        num_piezas = int(input("¿Cuántas piezas trae el lote en total? "))
        costo_envio = float(input("¿Cuánto te cobran de envío ($)? "))
        merma = int(input("¿Cuántas piezas estimas de MERMA?: "))
        
        # Si todo se introduce como número, este 'break' rompe el ciclo y continúa hacia abajo
        break
        
    except ValueError:
        # SI EL USUARIO ESCRIBE LETRAS, Python cacha el error aquí y evita que el programa truene
        print("\n[❌ ERROR] ¡Por favor introduce solo números! No uses letras, signos de pesos o comas.\n")
        print("Vamos a intentarlo de nuevo...\n")
        print("-----------------------------------------")

# 2. PROCESAMIENTO (Esta parte ya la dominas, solo corre si el 'while' terminó con éxito)
inversion_total = costo_lote + costo_envio
piezas_vendibles = num_piezas - merma

# Un candado extra: Evitar la división entre cero si la merma es igual o mayor a las piezas
if piezas_vendibles <= 0:
    print("\n[⚠️ ALERTA] Tu merma no puede ser igual o mayor al total de piezas. ¡Te quedarías sin negocio!")
else:
    costo_real_unitario = inversion_total / piezas_vendibles

    precio_margen_40 = costo_real_unitario / (1 - 0.40)
    precio_margen_50 = costo_real_unitario / (1 - 0.50)
    precio_margen_60 = costo_real_unitario / (1 - 0.60)

    # 4. SALIDA DE DATOS
    print("\n=========================================")
    print("           REPORTE DE ANALISIS           ")
    print("=========================================")
    print(f"-> Inversión Total Real (Lote + Envío): ${inversion_total:.2f}")
    print(f"-> Total piezas: {num_piezas} | Piezas vendibles: {piezas_vendibles}")
    print(f"-> Costo Real por Pieza VENDIBLE: ${costo_real_unitario:.2f}")
    print("-----------------------------------------")
    print("PRECIOS SUGERIDOS PARA MENUDEO:")
    print(f"[*] Para ganar el 40% de margen: Vender en ${precio_margen_40:.2f}")
    print(f"[*] Para ganar el 50% de margen: Vender en ${precio_margen_50:.2f}")
    print(f"[*] Para ganar el 60% de margen: Vender en ${precio_margen_60:.2f}")
    print("=========================================")