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

from agent.AgenteDeBaseDeDatos.ToolsAgenteDeBaseDeDatos import *

## #######################################################################################################
## @section Clase
## #######################################################################################################

#Definimos una clase
class AgenteDeBaseDeDatos:

  #Definimos el constructor
  def __init__(
      self,
      llm = None,
      dialectoDeBaseDeDatos = None,
      rutaDeBaseDeDatos = None,
      connect_args = None
  ):
    #Obtenemos los tools
    self.toolsAgenteDeBaseDeDatos = ToolsAgenteDeBaseDeDatos(
      llm = llm,
      dialectoDeBaseDeDatos = dialectoDeBaseDeDatos,
      rutaDeBaseDeDatos = rutaDeBaseDeDatos,
      connect_args = connect_args
    ).obtenerTools()

    #Creamos el agente
    self.agente = crearAgente(
      llm = llm,
      tools = self.toolsAgenteDeBaseDeDatos
    )

  #Ejecutar el agente
  def ejecutar(self, prompt):
    respuesta = None

    #Ejecutamos el agente con el prompt
    respuesta = enviarMensajeAlAgente(
        agente = self.agente,
        mensaje = prompt
    )

    #Devolvemos la respuesta
    return respuesta