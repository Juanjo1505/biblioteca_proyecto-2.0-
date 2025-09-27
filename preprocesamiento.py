import pandas as pd
import numpy as np

def cargar_datos(path_libros='data/libros.csv', path_prestamos='data/prestamos.csv'):
    """Carga archivos CSV y devuelve dos DataFrames: libros, prestamos."""
    libros = pd.read_csv(path_libros)
    prestamos = pd.read_csv(path_prestamos)
    return libros, prestamos

def manejar_nulos(df, strategy='fill', fill_value=None, cols=None):
    """Maneja valores nulos:
    - strategy='fill' -> llena nulos con fill_value (o '' para strings, 0 para num)
    - strategy='drop' -> elimina filas con nulos en cols (si provided) o en todo el df
    """
    if cols is None:
        cols = df.columns.tolist()
    if strategy == 'fill':
        if fill_value is not None:
            return df.fillna(fill_value)
        # rellenar por tipo
        for c in cols:
            if df[c].dtype == object:
                df[c] = df[c].fillna('')
            else:
                df[c] = df[c].fillna(0)
        return df
    elif strategy == 'drop':
        return df.dropna(subset=cols)
    else:
        raise ValueError('strategy debe ser "fill" o "drop"')

def estandarizar_texto(df, text_cols):
    """Convierte a minúsculas, quita espacios extra y normaliza acentos simples en columnas de texto."""
    def clean_text(s):
        if pd.isna(s):
            return ''
        s = str(s).strip()
        s = ' '.join(s.split())
        s = s.lower()
        return s
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].apply(clean_text)
    return df

def limpieza_especifica(libros_df):
    """Limpieza específica para libros: quitar símbolo de moneda en 'precio' y convertir a num."""
    df = libros_df.copy()
    if 'precio' in df.columns:
        df['precio'] = df['precio'].astype(str).str.replace(r'[^0-9.,]', '', regex=True)
        df['precio'] = df['precio'].str.replace(',', '').replace('', '0')
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce').fillna(0).astype(int)
    return df

def preparar_datos():
    """Pipeline completa: carga, maneja nulos, estandariza texto y aplica limpieza específica."""
    libros, prestamos = cargar_datos()
    # manejar nulos
    libros = manejar_nulos(libros)
    prestamos = manejar_nulos(prestamos)
    # estandarizar texto en columnas relevantes
    libros = estandarizar_texto(libros, ['titulo','autor','categoria'])
    prestamos = estandarizar_texto(prestamos, ['usuario','estado'])
    # limpieza especifica
    libros = limpieza_especifica(libros)
    # asegurar campos numéricos (esto evita el error del merge)
    if 'id_libro' in libros.columns:
        libros['id_libro'] = pd.to_numeric(libros['id_libro'], errors='coerce').fillna(0).astype(int)
    if 'id_libro' in prestamos.columns:
        prestamos['id_libro'] = pd.to_numeric(prestamos['id_libro'], errors='coerce').fillna(0).astype(int)
    if 'dias_prestamo' in prestamos.columns:
        prestamos['dias_prestamo'] = pd.to_numeric(prestamos['dias_prestamo'], errors='coerce').fillna(0).astype(int)
    return libros, prestamos