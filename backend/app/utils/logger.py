import logging

# Crear el logger
logger = logging.getLogger('api-cantonica')
logger.setLevel(logging.DEBUG)

# Crear un formateador
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Crear un manejador para escribir los registros en un archivo
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crear un manejador para mostrar los registros en la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)