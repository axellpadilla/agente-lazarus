"""
Script simple para convertir faq_grupo_lazarus.xlsx a formato CSV sin procesamiento
Para fines de simulacion - guarda los datos tal como estan
"""

import pandas as pd
import os


def main():
    # Definir rutas de entrada y salida
    input_path = 'data/faq_grupo_lazarus.xlsx'
    output_dir = 'packages/lazarus-kb/data'
    output_path = os.path.join(output_dir, 'faq_limpio.csv')

    # Crear directorio de salida si no existe aun
    os.makedirs(output_dir, exist_ok=True)

    # Leer el archivo Excel
    df = pd.read_excel(input_path)

    # Normalizar nombres de columnas a snake_case y remover acentos
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df.columns = df.columns.str.normalize('NFKD').str.encode(
        'ascii', errors='ignore').str.decode('utf-8')

    # Guardar a CSV sin procesamiento adicional
    df.to_csv(output_path, index=False)
    print(f"Conversion completada. CSV guardado en {output_path}")
    print(f"Total de registros: {len(df)}")


if __name__ == "__main__":
    main()
