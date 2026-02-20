# Readers/HDF5ReaderAdapter.py
import pandas as pd
import logging
from typing import Dict, Any
from Readers.BaseReader import BaseReader
from Readers.HDF5PyReader import HDF5PyReader

class HDF5ReaderAdapter(BaseReader):
    def leer_archivo(self, ruta: str) -> Dict[str, Any]:
        errores = []
        try:
            with HDF5PyReader(ruta) as reader:
                # Obtener DataFrame consolidado
                tabla = reader.get_consolidated_dataframe()
                # Metadata básica para la consolidada
                texto = f"Archivo HDF5 cargado: {len(tabla)} filas de datos consolidados."
                logging.info(f"HDF5 cargado exitosamente: {ruta}")
                
                # Crear diccionario de tablas: consolidada + por Source
                tablas = {'consolidado': tabla}
                if 'Source' in tabla.columns:
                    grouped = tabla.groupby('Source')
                    for source, df in grouped:
                        # Quitar la columna 'Source' en las tablas individuales (redundante)
                        tablas[str(source)] = df.drop(columns=['Source'])
                
                return {'texto': texto, 'tablas': tablas, 'errores': errores}
        except Exception as e:
            errores.append(f"Error al leer HDF5: {str(e)}")
            logging.error(f"Error en HDF5: {e}")
            return {'texto': '', 'tablas': {}, 'errores': errores}

    def get_file_filter(self) -> str:
        return "Archivos HDF5 (*.hdf5 *.h5);;Todos los archivos (*)"