import sqlite3


def conectar ():
  miConexion=sqlite3.connect("CrudDB")
  cursor=miConexion.cursor()
  try:
    table= """
      CREATE TABLE IF NOT EXISTS personas (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       dni TEXT NOT NULL UNIQUE,
       edad INTEGER NOT NULL,
       nombre VARCHAR(60) NOT NULL,
       apellido VARCHAR(60) NOT NULL,
       direccion TEXT NULL,
       correo TEXT NOT NULL UNIQUE
      
      )
    """
    cursor.execute(table)
    return miConexion
  except Exception as ex:
    print(f'Error de conexion:{ex}')
  finally:
    cursor.close()

