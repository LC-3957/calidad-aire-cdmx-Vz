import os
import pandas as pd
import glob
print("=== EXPLORACION DETALLADA DE LA ESTRUCTURA ===\n")

ruta_base = "AIRE_CDMX_2011_2021/AIRE"

archivos = glob.glob("AIRE_CDMX_2011_2021/AIRE/contaminantes/medias/horarios/medias6h_*.csv")
for archivo in sorted(archivos):
    df = pd.read_csv(archivo)
    año = archivo[-8:-4]
    for param in ['O3', 'NO2', 'PM2.5']:
        sub = df[df['id_parameter'] == param]
        total = len(sub)
        no_nulos = sub['value'].notna().sum()
        pct = round(100 * no_nulos / total, 1) if total > 0 else 0
        print(f"{año} | {param:6} | {no_nulos}/{total} registros válidos ({pct}%)")

print(" Contenido de 'contaminantes/':")
ruta_contaminantes = f"{ruta_base}/contaminantes"
if os.path.exists(ruta_contaminantes):
    archivos = os.listdir(ruta_contaminantes)
    for archivo in archivos[:20]:
        print(f" {archivo}")
        
    if 'contaminantes_2011.csv' in archivos:
        print(f"\n Leyendo las primeras 20 lineas de contaminantes_2011.csv:")
        with open(f"{ruta_contaminantes}/contaminantes_2011.csv", 'r', encoding='latin-1') as f:
            lineas = f.readlines()
            for i, linea in enumerate(lineas[:20]):
                print(f"{i+1}: {linea.rstrip()}")
else:
    print("No existe carpeta contaminantes/")


print(f"\n Contenido de '{ruta_base}':")
if os.path.exists(ruta_base):
    archivos = os.listdir(ruta_base)
    for archivo in archivos:
        ruta_completa = f"{ruta_base}/{archivo}"
        if os.path.isdir(ruta_completa):
            print(f"   {archivo}/")
        else:
            print(f"  {archivo}")


print(f"\n Buscando archivos CSV en toda la estructura:")
csvs = []
for root, dirs, files in os.walk(ruta_base):
    for file in files:
        if file.endswith('.csv'):
            csvs.append(os.path.join(root, file))

for csv_file in csvs[:20]:
    print(f"  {csv_file}")
    
   
    try:
        with open(csv_file, 'r', encoding='latin-1') as f:
            primeras_lineas = f.readlines()[:3]
            print(f"Primeras lineas: {primeras_lineas}")
    except:
        print(f" Error leyendo archivo")