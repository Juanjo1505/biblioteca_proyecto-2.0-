
from preprocesamiento import preparar_datos
import pandas as pd

def main():
    while True:
        print("\n===== MENÚ BIBLIOTECA =====")
        print("1. Mostrar todos los libros")
        print("2. Mostrar análisis de la biblioteca")
        print("3. Borrar un libro por ID")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            libros, _ = preparar_datos()
            print("\n===== LISTA DE LIBROS =====")
            print(libros[['id_libro','titulo','autor','categoria','precio']].to_string(index=False))

        elif opcion == '2':
            libros, prestamos = preparar_datos()
            df = prestamos.merge(libros, left_on='id_libro', right_on='id_libro', how='left', suffixes=('_prest', '_lib'))
            print('\n===== RESUMEN DE DATOS =====')
            print(f'Número de libros (únicos): {libros["id_libro"].nunique()}')
            print(f'Número total de registros de préstamos: {prestamos.shape[0]}')
            cuenta_libros = df['titulo'].value_counts()
            top = cuenta_libros.head(5)
            print('\n===== LIBROS MÁS PRESTADOS (top 5) =====')
            print(top.to_string())
            avg_dias_por_categoria = df.groupby('categoria')['dias_prestamo'].mean().round(2).sort_values(ascending=False)
            print('\n===== PROMEDIO DE DÍAS DE PRÉSTAMO POR CATEGORÍA =====')
            print(avg_dias_por_categoria.to_string())
            autor = 'gabriel garcía márquez'
            prestados_autor = df[(df['autor'] == autor) & (df['estado'].str.contains('prest'))]
            print(f'\n===== LIBROS DE {autor.title()} ACTUALMENTE PRESTADOS =====')
            if prestados_autor.empty:
                print('No hay préstamos activos para ese autor.')
            else:
                print(prestados_autor[['id_prestamo','titulo','usuario','dias_prestamo','estado']].to_string(index=False))
            conteo_estado = df['estado'].value_counts()
            print('\n===== PRÉSTAMOS POR ESTADO =====')
            print(conteo_estado.to_string())
            problemas = libros[(libros['titulo']=='') | (libros['autor']=='')].copy()
            print('\n===== REGISTROS DE LIBROS CON PROBLEMAS (titulo o autor vacío) =====')
            if problemas.empty:
                print('No se detectaron problemas críticos en los libros.')
            else:
                print(problemas.to_string(index=False))
            resumen_autor = df.groupby('autor').agg(
                prestamos_total = ('id_prestamo','count'),
                precio_promedio = ('precio','mean')
            ).sort_values('prestamos_total', ascending=False).head(10)
            resumen_autor['precio_promedio'] = resumen_autor['precio_promedio'].round(2)
            print('\n===== RESUMEN POR AUTOR (prestamos_total, precio_promedio) TOP 10 =====')
            print(resumen_autor.to_string())

        elif opcion == '3':
            libros, _ = preparar_datos()
            print("\n===== ELIMINAR LIBRO =====")
            print(libros[['id_libro','titulo','autor']].to_string(index=False))
            try:
                id_borrar = int(input("Ingrese el ID del libro a borrar: "))
                if id_borrar in libros['id_libro'].values:
                    libros = libros[libros['id_libro'] != id_borrar]
                    libros.to_csv('data/libros.csv', index=False)
                    print(f"Libro con ID {id_borrar} eliminado correctamente.")
                else:
                    print("ID no encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcion == '4':
            print("Saliendo de la biblioteca. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    main()
