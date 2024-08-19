import os
import processing
from qgis.core import QgsRasterLayer

def obtener_numero_bandas(raster_path):
    """Obtiene el número de bandas del archivo raster."""
    raster_layer = QgsRasterLayer(raster_path, 'NDWI')
    return raster_layer.bandCount()

def verificar_y_procesar_shapefile(output_folder, nombre_shape, input_shapefile, input_raster):
    """Verifica si el shapefile existe y lo procesa si no existe."""
    shape_path = os.path.join(output_folder, f"{nombre_shape}.shp")
    
    if not os.path.exists(shape_path):
        print(f"El archivo {nombre_shape}.shp NO existe en la carpeta. Procesando...")
        parametros = {
            'INPUT': input_shapefile,
            'INPUT_RASTER': input_raster,
            'RASTER_BAND': 1,
            'COLUMN_PREFIX': '_1',
            'STATISTICS': [2, 3, 4],
            'OUTPUT': shape_path
        }
        processing.run("native:zonalstatisticsfb", parametros)
    else:
        print(f"El archivo {nombre_shape}.shp ya existe en la carpeta.")

def procesar_bandas(output_folder, input_raster, num_bands, input_shapefile):
    """Procesa estadísticas zonales para todas las bandas del raster."""
    for band in range(2, num_bands + 1):
        input_path2 = os.path.join(output_folder, f'TEMPORARY_OUTPUT_{band-1}.shp')
        output_path2 = os.path.join(output_folder, f'TEMPORARY_OUTPUT_{band}.shp')

        if os.path.exists(input_path2):
            parametros = {
                'INPUT': input_path2,
                'INPUT_RASTER': input_raster,
                'RASTER_BAND': band,
                'COLUMN_PREFIX': f'_{band}',
                'STATISTICS': [2, 3, 4],
                'OUTPUT': output_path2
            }
            processing.run("native:zonalstatisticsfb", parametros)
        else:
            print(f"El archivo {input_path2} no existe. No se puede procesar la banda {band}.")

# Definir los caminos de los archivos
input_shapefile = 'D:/Trabajo/Tesis/Carpeta indices/AreasAfecatdas/AreasAfec.shp'
input_raster = 'D:/Trabajo/Tesis/Carpeta indices/Indices/SAVI_mul2.tif'
output_folder = r'D:\Trabajo\Tesis\Carpeta indices\Indices\SAVI\Estadisticas'

nombre_shape = "TEMPORARY_OUTPUT_1"

# Obtener el número de bandas del raster
num_bands = obtener_numero_bandas(input_raster)

# Verificar y procesar el shapefile inicial
verificar_y_procesar_shapefile(output_folder, nombre_shape, input_shapefile, input_raster)

# Procesar las bandas
procesar_bandas(output_folder, input_raster, num_bands, input_shapefile)

    
    
    

