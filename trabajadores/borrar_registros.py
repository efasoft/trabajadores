# borrar_registros.py
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

try:
    # Conexión a la base de datos
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Paso 1: Obtener los IDs de los últimos 100 registros
    cur.execute(f"SELECT {id_column} FROM {table_name} ORDER BY {id_column} DESC LIMIT 5000;")
    rows = cur.fetchall()

    if not rows:
        print("⚠️ No se encontraron registros en la tabla.")
    else:
        # Extraer los IDs en una lista
        ids_to_delete = [row[0] for row in rows]
        num_records = len(ids_to_delete)

        # Confirmar intención (opcional, pero seguro)
        print(f"Se eliminarán los últimos {num_records} registros con los siguientes IDs: {ids_to_delete[:5]}... (total: {num_records})")
        confirm = input("¿Estás seguro? (sí/no): ").strip().lower()
        if confirm not in ['si', 'sí', 's', 'yes', 'y']:
            print("❌ Eliminación cancelada por el usuario.")
        else:
            # Paso 2: Eliminar los registros
            placeholders = ','.join(['%s'] * len(ids_to_delete))
            delete_query = f"DELETE FROM {table_name} WHERE {id_column} IN ({placeholders})"
            cur.execute(delete_query, ids_to_delete)

            # Confirmar cambios
            conn.commit()
            print(f"✅ Se eliminaron exitosamente {cur.rowcount} registros.")

except psycopg2.Error as e:
    # Revertir si hay error
    conn.rollback()
    print(f"❌ Error al eliminar registros: {e}")

except Exception as e:
    conn.rollback()
    print(f"❌ Error inesperado: {str(e)}")

finally:
    # Cerrar conexión
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()