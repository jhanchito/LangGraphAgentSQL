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

## #######################################################################################################
## @section Clase
## #######################################################################################################

#Definimos una clase
class AgenteDeChatbot:

  #Definimos el constructor
  def __init__(
      self,
      llm = None,
      contexto = None
  ):
    #Creamos el agente
    self.llm = llm

    #Creamos la memoria a corto plazo
    self.memoriaCortoPlazo = crearMemoriaCortoPlazo(
        contexto = contexto
        # """
        #   Eres un asistente llamado "Integratin" que atenderá consultas de Trabajadores de la empresa "Integratel" , la cual es una empresa de telecomunicaiones
        #   tanto de red movil como de fibra optica. Al contestar debes
        #   seguir las siguientes reglas:

        #   1. Debes contestar en un lenguaje formal pero amigable
        #   2. Debes de usar emojis al responder
        # """
    )

  #Ejecutar el agente
  def ejecutar(self, prompt):
    #Ejecutamos el agente con el prompt
    respuesta = enviarMensajeAlModelo(
      llm = self.llm,
      memoriaCortoPlazo = self.memoriaCortoPlazo,
      mensaje = prompt
    )

    #Devolvemos la respuesta
    return respuesta