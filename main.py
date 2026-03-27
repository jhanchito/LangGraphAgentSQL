## #######################################################################################################
##
## @copyright Integratel [integratel.com]
## @developer Jhampier Tapia [jhampiertapia@gmail.com]
##
## #######################################################################################################

## #######################################################################################################
## @section Librerías
## #######################################################################################################

#Librería para implementar funciones en GCP
import functions_framework

#Importamos el Multi-Agente
from multiagent.MultiAgenteChatbot.MultiAgenteChatbot import *

## #######################################################################################################
## @section OBJETOS
## #######################################################################################################

# Cache global (se mantiene “warm” entre requests)
_multiAgenteChatbot = None

def get_multi_agente():
    global _multiAgenteChatbot

    if _multiAgenteChatbot is None:
        llm = obtenerModelo()

        _multiAgenteChatbot = MultiAgenteChatbot(
            llm=llm,
            baseDeConocimientoDeUsuario="armg",
            personalidad="""
              Eres un asistente llamado "BigDatin" que atenderá consultas de alumnos en una academia llamada "Big Data Academy",
              de formación de cursos de Big Data, Cloud Computing e Inteligencia Artificial. Al contestar debes seguir las siguientes reglas:

              1. Debes contestar en un lenguaje formal pero amigable
              2. Debes de usar emojis al responder
            """,
            condicionesDeContexto="""
              Como mínimo debe cumplirse todas estas condiciones a la vez:

              - Es un mensaje relacionado a lo que se esperaría en una conversación
              - Es un mensaje que no contiene palabras groseras o que se consideren faltas de respeto
              - Es un mensaje con un tema que una academia que dicta cursos esperaría recibir
            """,
            reglasDeMemoriaDeLargoPlazo="""
              - El nombre del usuario
              - La edad del usuario
              - El sexo del usuario
            """
        )
    
    return _multiAgenteChatbot

## #######################################################################################################
## @section Función
## #######################################################################################################

#En Python los comandos que comienzan con "@" son conocidos como "decorators"
#Los "decorators" activan funcionalidades especiales
#El decorator "functions_framework.http" publica una función para ser accedida desde la web
@functions_framework.http
def procesar(request):
  #Respuesta que devuelve la función
  respuesta = ""

  #Existen 2 maneras de enviar parámetros a una función: POST Y GET
  #Si los parámetros fueron enviados con POST, se extraen de la siguiente manera
  parametros = request.get_json(silent = True)

  #Verificamos que la variable exista
  #Si no existe significa que los parámetros fueron enviados con GET
  if(parametros == None):
    parametros = request.args

  #Verificamos si la función recibió todos los
  #parámetros que necesita para funcionar
  if(
    ("prompt" in parametros)
  ):
    #Extraemos cada parámetro indicando el tipo de dato
    prompt = parametros["prompt"]

    #Obtenemos el multi agente
    multiAgenteChatbot = get_multi_agente()

    #Ejecutamos la función utilitaria para chatear
    respuesta = multiAgenteChatbot.ejecutar(
        prompt = prompt
    )
  else:
    #Indicamos en la respuesta que hay un error
    respuesta = "Debe agregar todos los parametros (prompt)"

  #Retornamos la respuesta
  return respuesta