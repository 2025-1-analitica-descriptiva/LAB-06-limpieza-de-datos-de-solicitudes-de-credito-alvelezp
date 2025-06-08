"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
from pathlib import Path
import re

def estandarizar_fecha(fecha_str):
    if pd.isna(fecha_str):
        return pd.NaT

    fecha_str = str(fecha_str).strip()
    
    if re.match(r'^\d{4}[/\-]', fecha_str):
        try:
            return pd.to_datetime(fecha_str, format='%Y/%m/%d', errors='raise')
        except:
            return pd.NaT
    else:
        try:
            return pd.to_datetime(fecha_str, dayfirst=True, errors='raise')
        except:
            return pd.NaT


def estandarizar_monto(valor):
    if pd.isna(valor):
        return pd.NA
    valor = str(valor)
    valor = valor.strip()
    valor = valor.replace('$', '')
    valor = valor.replace(',', '')
    valor = valor.replace(' ', '')
    valor = valor.replace('-', '')
    return int(float(valor))


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    input_path = Path("files/input/solicitudes_de_credito.csv")
    output_path = Path("files/output/solicitudes_de_credito.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Leer el archivo
    df = pd.read_csv(input_path, sep=';', index_col=0)

    for col in df.select_dtypes(include='object').columns:
        df[col] = (
            df[col]
            .str.replace(r'[-_]', '-', regex=True)
            .str.replace(r'\s+', '-', regex=True)
            .str.strip()
            .str.lower()
        )
    
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(estandarizar_fecha)

    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].dt.strftime('%-d/%-m/%Y')

    df['monto_del_credito'] = df['monto_del_credito'].apply(estandarizar_monto)

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Eliminar filas con datos faltantes
    df = df.dropna()

    # Guardar el archivo limpio
    df.to_csv(output_path, index=False, sep=';')
