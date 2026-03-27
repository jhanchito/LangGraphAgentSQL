## #######################################################################################################
##
## @copyright Integratel [integratel.com]
## @developer Jhampier Tapia [jhampiertapia@gmail.com]
##
## #######################################################################################################

## #######################################################################################################
## @section Librerías
## #######################################################################################################

#Importamos el Multi-Agente
from multiagent.MultiAgenteChatbot.MultiAgenteChatbot import *
#from MultiAgenteChatbot import *

## #######################################################################################################
## @section Ejecución
## #######################################################################################################

#Obtenemos el modelo
llm = obtenerModelo()

#Construimos el flujo multi-agente
multiAgenteChatbot = MultiAgenteChatbot(
  llm = llm,
  baseDeConocimientoDeUsuario = "jts",
  personalidad = """
    Eres un asistente llamado "Integratin" que atenderá consultas de trabajadores internos  de la empresa llamada "Integratel Perú", de
      servicios de telecomunicaciones para Red Movil y Red Fija. Al contestar debes
      seguir las siguientes reglas:

      1. Debes contestar en un lenguaje formal pero amigable
      2. Debes de usar emojis al responder
  """,
  condicionesDeContexto = """
    Como mínimo debe cumplirse todas estas condiciones a la vez:

      - Es un mensaje relacionado a lo que se esperaría en una conversación
      - Es un mensaje que no contiene palabras groseras o que se consideren faltas de respeto
      - Es un mensaje con un tema que una empresa que dicta servicios de telecomunicaciones esperaría recibir
  """,
  reglasDeMemoriaDeLargoPlazo = """
    - El nombre del usuario
    - El cargo del usuario
    - El departamento del usuario
  """
)

#Ejecutamos la función utilitaria para chatear
respuesta = multiAgenteChatbot.ejecutar(
    prompt = """
        Mi Nombre es Jhampier Tapia y tengo 37 años y soy ingeniero de sistemas
    """
)

#Vemos la respuesta
print("Respuesta:")
print(respuesta)