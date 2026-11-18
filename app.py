import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página para vista móvil
st.set_page_config(page_title="Control de Gastos", page_icon="💰", layout="centered")

ARCHIVO = "gastos.csv"

# Inicializar base de datos local (CSV) si no existe, incluyendo la columna Método de Pago
if not os.path.exists(ARCHIVO):
    df_init = pd.DataFrame(columns=["Fecha", "Tipo", "Metodo_Pago", "Descripcion", "Monto"])
    df_init.to_csv(ARCHIVO, index=False)

# Cargar datos
df = pd.read_csv(ARCHIVO)

# Asegurar compatibilidad por si el CSV viejo no tenía la columna
if "Metodo_Pago" not in df.columns:
    df["Metodo_Pago"] = "Efectivo"

st.title("📱 Mi Billetera en Python")

# Calcular balance total
balance = 0
if not df.empty:
    for _, row in df.iterrows():
        if row["Tipo"] == "Ingreso":
            balance += row["Monto"]
        else:
            balance -= row["Monto"]

# Mostrar balance con colores
if balance >= 0:
    st.success(f"### Balance Total: ${balance:.2f}")
else:
    st.error(f"### Balance Total: ${balance:.2f}")

# Formulario para registrar ingresos o gastos
with st.form("form_movimiento", clear_on_submit=True):
    st.subheader("Agregar Movimiento")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    
    # Nuevo campo: Método de Pago
    metodo_pago = st.selectbox("Método de Pago", [
        "Efectivo", 
        "Tarjeta de Débito", 
        "Tarjeta de Crédito", 
        "Transferencia", 
        "Mercado Pago", 
        "Otro"
    ])
    
    descripcion = st.text_input("Descripción (ej. Supermercado, Sueldo)")
    monto = st.number_input("Monto ($)", min_value=0.01, format="%.2f")
    
    enviar = st.form_submit_button("Registrar")

    if enviar:
        if descripcion.strip() == "":
            st.warning("Por favor escribe una descripción.")
        else:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            nuevo = pd.DataFrame([[fecha, tipo, metodo_pago, descripcion, monto]], 
                                  columns=["Fecha", "Tipo", "Metodo_Pago", "Descripcion", "Monto"])
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(ARCHIVO, index=False)
            st.success("¡Movimiento guardado con éxito!")
            st.rerun()

# Historial de movimientos
st.markdown("---")
st.subheader("📋 Movimientos Recientes")

if not df.empty:
    # Mostrar del más nuevo al más viejo
    st.dataframe(df.iloc[::-1], use_container_width=True)
else:
    st.info("Aún no hay registros en tu base de datos.")
