# Portafolio-Macro-Quant
# Motor Quant y Backtesting de Portafolio: Estrategia Top-Down Global Macro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://TU-LINK-DE-STREAMLIT.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Finanzas%20Cuantitativas-150458?style=for-the-badge&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit)

---

## Resumen del Proyecto y Generación de Alfa

Este proyecto documenta y sistematiza la gestión de un portafolio de inversión real (anonimizado en montos por confidencialidad), el cual logró **un rendimiento absoluto superior al 50%**. La selección de activos no se basó en movimientos aleatorios de mercado, sino en la ejecución disciplinada de una **Tesis Macroeconómica Top-Down**:

1. **Megatendencias Estructurales:** Inversión profunda en la infraestructura de Inteligencia Artificial (NVDA, MU, IXN) y la transición energética / renacimiento nuclear como cuello de botella del crecimiento cloud (VST, NLR).
2. **Coberturas Geopolíticas (Hedges):** Adquisición de activos defensivos del sector aeroespacial y de defensa (ITA) frente al escalamiento de tensiones globales.
3. **Gestión de Eventos Macro:** Estrategias tácticas de Dollar-Cost Averaging (DCA) condicionadas a la publicación de datos clave como el CPI (Inflación), NFP (Empleo) y decisiones de tasas de la Reserva Federal (FOMC).

---

## Arquitectura Técnica y Pipeline de Datos (ETL)

Para demostrar habilidades integrales de Data Engineering y Análisis Financiero, la construcción de este motor se dividió en tres fases técnicas automatizadas en Python:

### 1. Extracción de Datos No Estructurados (ETL y Regex)
Los brokers suelen emitir confirmaciones de compra en documentos de texto mixto o PDFs desestructurados. 
* **Solución:** Se desarrolló un script en Python que lee el archivo fuente bruto (`.docx`) y utiliza **Expresiones Regulares (Regex)** para segmentar fechas operativas y extraer los Tickers, volumen y precios de ejecución, exportando un archivo tabular estandarizado (`.csv`).

### 2. Conexión a API y Reconstrucción Vectorial (Pandas)
Para calcular la valuación del portafolio, es necesario un análisis de series de tiempo financieras diario.
* **Extracción de Precios:** Integración con la API de Wall Street mediante la librería `yfinance` para extraer los Precios de Cierre Ajustados (Adj Close) de todo el portafolio, considerando splits y dividendos.
* **Motor Matemático:** Mediante operaciones vectorizadas en `Pandas` (evitando ineficientes bucles for), se calculó una matriz de posiciones acumuladas cruzada contra la matriz de precios históricos. Esto permitió reconstruir con precisión milimétrica la curva de capital y rendimiento diario (Time-Series Analysis).

### 3. Despliegue de Interfaz Gráfica Institucional
* Se construyó un Dashboard interactivo usando **Streamlit** y **Plotly**.
* **Protección de Datos:** Se implementó una capa de ofuscación metodológica (escala fraccional) para exhibir métricas relativas (rendimiento %, Sharpe, pesos de diversificación) sin comprometer la privacidad del capital absoluto invertido.

---

## Estructura del Repositorio

```bash
├── etl_broker.py               # Script Regex para extracción de operaciones desde .docx
├── backtest_engine.py          # Motor Pandas para cruce de precios API vs Inventario
├── dashboard_portafolio.py     # Código fuente de la Web App en Streamlit
├── transacciones_anonimas.csv  # Base de datos escalada (Input)
├── rendimiento_portafolio.csv  # Series de tiempo de la valuación diaria
├── requirements.txt            # Dependencias para el despliegue en servidor
└── README.md                   # Documentación técnica
```

---

## Uso y Visualización

Puedes explorar la interactividad del portafolio, analizar la distribución táctica por sector y observar las anotaciones macroeconómicas en los puntos de inflexión del mercado directamente en la Web App desplegada:

**[Ver el Dashboard Interactivo Aquí](http://localhost:8501/)**

---

## Autor

* **Miguel Ángel Cortés Monge**
* **Perfil:** Econometrista, Analista de Datos y Financial Data Engineer
* **Áreas de Especialidad:** Análisis Macroeconómico Top-Down, ETL, Python, Finanzas Cuantitativas, Visualización de Datos Institucionales.
