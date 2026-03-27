## #######################################################################################################
##
## @copyright Integratel [integratel.com]
## @developer Jhampier Tapia [jhampiertapia@gmail.com]
##
## #######################################################################################################

## ################q######################################################################################
## @section Configuración
## #######################################################################################################

#Importamos la configuración
from conf.conf import *

#Importamos los utilitarios
from util.util_ia import *

## ################q######################################################################################
## @section Librerías
## #######################################################################################################

#Utilitario para crear una plantilla de prompt
from langchain_core.prompts import PromptTemplate

#Utilitario para convertir la estructura string a json
import json

#Libreria para conectar a Teradata
import teradatasql

#Utilitario para manejo de sistema y errores
import sys
import logging

## #######################################################################################################
## @section Clase
## #######################################################################################################

#Definimos una clase
class UtilesBaseDeDatosTeradata:

  #Definimos el constructor
  def __init__(
      self,
      host = None,
      user = None,
      password = None,
      port = 1025,
      database = None,
      prefixTabla = None,
      logmech = None
  ):
    self.host = host
    self.user = user
    self.password = password
    self.port = port
    self.database = database
    self.prefixTabla = prefixTabla
    self.logmech = logmech

  #Función para conectar a Teradata
  def ConnectTD(self, phost=None, puser=None, ppwd=None, port=None):
      try:
         logging.info('Conectandose a Terada...')
         
         # Si no se pasan parametros, usar los de la instancia
         if phost is None:
             phost = self.host
         if puser is None:
             puser = self.user
         if ppwd is None:
             ppwd = self.password
         if port is None:
             port = self.port

         connect_args = {
             "host": phost,
             "user": puser,
             "password": ppwd,
             "dbs_port": port
         }
         #print(connect_args)

         connect = teradatasql.connect(None, **connect_args)
         logging.info('Conexion EXITOSA..!.')
         return connect
      except:
         logging.error('No se ha podido realizar la conexion a Teradata.')
         logging.error("%s", sys.exc_info()[0:])
         sys.exit()

  #Función utilitaria para obtener las tablas de una base de datos
  def obtenerTablas(
    self
  ):
    #Creamos la conexion
    conexion = self.ConnectTD()

    #Creamos un cursor
    cursor = conexion.cursor()

    #Lanzamos la consulta a DBC.TablesV
    # Si tenemos una base de datos definida, filtramos por ella.
    # Caseo contrario, traemos todas las tablas no del sistema (heuristica simple)
    query = """
      SELECT
        TableName
      FROM
        DBC.TablesV
      WHERE
        TableKind = 'T'
    """
    if self.database:
        query += f" AND DatabaseName = '{self.database}' AND TableName like '{self.prefixTabla}%'"
    else:
        # Excluir tablas de sistema comunes si no se especifica DB
        query += " AND DatabaseName NOT IN ('DBC', 'SYSADMIN', 'tdwm', 'SystemFe')"

    cursor.execute(query)

    #Obtenemos los nombres de las tablas
    tablas = []

    #Iteramos la consulta
    for fila in cursor.fetchall():
      #print(fila)
      tablas.append(fila[0])

    conexion.close()
    return tablas

  #Función utilitaria para obtener la información de las columnas de una tabla
  def obtenerInformacionDeColumnasDeTabla(
    self,
    tabla = None
  ):
    #Columnas de una tabla
    #Dentro, para cada columna, se indicará en un JSON:
    #
    # - nombreDeColumna: Nombre de la columna
    # - tipoDeDatoDeColumna: Tipo de dato de la columna
    columnasDeTabla = []

    #Creamos la conexion
    conexion = self.ConnectTD()

    #Creamos un cursor
    cursor = conexion.cursor()

    #Obtenemos la información de las columnas de la tabla desde DBC.ColumnsV
    # Asumimos que tabla es solo nombre. Si tiene DatabaseName.TableName, habria que parsear.
    # Por ahora asumimos busqueda simple por TableName.
    
    query = f"""
    SELECT ColumnName, ColumnType, ColumnLength
    FROM DBC.ColumnsV 
    WHERE TableName = '{tabla}'
    """
    
    if self.database:
        query += f" AND DatabaseName = '{self.database}'"

    cursor.execute(query)

    #Obtenemos la información de las columnas de la tabla
    informacionDeColumnas = cursor.fetchall()

    #Iteramos la información de cada columna
    # ColumnType en Teradata es codigo (e.g. 'CV', 'I'). Podriamos mapear a nombres legibles si fuera necesario.
    for informacion in informacionDeColumnas:
      columnasDeTabla.append(
        {
          "nombreDeColumna": informacion[0].strip(),
          "tipoDeDatoDeColumna": informacion[1].strip() # Retornamos el codigo tipo 'I', 'CV', etc.
        }
      )

    conexion.close()
    return columnasDeTabla

  #Función para obtener el esquema de metadatos de la base de datos
  def obtenerEsquemaDeMetadatos(
    self
  ):
    #Nombres de tablas, e información de todos las columnas
    esquema = {}

    #Lo haremos en bucle para todas las tablas
    #Obtenemos las tablas
    tablas = self.obtenerTablas()

    #Iteramos todas las tablas
    for tabla in tablas:
      #Obtenemos la información de los campos
      informacion = self.obtenerInformacionDeColumnasDeTabla(
        tabla = tabla
      )

      #Asignamos el esquema a la tabla
      esquema[self.database + "." + tabla] = informacion

    return esquema

  #Función para ejecutar una consulta en la base de datos
  def ejecutarConsulta(
    self,
    sql = None
  ):
    #Creamos la conexion
    conexion = self.ConnectTD()

    #Creamos un cursor que consulte a la base de datos
    cursor = conexion.cursor()

    #Ejecutamos la consulta
    cursor.execute(sql)

    #Obtenemos los resultados
    resultados = cursor.fetchall()
    
    conexion.close()

    return resultados
