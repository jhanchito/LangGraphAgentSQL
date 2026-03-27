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

#Utilitarios para manipular la base de datos
from agent.AgenteDeBaseDeDatos.UtilesBaseDeDatosSQLite import *
from agent.AgenteDeBaseDeDatos.UtilesBaseDeDatosTeradata import *
from agent.AgenteDeBaseDeDatos.UtilesAgenteDeBaseDeDatos import *

## #######################################################################################################
## @section Clase
## #######################################################################################################

#Definimos una clase
class FuncionesAgenteDeBaseDeDatos:

  #Definimos el constructor
  def __init__(
      self,
      llm = None,
      dialectoDeBaseDeDatos = None,
      rutaDeBaseDeDatos = None,
      connect_args = None
  ):
    #Objetos básicos
    self.llm = llm,
    self.dialectoDeBaseDeDatos = dialectoDeBaseDeDatos
    self.rutaDeBaseDeDatos = rutaDeBaseDeDatos
    self.connect_args = connect_args

    #Utilitarios para manipular la base de datos SQLite
    self.utilesBaseDeDatos = utilesBaseDeDatosSQLite = UtilesBaseDeDatosSQLite(
      rutaDeBaseDeDatos = rutaDeBaseDeDatos
    )

    #Utilitarios para manipular la base de datos Teradata
    # self.utilesBaseDeDatos = utilesBaseDeDatosTeradata = UtilesBaseDeDatosTeradata(
    #   host = connect_args["host"],
    #   user = connect_args["user"],
    #   password = connect_args["password"],
    #   port = connect_args["port"],
    #   database = connect_args["database"],
    #   prefixTabla = connect_args["prefixTabla"]
    # )

    #Utilitarios del agente
    self.utilesAgenteDeBaseDeDatos = UtilesAgenteDeBaseDeDatos(
      llm = llm,
      dialectoDeBaseDeDatos = dialectoDeBaseDeDatos,
      esquema = self.utilesBaseDeDatos.obtenerEsquemaDeMetadatos()
    )

  #Ejecuta una consulta en lenguaje natural en la base de datos
  def procesarConsultaDeBaseDeDatos(
    self,
    prompt : str
  ) -> dict:
    respuesta = None

    #Generamos el código SQL
    sql = self.utilesAgenteDeBaseDeDatos.generaCodigoSQLDesdeNLP(
        pregunta = prompt
    )
    print("💻💻💻💻💻💻💻SQL: " + sql + "\n💻💻💻💻💻💻💻")
    #Ejecutamos la consulta SQL
    resultados = self.utilesBaseDeDatos.ejecutarConsulta(
        sql = sql
    )
    print("💻💻💻💻💻💻💻Resultados: " + str(resultados) + "\n💻💻💻💻💻💻💻")

    #Analizamos los resultados
    analisis = self.utilesAgenteDeBaseDeDatos.analizarDatos(
        datos = resultados,
        sql = sql,
        prompt = prompt
    )
    print("💻💻💻💻💻💻💻Analisis: " + str(analisis) + "\n💻💻💻💻💻💻💻")
    #Construimos la respuesta
    respuesta = {
        "sql": sql,
        "resultados": resultados,
        "analisis": analisis
    }

    return respuesta