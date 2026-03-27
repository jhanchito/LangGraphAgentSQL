## #######################################################################################################
##
## @copyright Integratel
## @author Jhampier Tapia [jhampier.tapia@integratel.com.pe]
##
## #######################################################################################################

## #######################################################################################################
## @section Librerías
## #######################################################################################################

#Utilitario para construir un servidor MCP
from mcp.server.fastmcp import FastMCP

## #######################################################################################################
## @section Servidor MCP
## #######################################################################################################

#Creamos el servidor MCP
SERVER_MCP_CALCULADORA = FastMCP("Calculadora")

## #######################################################################################################
## @section Tools del servidor MCP
## #######################################################################################################

@SERVER_MCP_CALCULADORA.tool()
def sumar(a: float, b: float) -> float:
    """Suma dos números"""
    return a + b

@SERVER_MCP_CALCULADORA.tool()
def restar(a: float, b: float) -> float:
    """Resta dos números"""
    return a - b

@SERVER_MCP_CALCULADORA.tool()
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números"""
    return a * b

@SERVER_MCP_CALCULADORA.tool()
def dividir(a: float, b: float) -> float:
    """Divide dos números"""
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a / b

## #######################################################################################################
## @section Ejecución del servidor
## #######################################################################################################

#Ejecutamos el script del servidor
if __name__ == "__main__":

    #Lo ejecutamos en segundo plano
    SERVER_MCP_CALCULADORA.run(transport="stdio")