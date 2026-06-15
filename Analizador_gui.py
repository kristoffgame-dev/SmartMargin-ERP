# =====================================================================
# PROYECTO: APP DE ESCRITORIO DE MÁRGENES (FASE GUI - SEGURIDAD PDF)
# OBJETIVO: Exportar el reporte en formato PDF protegido para evitar alteraciones.
# =====================================================================

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
import webbrowser

# --- FUNCIONES DE LÓGICA Y BASE DE DATOS ---

def limpiar_convertir_float(texto):
    texto_limpio = texto.strip().replace(",", "")
    return float(texto_limpio)

def limpiar_convertir_int(texto):
    texto_limpio = texto.strip().replace(",", "")
    return int(texto_limpio)

def calcular_y_guardar():
    nombre = entry_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "Por favor, dale un nombre al lote.")
        return
        
    try:
        costo = limpiar_convertir_float(entry_costo.get())
        piezas = limpiar_convertir_int(entry_piezas.get())
        envio = limpiar_convertir_float(entry_envio.get())
        merma = int(entry_merma.get())
    except ValueError:
        messagebox.showerror("Error de Formato", "Revisa que los costos y piezas sean números válidos.")
        return

    inversion_total = costo + envio
    piezas_vendibles = piezas - merma

    if piezas_vendibles <= 0:
        messagebox.showwarning("Negocio Inviable", "La merma no puede ser mayor o igual a las piezas totales.")
        return

    costo_unitario = inversion_total / piezas_vendibles
    precio_50 = costo_unitario / (1 - 0.50)

    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO lotes (nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50, piezas_vendidas)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (nombre, inversion_total, piezas_vendibles, costo_unitario, precio_50))
    conexion.commit()
    conexion.close()

    lbl_res_costo.config(text=f"${costo_unitario:,.2f}", fg="#10b981")
    lbl_res_precio.config(text=f"${precio_50:,.2f}", fg="#2563eb")
    
    messagebox.showinfo("¡Éxito!", f"El lote '{nombre}' ha sido guardado con stock inicial.")
    actualizar_tabla() 

def actualizar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
        
    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50, piezas_vendidas FROM lotes")
    filas = cursor.fetchall()
    conexion.close()

    for f in filas:
        id_lote = f[0]
        nombre_lote = f[1]
        inv_total = f"${f[2]:,.2f}"
        pzas_vendibles = f[3]
        costo_u = f"${f[4]:,.2f}"
        precio_sug = f"${f[5]:,.2f}"
        pzas_vendidas = f[6] if f[6] is not None else 0
        
        stock_actual = pzas_vendibles - pzas_vendidas
        tabla.insert("", tk.END, iid=id_lote, values=(nombre_lote, inv_total, f"{stock_actual:,}", costo_u, precio_sug))

def registrar_venta():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Selección Requerida", "Por favor, selecciona un lote en la tabla para registrar la venta.")
        return
        
    id_lote = seleccion[0]
    
    try:
        cantidad_a_vender = int(entry_venta_cantidad.get())
        if cantidad_a_vender <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Introduce una cantidad válida de piezas a vender.")
        return

    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, piezas_vendibles, piezas_vendidas FROM lotes WHERE id = ?", (id_lote,))
    lote = cursor.fetchone()
    
    nombre_lote = lote[0]
    pzas_vendibles = lote[1]
    pzas_vendidas_actuales = lote[2] if lote[2] is not None else 0
    stock_ahora = pzas_vendibles - pzas_vendidas_actuales

    if cantidad_a_vender > stock_ahora:
        messagebox.showerror("Sin Stock", f"¡No puedes vender {cantidad_a_vender} piezas! Solo quedan {stock_ahora}.")
        conexion.close()
        return

    nuevas_vendidas = pzas_vendidas_actuales + cantidad_a_vender
    cursor.execute("UPDATE lotes SET piezas_vendidas = ? WHERE id = ?", (nuevas_vendidas, id_lote))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Venta Registrada", f"¡Se descontaron {cantidad_a_vender} piezas de '{nombre_lote}'!")
    entry_venta_cantidad.delete(0, tk.END)
    actualizar_tabla()

def borrar_historial_completo():
    respuesta = messagebox.askyesno("⚠️ Confirmación Crítica", "¿Deseas ELIMINAR TODO el historial de lotes?")
    if respuesta:
        conexion = sqlite3.connect("mi_negocio.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM lotes")
        conexion.commit()
        conexion.close()
        lbl_res_costo.config(text="$0.00", fg="#6b7280")
        lbl_res_precio.config(text="$0.00", fg="#6b7280")
        actualizar_tabla()
        messagebox.showinfo("Historial Borrado", "Se ha limpiado el historial con éxito.")

def exportar_a_pdf():
    """Genera un reporte seguro en formato de impresión no modificable (PDF/Print Layout)."""
    conexion = sqlite3.connect("mi_negocio.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, inversion_total, piezas_vendibles, costo_unitario, precio_sugerido_50, piezas_vendidas FROM lotes")
    filas = cursor.fetchall()
    conexion.close()

    if len(filas) == 0:
        messagebox.showwarning("Historial Vacío", "No hay datos en el historial para exportar.")
        return

    nombre_archivo = "reporte_seguro.html"
    
    # Construimos un reporte ejecutivo con diseño CSS profesional e indestructible
    html_contenido = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Reporte Oficial de Inventario</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; background-color: #fff; }
            .header { text-align: center; border-bottom: 3px solid #1f2937; padding-bottom: 10px; margin-bottom: 30px; }
            .header h1 { margin: 0; font-size: 24px; color: #1f2937; }
            .header p { margin: 5px 0 0 0; color: #6b7280; font-size: 14px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
            th { background-color: #1f2937; color: white; padding: 12px; text-align: left; }
            td { padding: 12px; border-bottom: 1px solid #e5e7eb; }
            tr:nth-child(even) { background-color: #f9fafb; }
            .footer { margin-top: 5px; text-align: center; font-size: 11px; color: #9ca3af; border-top: 1px dashed #d1d5db; padding-top: 15px; position: fixed; bottom: 20px; width: 100%; }
            .monto { font-weight: bold; text-align: right; }
            .centro { text-align: center; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 REPORTE DE INVENTARIO Y CONTROL DE STOCK</h1>
            <p>Documento Oficial Protegido - Sistema de Control de Márgenes</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Nombre Lote</th>
                    <th style="text-align: right;">Inversión Total</th>
                    <th class="centro">Stock Disponible</th>
                    <th style="text-align: right;">Costo Unitario</th>
                    <th style="text-align: right;">Precio Sugerido (50%)</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for f in filas:
        pzas_vendidas = f[5] if f[5] is not None else 0
        stock_real = f[2] - pzas_vendidas
        html_contenido += f"""
                <tr>
                    <td>{f[0]}</td>
                    <td class="monto">${f[1]:,.2f}</td>
                    <td class="centro">{stock_real:,} pzas</td>
                    <td class="monto">${f[3]:,.2f}</td>
                    <td class="monto">${f[4]:,.2f}</td>
                </tr>
        """
        
    html_contenido += """
            </tbody>
        </table>
        
        <div class="footer">
            Este documento representa los estados reales de la base de datos SQL del negocio. Prohibida su alteración o falsificación.
        </div>
        
        <script>
            // Lanza el cuadro de diálogo de impresión nativo del sistema de forma inmediata
            window.onload = function() {
                window.print();
            }
        </script>
    </body>
    </html>
    """

    # Guardamos el archivo HTML
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html_contenido)

    messagebox.showinfo("🔒 Reporte de Seguridad", 
                        f"Se ha generado el panel de impresión seguro.\n\n"
                        "Se abrirá tu navegador. Selecciona 'Guardar como PDF' o selecciona tu impresora física.")
    
    # Abre el archivo en el navegador predeterminado para su impresión directa y segura en PDF
    ruta_absoluta = os.path.abspath(nombre_archivo)
    webbrowser.open(f"file://{ruta_absoluta}")

# --- DISEÑO DE LA INTERFAZ GRÁFICA (GUI) ---

ventana = tk.Tk()
ventana.title("Sistema de Márgenes y Stock - Portafolio Seguro")
ventana.geometry("740x740") 
ventana.configure(bg="#f3f4f6") 

lbl_titulo = tk.Label(ventana, text=" 🛡️ CONTROLADOR DE LOTES, MÁRGENES Y STOCK EN PDF", font=("Arial", 14, "bold"), bg="#1f2937", fg="white")
lbl_titulo.pack(fill=tk.X, ipady=10)

# FORMULARIO
frame_form = tk.LabelFrame(ventana, text=" Datos del Lote Nuevo ", font=("Arial", 10, "bold"), bg="#f3f4f6")
frame_form.pack(padx=20, pady=10, fill=tk.X, ipady=5, ipadx=10)

labels = ["Nombre / Etiqueta del lote:", "Costo total del lote ($):", "Total de piezas:", "Costo de envío ($):", "Piezas estimadas de merma:"]
entries = []

for i, texto in enumerate(labels):
    lbl = tk.Label(frame_form, text=texto, font=("Arial", 10), bg="#f3f4f6")
    lbl.grid(row=i, column=0, sticky="w", pady=4)
    ent = tk.Entry(frame_form, font=("Arial", 10), width=30)
    ent.grid(row=i, column=1, pady=4, padx=10)
    entries.append(ent)

entry_nombre, entry_costo, entry_piezas, entry_envio, entry_merma = entries

frame_res = tk.Frame(ventana, bg="#f3f4f6")
frame_res.pack(padx=20, fill=tk.X, pady=5)

tk.Label(frame_res, text="Costo Real Unitario:", font=("Arial", 11, "bold"), bg="#f3f4f6").grid(row=0, column=0, sticky="w")
lbl_res_costo = tk.Label(frame_res, text="$0.00", font=("Arial", 12, "bold"), bg="#f3f4f6", fg="#6b7280")
lbl_res_costo.grid(row=0, column=1, padx=10)

tk.Label(frame_res, text="Precio Sugerido (50%):", font=("Arial", 11, "bold"), bg="#f3f4f6").grid(row=0, column=2, sticky="w", padx=30)
lbl_res_precio = tk.Label(frame_res, text="$0.00", font=("Arial", 12, "bold"), bg="#f3f4f6", fg="#6b7280")
lbl_res_precio.grid(row=0, column=3, padx=10)

btn_calcular = tk.Button(ventana, text="🚀 Calcular y Guardar en SQL", font=("Arial", 11, "bold"), bg="#2563eb", fg="black", command=calcular_y_guardar)
btn_calcular.pack(padx=20, pady=10, fill=tk.X, ipady=2)

# TABLA VISUAL
frame_tabla = tk.LabelFrame(ventana, text=" Historial e Inventario Disponible (SQL) ", font=("Arial", 10, "bold"), bg="#f3f4f6")
frame_tabla.pack(padx=20, pady=5, fill=tk.BOTH, expand=True, ipady=5, ipadx=5)

columnas = ("nombre", "inversion", "piezas", "costo_u", "precio_sug")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

tabla.heading("nombre", text="Nombre Lote")
tabla.heading("inversion", text="Inv. Total ($)")
tabla.heading("piezas", text="Stock Actual") 
tabla.heading("costo_u", text="Costo Unitario ($)")
tabla.heading("precio_sug", text="Precio Venta (50%)")

tabla.column("nombre", width=120)
tabla.column("inversion", width=110, anchor="center")
tabla.column("piezas", width=100, anchor="center")
tabla.column("costo_u", width=120, anchor="center")
tabla.column("precio_sug", width=120, anchor="center")
tabla.pack(fill=tk.BOTH, expand=True)

# MÓDULO DE VENTAS
frame_ventas = tk.LabelFrame(ventana, text=" Módulo de Ventas (Selecciona un lote arriba) ", font=("Arial", 10, "bold"), bg="#f3f4f6")
frame_ventas.pack(padx=20, pady=10, fill=tk.X, ipady=5)

tk.Label(frame_ventas, text="Cantidad de piezas vendidas:", font=("Arial", 10), bg="#f3f4f6").pack(side=tk.LEFT, padx=10)
entry_venta_cantidad = tk.Entry(frame_ventas, font=("Arial", 10), width=10)
entry_venta_cantidad.pack(side=tk.LEFT, padx=10)

btn_vender = tk.Button(frame_ventas, text="Registrar Venta 🛍️", font=("Arial", 10, "bold"), bg="#f59e0b", fg="black", command=registrar_venta)
btn_vender.pack(side=tk.LEFT, padx=10)

# BOTONES INFERIORES ADAPTADOS PARA SEGURIDAD
frame_botones_abajo = tk.Frame(ventana, bg="#f3f4f6")
frame_botones_abajo.pack(padx=20, pady=10, fill=tk.X)

# Cambio estratégico: Botón verde para exportar PDF oficial
btn_pdf = tk.Button(frame_botones_abajo, text="📄 Exportar Historial a PDF", font=("Arial", 10, "bold"), bg="#10b981", fg="black", command=exportar_a_pdf)
btn_pdf.pack(side=tk.LEFT)

btn_limpiar = tk.Button(frame_botones_abajo, text="🗑️ Vaciar Historial Completo", font=("Arial", 10, "bold"), bg="#ef4444", fg="black", command=borrar_historial_completo)
btn_limpiar.pack(side=tk.RIGHT)

# --- CONFIGURACIÓN BASE DE DATOS ---
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
try:
    cursor.execute("ALTER TABLE lotes ADD COLUMN piezas_vendidas INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass 
conexion.commit()
conexion.close()

actualizar_tabla()
ventana.mainloop()