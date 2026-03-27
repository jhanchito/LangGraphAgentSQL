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

from agent.AgenteDeBaseDeDatos.FuncionesAgenteDeBaseDeDatos import *

## #######################################################################################################
## @section Clase
## #######################################################################################################

#Definimos una clase
class ToolsAgenteDeBaseDeDatos:

  #Definimos el constructor
  def __init__(
      self,
      llm = None,
      dialectoDeBaseDeDatos = None,
      rutaDeBaseDeDatos = None,
      connect_args = None
  ):
    self.funcionesAgenteDeBaseDeDatos = FuncionesAgenteDeBaseDeDatos(
      llm = llm,
      dialectoDeBaseDeDatos = dialectoDeBaseDeDatos,
      rutaDeBaseDeDatos = rutaDeBaseDeDatos,
      connect_args = connect_args
    )

  #Devuelve todas las herramientas
  def obtenerTools(self):
    return [
      self.tool_procesarConsultaDeBaseDeDatos()
    ]

  def tool_procesarConsultaDeBaseDeDatos(self):
    @tool
    def tool_procesarConsultaDeBaseDeDatos(input: str) -> float:
      """
        DESCRIPCIÓN:

        Vas a ejecutar una consulta hecha en lenguaje natural en una base de datos

        INPUT

        prompt: Consulta en lenguaje natural que el usuario ha hecho
      """

      #RESPUESTA
      respuesta = None
      print("💻💻💻Input: " + input + "\n💻💻💻")
      #ACCIONES
      resultado = self.funcionesAgenteDeBaseDeDatos.procesarConsultaDeBaseDeDatos(
        prompt = input
      )

      #Lo colocamos en una respuesta
      respuesta = f"""
        CONSULTA SQL GENERADA:

        {resultado["sql"]}

        ANÁLISIS:

        {resultado["analisis"]}

        DATOS DE LA CONSULTA:

        {resultado["resultados"]}
      """
      print("💻💻💻Respuesta: " + respuesta + "\n💻💻💻")
      #Devolvemos la respuesta
      return respuesta

    return tool_procesarConsultaDeBaseDeDatos