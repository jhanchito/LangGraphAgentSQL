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
class AgenteDeMemoriaLargoPlazo:

  #Definimos el constructor
  def __init__(
      self,
      llm = None,
      condiciones = None
  ):
    #Guardamos los atributos
    self.llm = llm
    self.condiciones = condiciones

    #Plantilla de prompt
    self.promptTemplate = PromptTemplate.from_template("""
      Si el mensaje incluye como mínimo 1 de estos puntos:

      {condiciones}

      Para cada información detectada en ese mensaje, devolverás un JSON con estas 2 variables

      - "estado": INFORMACION_POR_RECORDAR
      - "informacion": Un párrafo de texto, en donca cada oración del párrafo diga exactamente lo siguiente "El usuario afirma que INFORMACION_DETECTADA",
      donde "INFORMACION_DETECTADA" es la información que se detectó respecto a alguno de esos puntos. Habrán tantas oraciones en
      el párrafo como informaciones detectadas
      
      Ejemplo:
      {{ 'estado' : 'INFORMACION_POR_RECORDAR'
      , 'informacion': 'El usuario afirma que Jhampier Tapia. El usuario afirma que arquitecto de datos. El usuario afirma que Arquitectura de datos.'
      }}
      Si no detectas nada, devolverás un JSON con 1 variable

      - "estado": 'NO_SE_DETECTO_INFORMACION_POR_RECORDAR'

      Este es el mensaje:

      {mensaje}
    """)

  #Ejecutar el agente
  def ejecutar(self, prompt):
    respuesta = None

    #Creamos la consulta
    consulta = self.promptTemplate.format(
      condiciones = self.condiciones,
      mensaje = prompt
    )
    print("Inicia a3")
    #Invocamos el modelo y reemplazamos la marca "json"
    respuestaDelModelo = self.llm.invoke(consulta).content.replace("```json", "").replace("```", "")
    print("FIN a3")
    #La convertimos a JSON
    try:
        respuesta = json.loads(respuestaDelModelo)
    except Exception as e:
        respuesta = {
            "status": "ERROR",
            "message": f"Ocurrió un error al parsear la respuesta del modelo: {respuestaDelModelo.content}"
        }

    #Devolvemos el contenido de la respuesta
    return respuesta