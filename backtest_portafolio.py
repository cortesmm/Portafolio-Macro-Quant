import pandas as pd
import numpy as np

print("⚙️ Iniciando el motor de reconstrucción del portafolio...")

# ==========================================
# 1. CARGAR BASES DE DATOS
# ==========================================
df_transacciones = pd.read_csv("transacciones_anonimas.csv")
df_transacciones['Fecha'] = pd.to_datetime(df_transacciones['Fecha'])

# Leemos los precios y convertimos la columna 'Date' en el índice de tiempo
df_precios = pd.read_csv("precios_historicos.csv", index_col="Date", parse_dates=True)

# ==========================================
# 2. CREAR MATRIZ DE POSICIONES (INVENTARIO)
# ==========================================
# Creamos una tabla llena de ceros con la misma forma que df_precios
df_posiciones = pd.DataFrame(0.0, index=df_precios.index, columns=df_precios.columns)
df_capital = pd.DataFrame(0.0, index=df_precios.index, columns=['Aportaciones_Acumuladas'])

aportacion_total = 0.0

# Iteramos sobre cada transacción para sumar las acciones a nuestro inventario
for _, operacion in df_transacciones.iterrows():
    fecha = operacion['Fecha']
    ticker = operacion['Ticker']
    titulos = operacion['Titulos']
    precio_compra = operacion['Precio_Ejecucion']
    accion = operacion['Accion']
    
    # Si la fecha de compra cae en fin de semana, la movemos al siguiente día hábil
    if fecha not in df_posiciones.index:
        fechas_futuras = df_posiciones.index[df_posiciones.index >= fecha]
        if not fechas_futuras.empty:
            fecha = fechas_futuras.min()
        else:
            continue
            
    # Sumamos los títulos desde el día de la compra hasta el futuro
    if accion.lower() == 'buy':
        df_posiciones.loc[fecha:, ticker] += titulos
        # Sumamos el costo de la compra a nuestro capital invertido
        aportacion_total += (titulos * precio_compra)
        df_capital.loc[fecha:, 'Aportaciones_Acumuladas'] = aportacion_total

# ==========================================
# 3. VALUACIÓN DIARIA DEL PORTAFOLIO
# ==========================================
# ¡La magia de Pandas! Multiplicamos la matriz de acciones por la matriz de precios
df_valor_activos = df_posiciones * df_precios

# Sumamos el valor de todas las acciones fila por fila (día por día)
df_rendimiento = pd.DataFrame(index=df_precios.index)
df_rendimiento['Valor_Portafolio'] = df_valor_activos.sum(axis=1)
df_rendimiento['Capital_Invertido'] = df_capital['Aportaciones_Acumuladas']

# Calculamos el % de rendimiento diario
df_rendimiento['Rendimiento_%'] = ((df_rendimiento['Valor_Portafolio'] / df_rendimiento['Capital_Invertido']) - 1) * 100

# Limpiamos valores infinitos o NaN iniciales
df_rendimiento = df_rendimiento.dropna()

# Guardamos el resultado final
df_rendimiento.to_csv("rendimiento_portafolio.csv")

print("✅ Reconstrucción completada. Datos guardados en 'rendimiento_portafolio.csv'.")
print("\n📊 Resumen Actual de tu Portafolio:")
print(f"Capital Total Invertido: ${df_rendimiento['Capital_Invertido'].iloc[-1]:,.2f}")
print(f"Valor Actual del Portafolio: ${df_rendimiento['Valor_Portafolio'].iloc[-1]:,.2f}")
print(f"Rendimiento Histórico: {df_rendimiento['Rendimiento_%'].iloc[-1]:.2f}%")