
from preprocesamiento import preparar_datos
import pandas as pd

def main():
    libros, prestamos = preparar_datos()

    # Merge: unir libros con prestamos
    df = prestamos.merge(libros, left_on='id_libro', right_on='id_libro', how='left', suffixes=('_prest', '_lib'))

    print('\n===== RESUMEN DE DATOS =====')
    print(f'Número de libros (únicos): {libros["id_libro"].nunique()}')
    print(f'Número total de registros de préstamos: {prestamos.shape[0]}')

    # 1) Análisis de Frecuencia: libro más prestado
    cuenta_libros = df['titulo'].value_counts()
    top = cuenta_libros.head(5)
    print('\n===== LIBROS MÁS PRESTADOS (top 5) =====')
    print(top.to_string())

    # 2) Análisis de Agregación: promedio de días de préstamo por categoría
    avg_dias_por_categoria = df.groupby('categoria')['dias_prestamo'].mean().round(2).sort_values(ascending=False)
    print('\n===== PROMEDIO DE DÍAS DE PRÉSTAMO POR CATEGORÍA =====')
    print(avg_dias_por_categoria.to_string())

    # 3) Análisis con Filtrado y Conteo:
    autor = 'gabriel garcía márquez'
    prestados_autor = df[(df['autor'] == autor) & (df['estado'].str.contains('prest'))]
    print(f'\n===== LIBROS DE {autor.title()} ACTUALMENTE PRESTADOS =====')
    if prestados_autor.empty:
        print('No hay préstamos activos para ese autor.')
    else:
        print(prestados_autor[['id_prestamo','titulo','usuario','dias_prestamo','estado']].to_string(index=False))

    # 4) Otros ejemplos: cantidad de préstamos por estado
    conteo_estado = df['estado'].value_counts()
    print('\n===== PRÉSTAMOS POR ESTADO =====')
    print(conteo_estado.to_string())

    # 5) Mostrar algunos registros con problemas detectados (e.g., filas con títulos vacíos o sin autor)
    problemas = libros[(libros['titulo']=='') | (libros['autor']=='')].copy()
    print('\n===== REGISTROS DE LIBROS CON PROBLEMAS (titulo o autor vacío) =====')
    if problemas.empty:
        print('No se detectaron problemas críticos en los libros.')
    else:
        print(problemas.to_string(index=False))

    # 6) Agregación adicional: total de préstamos y promedio de precio de libros por autor (top 5 autores con más préstamos)
    resumen_autor = df.groupby('autor').agg(
        prestamos_total = ('id_prestamo','count'),
        precio_promedio = ('precio','mean')
    ).sort_values('prestamos_total', ascending=False).head(10)
    resumen_autor['precio_promedio'] = resumen_autor['precio_promedio'].round(2)
    print('\n===== RESUMEN POR AUTOR (prestamos_total, precio_promedio) TOP 10 =====')
    print(resumen_autor.to_string())

if __name__ == '__main__':
    main()
