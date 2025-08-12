import psycopg2

# Datos de conexión a la base de datos
db_params = {
    'host': '127.0.0.1',
    'database': 'db_trabajadores_521',
    'user': 'postgres',
    'password': 'Espana21'
}

def grabar_ultimo_registro(db_params, num_repeticiones=1000):
    """
    Graba el último registro de la tabla especificada un número determinado de veces.

    Args:
        db_params (dict): Diccionario con los parámetros de conexión a la base de datos.
        num_repeticiones (int, optional): Número de veces que se debe repetir la grabación. Defaults to 1000.
    """
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Obtener el último registro insertado (necesitas adaptar la consulta a tu tabla)
        cursor.execute("SELECT * FROM trabajadores_trabajador ORDER BY id DESC LIMIT 1;")  # Ajusta 'id' y 'tu_tabla'
        ultimo_registro = cursor.fetchone()

        if ultimo_registro:
            # Preparar la consulta de inserción
            columnas = [desc[0] for desc in cursor.description]
            valores = tuple(ultimo_registro)
            placeholders = ', '.join(['%s'] * len(columnas))
            consulta_insert = f"INSERT INTO tu_tabla ({', '.join(columnas)}) VALUES ({placeholders}) RETURNING id;" #Ajusta 'tu_tabla' y el nombre de la columna de id

            # Repetir la inserción
            for _ in range(num_repeticiones):
                cursor.execute(consulta_insert, valores)
                #Si necesitas el id del registro insertado, puedes usar:
                id_insertado = cursor.fetchone()[0]
                print(f"Registro insertado con ID: {id_insertado}") #Muestra el id del registro insertado
            conn.commit() #Confirmar los cambios

        else:
            print("No se encontraron registros en la tabla.")


    except psycopg2.Error as e:
        print(f"Error al conectar o insertar datos: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Conexión cerrada.")

# Ejecutar la función
grabar_ultimo_registro(db_params)