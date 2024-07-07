# enlacesweb2txt
## Programa Python para Accesos Directos

Este programa en Python está diseñado para buscar y organizar los accesos directos de Internet (archivos `.url`) que se encuentran en la misma carpeta que el script. 

El script en Python busca archivos de acceso directo (`.url`) en la carpeta del script, extrae sus nombres y URLs, y los guarda en un archivo de texto. Ordena los accesos directos por fecha de creación y escribe los resultados en (`accesos_directos.txt`).

1. **Importa los módulos necesarios**: `os` para interactuar con el sistema operativo y `glob` para buscar archivos que coincidan con un patrón específico.
2. **Define la ruta de la carpeta actual** donde se ejecuta el script y la extensión de los archivos de acceso directo que busca (`.url`).
3. **Crea un archivo de salida** (`accesos_directos.txt`) donde se guardarán los nombres de los archivos de acceso directo y las URLs correspondientes.
4. **Busca todos los archivos `.url`** en la carpeta actual y los almacena en una lista.
5. **Ordena los archivos** encontrados por fecha de creación, del más reciente al más antiguo.
6. **Abre el archivo de salida** en modo de escritura y procede a iterar sobre cada archivo de acceso directo encontrado.
7. Para cada archivo `.url`, **obtiene el nombre del archivo** sin la extensión y luego busca dentro del archivo la línea que comienza con `URL=`, que contiene la dirección web.
8. **Escribe el nombre del archivo y la URL** encontrada en el archivo de salida.
9. Al final, **imprime un mensaje** en la consola informando que los nombres y las URLs se han extraído al archivo especificado.

El propósito de este script es facilitar la gestión de accesos directos, permitiendo al usuario tener un archivo de texto con una lista de todas las URLs y los títulos de las páginas web correspondientes.
