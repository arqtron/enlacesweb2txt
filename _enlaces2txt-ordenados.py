import os
import glob

# Ruta de la carpeta actual donde se encuentra el script
folder_path = os.path.dirname(os.path.realpath(__file__))
# Extensión de los accesos directos
shortcut_extension = '*.url'

# Archivo de salida donde se guardarán los nombres de los archivos y las URLs
output_file = 'accesos_directos.txt'

# Encuentra todos los archivos con la extensión de acceso directo en la carpeta actual
shortcut_files = glob.glob(os.path.join(folder_path, shortcut_extension))

# Ordena los archivos por fecha de creación (el más reciente primero)
shortcut_files.sort(key=lambda x: os.path.getctime(x), reverse=True)

# Abre el archivo de salida en modo de escritura con codificación utf-8
with open(output_file, 'w', encoding='utf-8') as file:
    # Itera sobre cada archivo de acceso directo
    for shortcut in shortcut_files:
        # Obtiene el nombre del archivo sin la extensión
        shortcut_name = os.path.basename(shortcut).replace('.url', '')
        # Abre el archivo de acceso directo en modo de lectura
        with open(shortcut, 'r', encoding='utf-8') as link:
            # Busca la URL dentro del archivo
            for line in link:
                if line.startswith('URL='):
                    # Escribe el nombre del archivo y la URL en el archivo de salida
                    file.write(f'{shortcut_name}\n{line.replace("URL=", "")}\n')

print(f'Se han extraído los nombres y las URLs al archivo {output_file}')
import os
import glob

# Ruta de la carpeta actual donde se encuentra el script
folder_path = os.path.dirname(os.path.realpath(__file__))
# Extensión de los accesos directos
shortcut_extension = '*.url'

# Archivo de salida donde se guardarán los nombres de los archivos y las URLs
output_file = 'accesos_directos.txt'

# Encuentra todos los archivos con la extensión de acceso directo en la carpeta actual
shortcut_files = glob.glob(os.path.join(folder_path, shortcut_extension))

# Ordena los archivos por fecha de creación (el más reciente primero)
shortcut_files.sort(key=lambda x: os.path.getctime(x), reverse=True)

# Abre el archivo de salida en modo de escritura con codificación utf-8
with open(output_file, 'w', encoding='utf-8') as file:
    # Itera sobre cada archivo de acceso directo
    for shortcut in shortcut_files:
        # Obtiene el nombre del archivo sin la extensión
        shortcut_name = os.path.basename(shortcut).replace('.url', '')
        # Abre el archivo de acceso directo en modo de lectura
        with open(shortcut, 'r', encoding='utf-8') as link:
            # Busca la URL dentro del archivo
            for line in link:
                if line.startswith('URL='):
                    # Escribe el nombre del archivo y la URL en el archivo de salida
                    file.write(f'{shortcut_name}\n{line.replace("URL=", "")}\n')

print(f'Se han extraído los nombres y las URLs al archivo {output_file}')