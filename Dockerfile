# Usa una imagen base de Python
FROM python:3.11.9-bullseye

# Crea un usuario para ejecutar la aplicación
RUN useradd --create-home --home-dir /home/flaskapp flaskapp

# Establece el directorio de trabajo en /home/flaskapp
WORKDIR /home/flaskapp

# Copia los archivos de la aplicación
COPY ./app.py .
COPY ./requirements.txt .
COPY ./pricebtc.py .

# on las siguientes dos lineas he creado un nuevo directorio en mi contenedor que es donde
# necesito guardar el dashboard
RUN mkdir -p templates
COPY ./templates/dashboard.html templates/

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación va a correr
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
