# image-text-reader OCR

Lector de texto de imágenes con python

Para usar la librería "tesseract", es necesario instalarlo desde su repositorio oficial: https://github.com/UB-Mannheim/tesseract/wiki.
Además, hay que agregar el ejecutable a la variable path de las variables de entorno

## Archivos relevantes:

- main.py: Archivo principal de ejecución
- multiple_faces.jpg: imagen con varios rostros para probar la función: detect_faces()
- dividir y sacar text.jpg: imagen para probar la función: save_images()
- qr.png: imagen para probar la detección de códigos de barras y qrs en la función read_code()
- table_new: imagen para probar la extración de tablas en la función read_table()

### IMPORTANTE

Para usar las imágenes, se puede copiar el path relativo y copiarlo en la consola
