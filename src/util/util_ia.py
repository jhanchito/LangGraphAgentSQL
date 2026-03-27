## #######################################################################################################
##
## @copyright Integratel 
## @Developer Jhampier Tapia    [jhampiertapia@gmail.com]
##
## #######################################################################################################

## ################q######################################################################################
## @section Configuración
## #######################################################################################################

#Importamos la configuración
from conf.conf import *

## ################q######################################################################################
## @section Librerías
## #######################################################################################################

#Utilitario de conexión a Vertex AI
#Puede tardar hasta 1 MINUTOS en ejecutarse
from langchain_google_vertexai import ChatVertexAI

#Utilitario para crear la memoria a corto plazo del modelo
from langchain_core.chat_history import InMemoryChatMessageHistory

#Utilitario para definir reglas de "personalidad" en el modelo
from langchain_core.messages import SystemMessage

#Utilitario para enviar mensajes más complejos
from langchain_core.messages import HumanMessage

#Utilitarios para interfaces gráficas
import gradio as gr

#Utilitario para conectarnos a bases de conocimiento
from vertexai.preview import rag

#Utilitario para deifinir las tools
from langchain_core.tools import tool

#Utilitario para crear agentes
from langchain.agents import create_agent

#Utilitario para obtener la fecha y hora actual
import datetime

#Utilitario para convertir la estructura string a json
import json

#Utilitario para obtener la fecha y hora
from datetime import datetime

#Librería para enviar consultas web
import requests

#Utilitario para procesar webs
from bs4 import BeautifulSoup

#Librería para SQLite
import sqlite3

#Librería para manipular el sistema operativo
import os

#Utilitario para crear una plantilla de prompt
from langchain_core.prompts import PromptTemplate

#Librería para generar números aleatorios
import random

#Utilitario para calcular tiempos entre fechas
from datetime import timedelta

#Utilitario para usar el servicio de Cloud Storage
from google.cloud import storage

#Utilitario para definir un grafo de LangGraph
from langgraph.graph import StateGraph


#Utilitario de conexión a Azure OpenAI
from langchain_openai import AzureChatOpenAI

## #######################################################################################################
## @section Funciones
## #######################################################################################################

#Obtiene el modelo con el que trabajamos
def obtenerModelo():
  if os.getenv('MODEL_PROVIDER', 'openai') == 'openai':
    llm = AzureChatOpenAI(
        api_version = CONF_API_VERSION,
        azure_endpoint = CONF_AZURE_ENDPOINT,
        openai_api_key = CONF_OPENAI_API_KEY,
        azure_deployment = CONF_AZURE_DEPLOYMENT
    )
  elif os.getenv('MODEL_PROVIDER', 'gemini') == 'gemini':
    #Conexión a un modelo
    llm = ChatVertexAI(
        model = CONF_MODEL,
        location = CONF_LOCATION
    )
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/adminintegratel/Integratel/agentesIA/BDAGCP/credenciales/llm_gcp.json"
  return llm

#Abre la sesión de chat con el modelo
def crearMemoriaCortoPlazo(
    contexto = None
):
  #Definimos el mensaje del sistema
  mensajeDelSistema = SystemMessage(
      content = contexto
  )

  #Creamos la memoria a corto plazo
  memoriaCortoPlazo = InMemoryChatMessageHistory()

  #Agregamos la personalidad en la memoria a corto plazo
  memoriaCortoPlazo.add_message(mensajeDelSistema)

  return memoriaCortoPlazo

#Agrega el contexto al mensaje del usuario, desde una base de conocimiento
def prepararMensaje(
    mensaje = None
):
  mensajePreparado = None

  #Si no tenemos bases de conocimiento
  if (
      (CONF_BASES_DE_CONOCIMIENTO is None) or
      (len(CONF_BASES_DE_CONOCIMIENTO) == 0)
  ):
    mensajePreparado = mensaje
  else:
    #Configuramos que sólo usaremos las 3 primeras coincidencias
    configuracionRag = rag.RagRetrievalConfig(
      top_k = CONF_BASE_DE_CONOCIMIENTO_COINCIDENCIAS_MAXIMAS
    )

    #Bases de conocimiento para RAG
    rag_resources = []

    #Agregamos todas las bases de conocimiento
    for baseDeConocimiento in CONF_BASES_DE_CONOCIMIENTO:
      rag_resources.append(
          rag.RagResource(
              rag_corpus = baseDeConocimiento,
          )
      )

    #Hacemos una búsqueda
    respuestaRag = rag.retrieval_query(
        rag_resources = rag_resources,
        text = mensaje,
        rag_retrieval_config = configuracionRag
    )

    #Variable que acumula todos los chunks de textos
    resultadoDeBusqueda = ""

    #Acumulamos todos los chunks
    for chunk in respuestaRag.contexts.contexts:
      resultadoDeBusqueda = resultadoDeBusqueda + chunk.text + "\n"

    #Definimos el mensaje con contexto
    mensajePreparado = f"""
      Usa los siguientes fragmentos de contexto para responder la pregunta.
      Si no encuentras la respuesta en el contexto, di que no lo sabes.

      Contexto:
      {resultadoDeBusqueda}

      Pregunta:
      {mensaje}
    """

  return mensajePreparado

#Envia un mensaje al modelo
def enviarMensajeAlModelo(
    llm = None,
    memoriaCortoPlazo = None,
    mensaje = None
):
  #Preparamos el mensaje
  mensajePreparado = prepararMensaje(mensaje)
  print("🚀 mensajePreparado: ", mensajePreparado)
  #Construmos el JSON del mensaje
  mensajeHumano = HumanMessage(
    content=[
      {
        "type": "text",
        "text": mensajePreparado
      }
    ]
  )

  #Agregamos el mensaje del ser humano
  memoriaCortoPlazo.add_user_message(mensajeHumano)
  #print("🚀 memoriaCortoPlazo: ", memoriaCortoPlazo.messages)
  #Envíamos el mensaje
  respuesta = llm.invoke(memoriaCortoPlazo.messages)

  #Guardamos en la memoria a corto plazo la respuesta de la IA
  memoriaCortoPlazo.add_ai_message(respuesta)

  return respuesta.content

#Función utilitaria para enviar mensajes a agentes
def enviarMensajeAlAgente(
    agente = None,
    mensaje = None
):
  #Construimos el JSON del mensaje
  mensajeHumano = HumanMessage(
      content=[
        {
          "type": "text",
          "text": mensaje
        }
      ]
    )

  #Ejecutamos el agente
  respuesta = agente.invoke(
      {
          "messages": [
              mensajeHumano
          ]
      }
  )

  #Retornamos la respuesta
  return respuesta["messages"][-1].content

#Obtiene los parámetros del agente
def obtenerParametrosDeAgente(input):
  parametros = None

  #Tratamos de obtener el json de los parámetros
  try:
    parametros = json.loads(input)
  except Exception as e:
    #Si falla, cremos un JSON vacío
    parametros = {}

  return parametros

#Función utilitaria para crear un agente
def crearAgente(
    llm = None,
    tools = None
):
  #Creamos el agente
  agente = create_agent(
    model = llm,
    tools = tools
  )

  #Lo devolvemos
  return agente

#Utilitario para escribir en base de conocimiento de usuario
def actualizarBaseDeConocimientoDeUsuario(
  baseDeConocimientoDeUsuario = None,
  contenido = None
):
  #Nos conectamos al servicio de Cloud Storage
  cliente = storage.Client()

  #Nos conectamos al bucket
  bucket = cliente.bucket(CONF_BASE_DE_CONOCIMIENTO_USUARIOS)

  #Archivo en donde se escribirá
  archivo = bucket.blob(baseDeConocimientoDeUsuario)

  #Escribimos en el archivo
  archivo.upload_from_string(
    contenido.encode("utf-8"),
    content_type="text/plain; charset=utf-8"
  )

#Utilitario para leer desde base de conocimiento de usuario
def leerBaseDeConocimientoDeUsuario(
  baseDeConocimientoDeUsuario = None
):
  #Nos conectamos al servicio de Cloud Storage
  cliente = storage.Client()

  #Nos conectamos al bucket
  bucket = cliente.bucket(CONF_BASE_DE_CONOCIMIENTO_USUARIOS)

  #Archivo en donde se escribirá
  archivo = bucket.blob(baseDeConocimientoDeUsuario)

  #Leemos el archivo
  contenido = archivo.download_as_text(encoding="utf-8")

  return contenido