import psycopg2

# Datos de conexión a la base de datos
db_params = {
    'host': '127.0.0.1',
    'database': 'db_trabajadores_521',
    'user': 'postgres',
    'password': 'Espana21',
    'port': '5432'    
}

# Nombre de la tabla y nombre de la columna del ID
table_name = 'trabajadores_trabajador'
id_column = 'id'

try:
    # Conexión a la base de datos
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Paso 1: Obtener el último registro
    # Obtener el registro y el orden de las columnas de la tabla
    cur.execute(f"SELECT * FROM {table_name} ORDER BY {id_column} DESC LIMIT 1;")
    last_record = cur.fetchone()
    
    if last_record:
        # Obtener los nombres de todas las columnas y su índice
        column_names = [desc[0] for desc in cur.description]
        
        # Encontrar el índice de la columna ID
        id_index = column_names.index(id_column)
        
        # Paso 2: Preparar la inserción sin el ID
        # Excluir la columna ID de la lista de columnas para el INSERT
        columns_to_insert = [col for col in column_names if col != id_column]
        
        # Crear la instrucción SQL de inserción
        placeholders = ', '.join(['%s'] * len(columns_to_insert))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_to_insert)}) VALUES ({placeholders})"
        
        # Paso 3: Repetir la inserción 100 veces
        for _ in range(1000):
            # Crear una lista de valores para la inserción, excluyendo el ID
            # Copiar la lista last_record y eliminar el valor en el índice del ID
            values = list(last_record)
            values.pop(id_index)
            
            cur.execute(insert_query, values)

        # Confirmar los cambios
        conn.commit()
        print("Registros duplicados insertados con éxito.")

    else:
        print("No se encontraron registros en la tabla.")

except psycopg2.Error as e:
    print(f"Error al conectar o ejecutar la consulta: {e}")

finally:
    # Cerrar la conexión
    if 'conn' in locals() and conn:
        cur.close()
        conn.close()