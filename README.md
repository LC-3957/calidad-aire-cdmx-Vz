# Proyecto: ¿Respiramos peor los lunes?

**Autor:** Lyzzet Valenzuela Cabello

**Proyecto Final - Visualizacion Grafica para IA**
**Universidad Iberoamericana Leon**

---

## Descripcion del proyecto

Aplicacion interactiva que analiza patrones de contaminacion del aire en la Ciudad de Mexico (2011-2021) usando datos oficiales de SEDEMA. El proyecto responde a la pregunta: ¿Respiramos peor los lunes?

### Hallazgo principal

Aunque el trafico es mayor entre semana, el peor aire se registra el domingo, debido a la formacion de ozono a partir de emisiones acumuladas de dias anteriores.

### Visualizaciones incluidas

- NO2: Trafico en tiempo real (sale del escape) - Color verde
- Ozono: Daño respiratorio (se forma con el sol) - Color naranja
- PM2.5: Particulas finas que dañan los pulmones - Color rojo

---

## Fuente de datos

- **Institucion:** SEDEMA · Sistema de Monitoreo Atmosferico (SIMAT) · Datos Abiertos CDMX
- **URL exacta:** https://repositorio-salud.conacyt.mx/jspui/handle/1000/235
- **Fecha de descarga:** 25 Abril 2026
- **Periodo de los datos:** 2011 – 2021
- **Volumen:** 3.5 millones de registros · 69 estaciones de monitoreo
- **Licencia:** Datos abiertos del gobierno de la Ciudad de Mexico

---

## Aplicacion en linea

https://huggingface.co/spaces/vcLy2/calidad-aire-mexico

---

## Tecnologias utilizadas

- Python 3.10 - Lenguaje principal
- Dash - Framework para la aplicacion web
- Plotly - Visualizaciones interactivas
- Pandas - Limpieza y procesamiento de datos
- Docker - Contenedor para despliegue
- Hugging Face Spaces - Plataforma de despliegue

---

## Estructura del repositorio
proyecto/
├── codigo/
│ ├── app.py # Aplicacion Dash principal
│ ├── data_loader.py # Carga y procesamiento de datos
│ └── assets/
│ └── style.css # Estilos personalizados
├── datos_procesados/ # Archivos CSV limpios
├── docs/
│ └── narrativa.md # Analisis narrativo completo
├── Dockerfile # Configuracion para despliegue
├── requirements.txt # Dependencias de Python
└── README.md 

## Instrucciones para ejecutar LOCALMENTE

### Requisitos previos

- Python 3.10 o superior
- Git

### Pasos para ejecutar
1. Clonar el repositorio

- git clone https://github.com/LC-3957/calidad-aire-cdmx-Vz.git
- cd calidad-aire-mexico

2. Crear y activar entorno virtual

- python -m venv venv
- source venv/bin/activate # En Linux/Mac
- venv\Scripts\activate # En Windows

3. Instalar dependencias

- pip install -r requirements.txt

4. Modificar app.py al final 

    Cambiar esto:

    if __name__ == '__main__':

        app.run(host='0.0.0.0', port=7860)

    Por esto: 

    if __name__ == '__main__':

        app.run(host='127.0.0.1', port=8050)


5. Ejecutar la aplicacion

- cd codigo
- python app.py
- Abrir en el navegador: `http://127.0.0.1:8050`

---

- La aplicacion debe mostrar tres visualizaciones interactivas
- El selector de contaminante debe cambiar los datos del ranking
- Los hover deben mostrar valores detallados

---

## Narrativa completa

El analisis detallado, incluyendo:
- Pregunta central de investigacion
- Publico objetivo
- Justificacion de cada visualizacion
- Hallazgos y conclusion

Se encuentra en: `/docs/narrativa.md`

---

## Nota para la profesora

Este repositorio es [publico].

---

*Proyecto final para la materia de Visualizacion Grafica para IA*
*Universidad Iberoamericana Leon *