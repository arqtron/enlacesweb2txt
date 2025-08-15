#!/usr/bin/env python3
"""
Script para extraer y ordenar enlaces de archivos .url de Windows.
Extrae el nombre del archivo y la URL, ordenándolos por fecha de creación.
"""

import os
import glob
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime


class URLExtractor:
    """Clase para extraer URLs de archivos .url de Windows."""
    
    def __init__(self, folder_path: str = None, output_file: str = 'accesos_directos.txt'):
        """
        Inicializa el extractor de URLs.
        
        Args:
            folder_path: Ruta de la carpeta a procesar (por defecto la actual)
            output_file: Nombre del archivo de salida
        """
        self.folder_path = Path(folder_path) if folder_path else Path(__file__).parent
        self.output_file = self.folder_path / output_file
        self.shortcut_extension = '*.url'
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('url_extractor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def find_shortcut_files(self) -> List[Path]:
        """
        Encuentra todos los archivos .url en la carpeta especificada.
        
        Returns:
            Lista de rutas de archivos .url ordenados por fecha de creación
        """
        try:
            pattern = self.folder_path / self.shortcut_extension
            shortcut_files = [Path(f) for f in glob.glob(str(pattern))]
            
            if not shortcut_files:
                self.logger.warning(f"No se encontraron archivos .url en {self.folder_path}")
                return []
            
            # Ordenar por fecha de creación (más reciente primero)
            shortcut_files.sort(key=lambda x: x.stat().st_ctime, reverse=True)
            
            self.logger.info(f"Encontrados {len(shortcut_files)} archivos .url")
            return shortcut_files
            
        except Exception as e:
            self.logger.error(f"Error al buscar archivos .url: {e}")
            return []
    
    def extract_url_from_file(self, file_path: Path) -> Optional[str]:
        """
        Extrae la URL de un archivo .url.
        
        Args:
            file_path: Ruta del archivo .url
            
        Returns:
            URL extraída o None si hay error
        """
        try:
            # Intentar diferentes codificaciones
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        for line in file:
                            line = line.strip()
                            if line.startswith('URL='):
                                url = line.replace('URL=', '', 1).strip()
                                if url:  # Verificar que la URL no esté vacía
                                    return url
                    break  # Si llegamos aquí, la codificación funcionó
                except UnicodeDecodeError:
                    continue  # Probar siguiente codificación
                    
            self.logger.warning(f"No se pudo encontrar URL válida en {file_path.name}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error al leer {file_path.name}: {e}")
            return None
    
    def process_shortcuts(self) -> List[Tuple[str, str, str]]:
        """
        Procesa todos los archivos .url y extrae la información.
        
        Returns:
            Lista de tuplas (nombre, url, fecha_creacion)
        """
        shortcut_files = self.find_shortcut_files()
        results = []
        
        for shortcut_path in shortcut_files:
            try:
                # Obtener nombre sin extensión
                shortcut_name = shortcut_path.stem
                
                # Extraer URL
                url = self.extract_url_from_file(shortcut_path)
                
                if url:
                    # Obtener fecha de creación formateada
                    creation_time = shortcut_path.stat().st_ctime
                    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                    
                    results.append((shortcut_name, url, creation_date))
                    self.logger.debug(f"Procesado: {shortcut_name} -> {url}")
                
            except Exception as e:
                self.logger.error(f"Error al procesar {shortcut_path.name}: {e}")
                continue
        
        return results
    
    def write_results(self, results: List[Tuple[str, str, str]], include_date: bool = False) -> bool:
        """
        Escribe los resultados al archivo de salida.
        
        Args:
            results: Lista de tuplas (nombre, url, fecha)
            include_date: Si incluir la fecha de creación en la salida
            
        Returns:
            True si se escribió correctamente, False en caso contrario
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write(f"# Enlaces extraídos - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"# Total de enlaces: {len(results)}\n\n")
                
                for name, url, date in results:
                    if include_date:
                        file.write(f"Nombre: {name}\n")
                        file.write(f"URL: {url}\n")
                        file.write(f"Fecha: {date}\n")
                        file.write("-" * 50 + "\n\n")
                    else:
                        file.write(f"{name}\n{url}\n\n")
            
            self.logger.info(f"Resultados escritos en {self.output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al escribir archivo de salida: {e}")
            return False
    
    def extract_urls(self, include_date: bool = False) -> bool:
        """
        Ejecuta el proceso completo de extracción.
        
        Args:
            include_date: Si incluir fechas en la salida
            
        Returns:
            True si el proceso fue exitoso
        """
        self.logger.info(f"Iniciando extracción en: {self.folder_path}")
        
        results = self.process_shortcuts()
        
        if not results:
            self.logger.warning("No se encontraron URLs válidas para extraer")
            return False
        
        success = self.write_results(results, include_date)
        
        if success:
            self.logger.info(f"Proceso completado. {len(results)} URLs extraídas.")
            print(f"\n✅ Se han extraído {len(results)} URLs al archivo '{self.output_file}'")
        
        return success


def main():
    """Función principal del script."""
    try:
        # Crear extractor con configuración por defecto
        extractor = URLExtractor()
        
        # Ejecutar extracción (cambiar include_date=True para incluir fechas)
        success = extractor.extract_urls(include_date=False)
        
        if not success:
            print("❌ El proceso no se completó correctamente. Revisar logs.")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    exit(main())