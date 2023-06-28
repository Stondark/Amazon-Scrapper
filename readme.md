# Amazon scrapper!
*Este proyecto es una aplicación de web scraping construida con FastAPI en Python. Permite a los usuarios extraer información de productos de Amazon proporcionando una URL válida del producto.*

**Instalación**

 1. Clonar el repositorio: 

> `git clone https://github.com/Stondark/Amazon-Scrapper.git`
 1. Instalar las dependencias: 
>`pip install -r requirements.txt`
 2. Ejecutar el servidor
>`uvicorn app:app`
 4. Realizar una solicitud POST al endpoint `/product` con un JSON que contenga la URL del producto:
>`POST /product HTTP/1.1 Host: localhost:8000 Content-Type: application/json { "url": "https://www.amazon.com/ejemplo-producto" }`