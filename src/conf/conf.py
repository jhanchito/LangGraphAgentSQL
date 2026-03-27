## #######################################################################################################
## @section Variables del proyecto
## #######################################################################################################

#Nombre del proyecto
CONF_NOMBRE_PROYECTO = "INTEGRATEL AGENTES IA - BI"

## #######################################################################################################
## @section Credenciales de acceso a la cuenta - GCP
## #######################################################################################################

#Identificador del modelo que queremos usar
CONF_MODEL = "gemini-2.5-flash-lite"

#Región a donde nos conectamos
CONF_LOCATION = "global"

#Identificadores de la base de conocimientos
CONF_BASES_DE_CONOCIMIENTO = [
    #"projects/vernal-signal-375402/locations/us-south1/ragCorpora/928324234"
]

#Cantidad de coincidencias máximas en la base de conocimiento
CONF_BASE_DE_CONOCIMIENTO_COINCIDENCIAS_MAXIMAS = 3

#Bucket para la base de conocimiento de usuarios
CONF_BASE_DE_CONOCIMIENTO_USUARIOS = "[GCP_BUCKET_NAME]"



## #######################################################################################################
## @section Credenciales de acceso a la cuenta - AZURE
## #######################################################################################################

#Utilitario para manipular el sistema operativo
import os

#Credenciales AZURE OPENAI FOUNDRY
CONF_AZURE_ENDPOINT = "[URL]"
CONF_OPENAI_API_KEY = "[ENCRYPTION_KEY]"
CONF_API_VERSION = "2025-01-01-preview"
CONF_AZURE_DEPLOYMENT = "gpt-4.1"



#Credenciales AZURE AI SEARCH
CONF_AZURE_SEARCH_SERVICE_NAME = "aisearchinglab"
CONF_AZURE_SEARCH_KEY = "[ENCRYPTION_KEY]"

#Credenciales AZURE DOCUMENT INTELLIGENCE
CONF_AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://endpoint.cognitiveservices.azure.com/"
CONF_AZURE_DOCUMENT_INTELLIGENCE_KEY = "[ENCRYPTION_KEY]"