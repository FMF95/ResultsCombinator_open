import h5py
import pandas as pd
import os

class HDF5PyReader:
    def __init__(self, file_path):
        """
        Inicializa el lector con la ruta del archivo HDF5.
        Verifica la extensión y abre el archivo en modo lectura.
        """
        if not (file_path.endswith('.hdf5') or file_path.endswith('.h5')):
            raise ValueError("El archivo debe tener extensión .hdf5 o .h5")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        self.file_path = file_path
        self.file = h5py.File(file_path, 'r')
        self.dataframes = {}  # Diccionario para almacenar DataFrames por path de dataset
    
    def __enter__(self):
        """Permite usar la clase como context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el archivo automáticamente al salir del context manager."""
        self.close()
    
    def load_dataset_to_dataframe(self, dataset_path):
        """
        Carga un dataset específico en un DataFrame de pandas.
        Asume que el dataset es tabular (con campos nombrados).
        """
        if dataset_path not in self.file:
            raise KeyError(f"Dataset no encontrado: {dataset_path}")
        
        dataset = self.file[dataset_path]
        if not hasattr(dataset, 'dtype') or not dataset.dtype.names or len(dataset.dtype.names) == 0:
            raise ValueError(f"El dataset {dataset_path} no es tabular o no tiene campos nombrados")
        
        # Convertir a DataFrame
        data = {name: dataset[name] for name in dataset.dtype.names}
        df = pd.DataFrame(data)
        self.dataframes[dataset_path] = df
        return df
    
    def search_by_id(self, dataset_path, id_column, target_id):
        """
        Busca filas en el DataFrame de un dataset por ID.
        """
        if dataset_path not in self.dataframes:
            self.load_dataset_to_dataframe(dataset_path)
        
        df = self.dataframes[dataset_path]
        if id_column not in df.columns:
            raise ValueError(f"Columna '{id_column}' no encontrada en {dataset_path}")
        
        results = df[df[id_column] == target_id]
        return results
    
    def list_datasets(self):
        """
        Lista todos los datasets en el archivo HDF5.
        """
        def collect_datasets(name, obj):
            if isinstance(obj, h5py.Dataset):
                print(f"Dataset: {name}")
        
        self.file.visititems(collect_datasets)
    
    def is_tabular_dataset(self, dataset_path):
        """
        Verifica si un dataset es tabular (tiene campos nombrados).
        """
        if dataset_path not in self.file:
            return False
        dataset = self.file[dataset_path]
        return hasattr(dataset, 'dtype') and dataset.dtype.names and len(dataset.dtype.names) > 0
    
    def get_consolidated_dataframe(self, base_path="/OptiStruct/RESULT/"):
        """
        Crea un DataFrame consolidado con todos los datasets tabulares bajo la ruta base.
        Agrega una columna 'Source' para identificar el origen del dataset.
        Útil para obtener todos los datos en una sola llamada desde otras aplicaciones.
        """
        consolidated_dfs = []
        
        def collect_tabular_datasets(name, obj):
            if isinstance(obj, h5py.Dataset) and hasattr(obj, 'dtype') and obj.dtype.names:
                full_path = f"/{name}"
                if full_path.startswith(base_path):
                    try:
                        df = self.load_dataset_to_dataframe(full_path)
                        df['Source'] = full_path  # Agregar columna para identificar origen
                        consolidated_dfs.append(df)
                    except Exception as e:
                        print(f"Advertencia: No se pudo cargar {full_path}: {e}")
        
        self.file.visititems(collect_tabular_datasets)
        
        if not consolidated_dfs:
            raise ValueError(f"No se encontraron datasets tabulares bajo {base_path}")
        
        # Concatenar todos los DataFrames
        consolidated_df = pd.concat(consolidated_dfs, ignore_index=True)
        return consolidated_df

    def close(self):
        """Cierra el archivo HDF5."""
        self.file.close()

# Función para uso interactivo cuando se ejecuta el script directamente
def interactive_search():
    file_path = input("Ingresa la ruta del archivo HDF5 (.hdf5 o .h5): ").strip()
    if not file_path:
        print("Error: La ruta del archivo no puede estar vacía.")
        return
    
    try:
        with HDF5PyReader(file_path) as reader:
            print("Datasets disponibles:")
            reader.list_datasets()
            
            while True:
                dataset_path = input("Ingresa el path del dataset (o 'exit' para salir): ").strip()
                if dataset_path.lower() == 'exit':
                    break
                if not dataset_path:
                    print("Error: El path del dataset no puede estar vacío. Intenta de nuevo.")
                    continue
                
                if not reader.is_tabular_dataset(dataset_path):
                    print(f"Error: El dataset {dataset_path} no es tabular o no existe.")
                    continue
                
                try:
                    df = reader.load_dataset_to_dataframe(dataset_path)
                    print(f"DataFrame cargado para {dataset_path}:")
                    print(df.head())  # Muestra las primeras filas
                    
                    id_column = input("Ingresa el nombre de la columna ID (o presiona Enter para saltar): ").strip()
                    if id_column:
                        target_id_str = input("Ingresa el ID a buscar: ").strip()
                        if not target_id_str:
                            print("Error: El ID no puede estar vacío. Intenta de nuevo.")
                            continue
                        try:
                            target_id = int(target_id_str)
                            results = reader.search_by_id(dataset_path, id_column, target_id)
                            print(f"Resultados para ID {target_id}:")
                            print(results)
                        except ValueError:
                            print("Error: El ID debe ser un número entero. Intenta de nuevo.")
                        except Exception as e:
                            print(f"Error al buscar por ID: {e}")
                    else:
                        print("Búsqueda por ID omitida.")
                except Exception as e:
                    print(f"Error inesperado al procesar el dataset: {e}")
    
    except FileNotFoundError:
        print("Error: Archivo no encontrado. Verifica la ruta.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

if __name__ == "__main__":
    interactive_search()