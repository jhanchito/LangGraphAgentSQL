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

#Definición de clase
class AgenteGenerativo:

  def __init__(
    self,
    llm = None,
    lenguajeDeProgramacion = None,
    tema = None
  ):
    #Guardamos los atributos
    self.llm = llm

    #Plantilla de prompt
    self.promptTemplate = PromptTemplate.from_template("""
      Eres un experto en el lenguaje de programación:

      {lenguajeDeProgramacion}

      Y también eres un experto en el siguiente tema:

      {tema}

      Vas a generar una función que haga lo siguiente

      {descripcion}

      Sólo genera la función, no agregues nada más que el código de la función
      Listo para ser ejecutado en el lenguaje de programación
    """)

  #Envía un mensaje
  def ejecutar(
      self,
      lenguajeDeProgramacion = None,
      tema = None,
      descripcion = None
  ):
    respuesta = None

    #Creamos el prompt
    promt = self.promptTemplate.format(
      lenguajeDeProgramacion = lenguajeDeProgramacion,
      tema = tema,
      descripcion = descripcion
    )

    #Invocamos el modelo y reemplazamos la marca "html"
    respuesta = self.llm.invoke(promt).content.replace(f"```{lenguajeDeProgramacion}", "").replace("```", "")

    #Devolvemos el contenido de la respuesta
    return respuesta