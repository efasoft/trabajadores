import psycopg2

# Datos de conexión a la base de datos
db_params = {
    'host': '127.0.0.1',
    'database': 'db_trabajadores_521',
    'user': 'postgres',
    'password': 'Espana21',
    'port': '5432'
}

# Nombre de la tabla y columna ID
table_name = 'trabajadores_trabajador'
id_column = 'id'
email_column = 'email'  # Nombre exacto de la columna en la tabla

try:
    # Conexión a la base de datos
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Paso 1: Obtener el último registro
    cur.execute(f"SELECT * FROM {table_name} ORDER BY {id_column} DESC LIMIT 1;")
    last_record = cur.fetchone()

    if not last_record:
        print("No se encontraron registros en la tabla.")
    else:
        # Obtener nombres de columnas
        column_names = [desc[0] for desc in cur.description]
        id_index = column_names.index(id_column)
        email_index = column_names.index(email_column)

        # Columnas a insertar (sin el ID)
        columns_to_insert = [col for col in column_names if col != id_column]
        placeholders = ', '.join(['%s'] * len(columns_to_insert))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_to_insert)}) VALUES ({placeholders})"

        # Extraer el email base
        original_email = last_record[email_index].strip()
        if '@' not in original_email:
            raise ValueError("El email original no es válido.")

        # Separar nombre y dominio para formato: nombre+num@dominio
        name, domain = original_email.split('@', 1)

        # Paso 2: Insertar 10,000 registros con emails únicos
        for i in range(1, 10001):
            # Crear lista de valores sin el ID
            values = list(last_record)
            values.pop(id_index)  # Remover el ID

            # Modificar el email en la lista de valores
            # Buscar el índice del email en la lista sin ID
            email_idx_in_insert = columns_to_insert.index(email_column)
            new_email = f"{name}+{i:05d}@{domain}"  # Formato: juan+00001@gmail.com
            values[email_idx_in_insert] = new_email

            # Ejecutar inserción
            cur.execute(insert_query, values)

        # Confirmar cambios
        conn.commit()
        print(f"✅ 10,000 registros insertados con emails únicos desde {new_email}.")

except psycopg2.UniqueViolation as e:
    conn.rollback()
    print("❌ Error: Violación de unicidad (posiblemente email duplicado). Detalles:", e)

except psycopg2.IntegrityError as e:
    conn.rollback()
    print("❌ Error de integridad (constraint violation). Detalles:", e)

except Exception as e:
    conn.rollback()
    print("❌ Error inesperado:", str(e))

finally:
    # Cerrar conexión
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()