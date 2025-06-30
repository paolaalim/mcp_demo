# servidor.py (VERSÃO FINAL COM HEALTH CHECK)

# --- Imports ---
import re
from collections import Counter
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context
import asyncio
from fastapi import FastAPI # Importamos o FastAPI

# --- Criação das Aplicações ---
# 1. Crie a aplicação FastAPI principal. Esta será a nossa porta de entrada.
app = FastAPI()

# 2. Crie a aplicação MCP como antes.
mcp = FastMCP("MeuServidorMCP", stateless_http=True)

# --- Endpoint de Health Check ---
# 3. Adicione uma rota na aplicação FastAPI principal.
# Esta rota responderá na raiz (/) com uma mensagem de sucesso.
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Servidor MCP está saudável!"}

# --- Montagem da Aplicação MCP ---
# 4. "Monte" a aplicação MCP para que ela responda no caminho /mcp
# Isto significa que todas as requisições do protocolo MCP irão para http://sua_url/mcp
app.mount("/mcp", mcp.streamable_http_app())

# --- Lógica do Servidor MCP (Ferramentas, etc.) ---
# O resto do seu código de ferramentas e prompts permanece exatamente o mesmo.

@mcp.resource("meuMCP://about")
def get_assistant_capabilities() -> str:
    """Descreve as principais ferramentas e o propósito deste assistente."""
    return "Descrição das ferramentas..." # (código omitido para brevidade)

@mcp.tool()
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    if not palavras: return "Nenhuma palavra encontrada no texto."
    contagem = Counter(palavras)
    resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
    return f"Frequência de palavras: {resultado_str}"
    
@mcp.tool()
async def registrar_log_interno(mensagem: str, ctx: Context) -> str:
    """Registra uma mensagem nos logs internos do servidor MCP."""
    await ctx.info(f"Log via ferramenta: {mensagem}")
    return f"Mensagem '{mensagem}' registrada nos logs."

# (O resto das suas ferramentas e prompts aqui...)

# O bloco if __name__ == "__main__" não é mais necessário,
# pois o uvicorn irá gerir a execução da aplicação 'app'.
