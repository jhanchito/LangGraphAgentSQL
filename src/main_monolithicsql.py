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
import streamlit as st
import sys
import os

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
    Eres un asistente llamado "SQL Lin" que atenderá consultas de trabajadores internos  
      de la empresa llamada "Integratel Perú", de servicios de telecomunicaciones para Red Movil 
      y Red Fija. Al contestar debes seguir las siguientes reglas:

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
             "host": "[IP_ADDRESS]", #"localhost", # 172.29.165.17
             "user": "[user]",
             "password": "[password]",
             "port": 1025,
             "database": "[database]",
             "prefixTabla": "T_IAGEN_"
         }
)

# Cargar variables de entorno desde .env (en la misma carpeta)
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    # dotenv no está instalado, continuar sin él
    pass

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(
    page_title="Agente SQL de Teradata",
    page_icon="🧠",
    layout="wide"
)

# --- BARRA LATERAL FIJA ---
try:
    st.sidebar.image("src/images/AgenteSQL.png", use_container_width=True)
except:
    st.sidebar.markdown("### 🏢 AGENTE SQL")

st.sidebar.markdown("## Sistema de Consulta a una base de datos - Dev: Jhampier Tapia")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 MULTIAGENTE")
st.sidebar.markdown("Usando LangGraph y SQL LITE")

st.title("🤖 Agente Analista de Datos de SQL LITE - Ventas Moviles")
st.caption("Hecho con LangGraph + Streamlit")

# --- GESTIÓN DEL HISTORIAL DE LA CONVERSACIÓN ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNCIÓN PARA EJECUTAR EL AGENTE ---
def run_agent_query(user_message: str) -> str:
    """
    Ejecuta el agente LangGraph usando el wrapper o método directo
    """
    try:
        # Si tenemos el wrapper, usarlo
        
        #Ejecutamos la función utilitaria para chatear
        respuesta = multiAgenteChatbot.ejecutar(
            prompt = user_message #"""
            #     Mi Nombre es Jhampier Tapia mi cargo es arquitecto de datos y 
            #     mi departamento es Arquitectura de datos; 
            #     Agrupa a los clientes por la edad y muestra por cada grupo:

            #     - La cantidad de clientes en el grupo
            #     - La cantidad de transacciones que han realizado
            #     - El monto total de sus transacciones
            #     - El monto promedio de sus transacciones
            # """
        )
        #        quiero saber cuantos equipos vendido por modelo y por mes

        #Vemos la respuesta
        print("Respuesta:")
        print(respuesta)

        # Si no, intentar con run_live
        response = respuesta #root_agent.run_live(user_message)
        
        # Procesar diferentes tipos de respuesta
        if response is None:
            return "El agente no generó una respuesta."
        
        # Si la respuesta es un string directo
        if isinstance(response, str):
            return response
        
        # Si la respuesta es un objeto con atributo 'content'
        if hasattr(response, 'content'):
            return str(response.content)
        
        # Si la respuesta es un objeto con atributo 'text'
        if hasattr(response, 'text'):
            return str(response.text)
        
        # Si la respuesta es un objeto con atributo 'message'
        if hasattr(response, 'message'):
            return str(response.message)
        
        # Si la respuesta es un objeto con atributo 'output'
        if hasattr(response, 'output'):
            return str(response.output)
        
        # Si la respuesta es un objeto con atributo 'result'
        if hasattr(response, 'result'):
            return str(response.result)
        
        # Si la respuesta es un objeto con atributo 'response'
        if hasattr(response, 'response'):
            return str(response.response)
        
        # Si la respuesta es un objeto con método __str__
        return str(response)
        
    except AttributeError as ae:
        # Si run_live no existe o falla, intentar con run_async
        error_msg = str(ae)
        
        try:
            # Intentar con run_async - este método existe según la lista
            import asyncio
            
            async def run_agent_async():
                return await root_agent.run_async(user_message)
            
            # Ejecutar de forma síncrona
            response = asyncio.run(run_agent_async())
            if isinstance(response, str):
                return response
            return str(response)
        except Exception as async_error:
            # Si run_async no funciona, intentar acceder directamente al modelo
            try:
                # El agente ADK tiene un atributo 'model' que podemos usar
                if hasattr(root_agent, 'model'):
                    # Construir un prompt con las instrucciones y la pregunta
                    full_prompt = f"{root_agent.instruction}\n\nUsuario: {user_message}\n\nRespuesta:"
                    
                    # Intentar generar contenido directamente con el modelo
                    if hasattr(root_agent.model, 'generate_content'):
                        response = root_agent.model.generate_content(full_prompt)
                        if hasattr(response, 'text'):
                            return response.text
                        return str(response)
                    
                    # Si el modelo es un string, intentar crear un modelo Gemini
                    elif isinstance(root_agent.model, str):
                        import google.generativeai as genai
                        import os
                        
                        # Configurar API key si existe
                        api_key = os.getenv('GOOGLE_API_KEY')
                        if api_key:
                            genai.configure(api_key=api_key)
                        
                        # Crear el modelo y generar respuesta
                        model = genai.GenerativeModel(root_agent.model)
                        response = model.generate_content(full_prompt)
                        
                        # Si hay herramientas, ejecutarlas manualmente
                        if hasattr(root_agent, 'tools') and root_agent.tools:
                            # Por ahora, solo informar que hay herramientas disponibles
                            tools_info = f"\n\nHerramientas disponibles: {[tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in root_agent.tools]}"
                            return response.text + tools_info
                        
                        return response.text
            except Exception as model_error:
                pass
        
        # Si ningún método funcionó, mostrar los métodos disponibles
        available_methods = [method for method in dir(root_agent) if not method.startswith('_') and callable(getattr(root_agent, method))]
        return f"Error: No se pudo ejecutar el agente.\nMétodos disponibles: {', '.join(available_methods[:20])}\nError original: {error_msg}"
        
    except TypeError as te:
        # El agente puede necesitar parámetros adicionales
        try:
            # Intentar con un contexto vacío
            response = root_agent.say(user_message, context={})
            if isinstance(response, str):
                return response
            return str(response)
        except:
            pass
        
        # Intentar con session_id
        try:
            response = root_agent.say(user_message, session_id="streamlit_session")
            if isinstance(response, str):
                return response
            return str(response)
        except:
            pass
        
        return f"Error de tipo: {str(te)}"
        
    except Exception as e:
        # Log del tipo de error para debugging
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Intentar obtener más información sobre el error
        import traceback
        traceback_str = traceback.format_exc()
        
        # Si el error menciona 'Message' o 'MessagePart', es un problema de formato
        if 'Message' in error_msg or 'MessagePart' in error_msg:
            return f"Error de formato de mensaje ADK. El agente puede requerir una actualización del SDK o una configuración diferente.\n\nError: {error_msg}"
        
        return f"Error {error_type}: {error_msg}\n\nDetalles: {traceback_str[:500]}"

# Mostramos el historial (chat mostrado en body)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ENTRADA Y COMUNICACIÓN CON EL AGENTE ---
if prompt := st.chat_input("¿En qué te puedo ayudar?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # Procesar y mostrar respuesta del agente
    with st.chat_message("assistant"):
        with st.spinner("Consultando Multiagente LangGraph..."):
            try:
                # Ejecutar el agente ADK
                response = run_agent_query(prompt)
                
                # Mostrar la respuesta
                st.markdown(response)
                
                # Agregar respuesta al historial
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_message = f"Error al procesar la consulta: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- INFORMACIÓN ADICIONAL EN LA BARRA LATERAL ---
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Información del Dataset")
    st.markdown("""**Dataset**: SQL LITE VENTAS MOVILES""")
    
    st.markdown("### 💡 Ejemplos de consultas")
    ejemplos = [
      "Dame en una tabla el total de transacciones agrupado por cliente y por equipo celular",
      "Agrupa por departamento ydame La cantidad de transacciones y el monto total  que han realizado",
      "Agrupa por equipos celulares y dame El monto total de sus transacciones",
      "Agrupa a los clientes por la edad y muestra El monto promedio de sus transacciones",
      """Mi Nombre es Jhampier Tapia mi cargo es arquitecto de datos y 
        mi departamento es Arquitectura de datos; 
        Agrupa a los clientes por la edad y muestra por cada grupo:
          - La cantidad de clientes en el grupo
          - La cantidad de transacciones que han realizado
          - El monto total de sus transacciones
          - El monto promedio de sus transacciones"""
    ]
    
    for ejemplo in ejemplos:
        if st.button(f"📝 {ejemplo}", key=f"ej_{hash(ejemplo)}"):
            # Agregar directamente al chat input
            st.session_state.messages.append({"role": "user", "content": ejemplo})
            st.rerun()
    
    if st.button("🔄 Limpiar historial"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🔧 Debug Info")
    
    if st.button("🧪 Test Agent Info"):
        try:
            from agent import root_agent
            st.success(f"✅ Agente cargado: {root_agent.name}")
            st.info(f"Descripción: {root_agent.description}")
            
            # Mostrar información adicional del agente
            agent_info = []
            if hasattr(root_agent, 'model'):
                agent_info.append(f"Modelo: {root_agent.model}")
            if hasattr(root_agent, 'tools'):
                agent_info.append(f"Herramientas: {len(root_agent.tools)} disponibles")
            if hasattr(root_agent, '__class__'):
                agent_info.append(f"Clase: {root_agent.__class__.__name__}")
            
            # Mostrar métodos disponibles
            methods = [m for m in dir(root_agent) if not m.startswith('_') and callable(getattr(root_agent, m))]
            agent_info.append(f"Métodos: {', '.join(methods[:10])}")
            
            for info in agent_info:
                st.info(info)
                
        except Exception as e:
            st.error(f"❌ Error agent: {e}")
    
    if st.button("🧪 Test Simple Query"):
        try:
            test_response = run_agent_query("Di 'Hola, el agente funciona correctamente'")
            st.success("✅ Respuesta del agente:")
            st.info(test_response)
        except Exception as e:
            st.error(f"❌ Error en test: {e}")
            
    if st.button("🧪 Test BigQuery Direct"):
        try:
            from tools.run_sql_query import run_sql_query
            test_result = run_sql_query("SELECT 1 as test, 'BigQuery Conectado' as status")
            st.success("✅ BigQuery conectado")
            st.code(test_result)
        except Exception as e:
            st.error(f"❌ Error BigQuery: {e}")
    
    if st.button("🧪 Ver Dependencias"):
        import pkg_resources
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        
        # Filtrar paquetes relevantes
        relevant_packages = [p for p in installed_packages if 
                            'google' in p.lower() or 
                            'adk' in p.lower() or 
                            'streamlit' in p.lower() or
                            'bigquery' in p.lower()]
        
        if relevant_packages:
            st.info("Paquetes relevantes instalados:")
            for package in sorted(relevant_packages):
                st.code(package)
        else:
            st.warning("No se encontraron paquetes ADK/Google instalados")