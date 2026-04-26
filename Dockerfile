FROM python:3.10

# Carpeta de trabajo
WORKDIR /app

# Copiar todo el proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto de Hugging Face
EXPOSE 7860

# Ejecutar app
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:7860"]