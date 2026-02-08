from GUI.Datos.conexion import Conexion
from GUI.Dominio.persona import Persona
import pyodbc as bd


class PersonaDAO:
    # -------------------------------------------------------------------------
    # CONSULTAS SQL (Ajustadas a los campos de la imagen: Ruta, Costo, Tipo)
    # -------------------------------------------------------------------------
    # IMPORTANTE: Asegúrate de que tu tabla en SQL tenga estas columnas.

    _INSERT = ("INSERT INTO Servicios (cedula, nombre, apellido, ruta, costo, tipo_servicio) "
               "VALUES (?, ?, ?, ?, ?, ?)")

    _SELECT = ("SELECT cedula, nombre, apellido, ruta, costo, tipo_servicio "
               "FROM Servicios WHERE cedula = ?")

    _UPDATE = ("UPDATE Servicios SET nombre=?, apellido=?, ruta=?, costo=?, tipo_servicio=? "
               "WHERE cedula=?")

    _DELETE = ("DELETE FROM Servicios WHERE cedula=?")

    # -------------------------------------------------------------------------
    # MÉTODOS CRUD
    # -------------------------------------------------------------------------

    @classmethod
    def insertar_persona(cls, persona):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            # Orden de datos según los ? del _INSERT
            datos = (persona.cedula, persona.nombre, persona.apellido,
                     persona.ruta, persona.costo, persona.tipo_servicio)

            cursor.execute(cls._INSERT, datos)
            cursor.commit()  # ¡IMPORTANTE! Confirmar cambios en SQL Server

            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Servicio guardado con éxito.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se pudo guardar el registro.'}

        except bd.IntegrityError as e_bb:
            # Manejo de errores específicos de SQL Server (Claves duplicadas)
            error_str = str(e_bb)
            if 'PRIMARY KEY' in error_str or 'duplicate key' in error_str:
                return {'ejecuto': False, 'mensaje': 'La cédula ya existe en la base de datos.'}
            else:
                return {'ejecuto': False, 'mensaje': f'Error de integridad: {error_str}'}
        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al guardar: {e}'}

    @classmethod
    def seleccionar_persona(cls, cedula):
        obj_servicio = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(cls._SELECT, (cedula,))
            registro = cursor.fetchone()

            if registro:
                # Mapeamos los resultados de la BD al objeto Persona
                # El orden depende del SELECT: 0:cedula, 1:nombre, 2:apellido, etc.
                obj_servicio = Persona(
                    cedula=registro[0],
                    nombre=registro[1],
                    apellido=registro[2],
                    ruta=registro[3],
                    costo=registro[4],
                    tipo_servicio=registro[5]
                )
            return obj_servicio

        except Exception as e:
            print(f'Error al buscar: {e}')
            return None

    @classmethod
    def actualizar_persona(cls, persona):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            # Orden según _UPDATE: nombre, apellido, ruta, costo, tipo, WHERE cedula
            datos = (persona.nombre, persona.apellido, persona.ruta,
                     persona.costo, persona.tipo_servicio, persona.cedula)

            cursor.execute(cls._UPDATE, datos)
            cursor.commit()

            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Datos actualizados correctamente.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se encontró el registro para actualizar.'}

        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al actualizar: {e}'}

    @classmethod
    def eliminar_persona(cls, cedula):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(cls._DELETE, (cedula,))
            cursor.commit()

            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Registro eliminado correctamente.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se encontró el registro con esa cédula.'}

        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al eliminar: {e}'}


if __name__ == "__main__":
    # Bloque de prueba
    # Asegúrate de que la clase Persona en 'persona.py' tenga los atributos correctos
    p_prueba = Persona(cedula="1122334455", nombre="Test", apellido="User",
                       ruta="Norte-Sur", costo="2.50", tipo_servicio="Express")

    # Prueba Insertar
    print(PersonaDAO.insertar_persona(p_prueba))