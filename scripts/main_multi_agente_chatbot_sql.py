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
  baseDeConocimientoDeUsuario = None ,# "jts",
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
  """,
  connect_args = {
             "host": "[IP_ADDRESS]",
             "user": "[user]",
             "password": "[password]",
             "port": 1025,
             "database": "[database]",
             "prefixTabla": "T_IAGEN_"
         }
)


#Ejecutamos la función utilitaria para chatear
respuesta = multiAgenteChatbot.ejecutar(
    prompt = """
        Mi Nombre es Jhampier Tapia mi cargo es arquitecto de datos y 
        mi departamento es Arquitectura de datos; 
        Agrupa a los clientes por la edad y muestra por cada grupo:

          - La cantidad de clientes en el grupo
          - La cantidad de transacciones que han realizado
          - El monto total de sus transacciones
          - El monto promedio de sus transacciones
    """
)
#        quiero saber cuantos equipos vendido por modelo y por mes

#Vemos la respuesta
print("Respuesta:")
print(respuesta)



        # Mi Nombre es Jhampier Tapia mi cargo es arquitecto de datos y 
        # mi departamento es Arquitectura de datos; 
        # Agrupa a los clientes por la edad y muestra por cada grupo:

        #   - La cantidad de clientes en el grupo
        #   - La cantidad de transacciones que han realizado
        #   - El monto total de sus transacciones
        #   - El monto promedio de sus transacciones