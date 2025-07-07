import os
import rasterio

# Archivo para generar stacks de índices multibanda (NDVI, NDBI, UI)
# Se usará para ML y visualización de datos en python

def make_index_stack(date, base_dir, out_dir):
    """
    Crea un TIFF multibanda (NDVI, NDBI, UI) para la carpeta de la fecha dada.
    
    - date: 'YYYY-MM-DD', nombre de la subcarpeta y prefijo de los TIFFs
    - base_dir: ruta al directorio que contiene carpetas 'YYYY-MM-DD'
    - out_dir: ruta donde guardar los stacks
    """
    # Rutas de entrada (dentro de la carpeta de la fecha)
    folder    = os.path.join(base_dir, date)
    ndvi_path = os.path.join(folder, f"{date}_NDVI.tif")
    ndbi_path = os.path.join(folder, f"{date}_NDBI.tif")
    ui_path   = os.path.join(folder, f"{date}_UI_final.tif")

    # Aseguramos que exista la carpeta de salida
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{date}_stack3.tif")

    # Copiamos el perfil (CRS, resolución, extent) de NDVI
    with rasterio.open(ndvi_path) as src0:
        meta = src0.meta.copy()
    meta.update(count=3, dtype='float32')

    # Escribimos el stack de 3 bandas
    with rasterio.open(out_path, 'w', **meta) as dst:
        for idx, path in enumerate([ndvi_path, ndbi_path, ui_path], start=1):
            with rasterio.open(path) as src:
                band = src.read(1).astype('float32')
                dst.write(band, idx)
                # Opcional: añadir descripción de banda
                dst.set_band_description(idx, ["NDVI", "NDBI", "UI"][idx-1])

    print(f"Stack 3 bandas creado: {out_path}")


if __name__ == "__main__":
   
    base_dir = "./carpeta_combinado"   # Carpeta que contiene subcarpetas YYYY-MM-DD
    out_dir  = "./carpeta_stacks"      # Carpeta donde se guardarán los stacks

    date = "2019-01-04" # Se corre el código a una sola fecha
    make_index_stack(date, base_dir, out_dir)