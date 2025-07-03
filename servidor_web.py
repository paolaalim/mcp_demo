# servidor_web.py (VERSÃO FINAL COM CORS PARA TESTE LOCAL)

import re
from collections import Counter
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # IMPORTANTE: Importar o Middleware CORS

# --- Criação das Aplicações ---
app = FastAPI()

# --- Configuração do CORS ---
# Adicione esta secção para permitir que o seu frontend (rodando localmente)
# possa fazer requisições para este servidor.
origins = [
    "null", # Necessário para permitir requisições de ficheiros locais (file://)
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

mcp = FastMCP("MeuServidorMCP", stateless_http=True)

# --- Endpoint de Health Check ---
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Servidor MCP está saudável!"}

# --- Montagem da Aplicação MCP ---
app.mount("/mcp", mcp.streamable_http_app())

# --- Lógica do Servidor MCP (Ferramentas, etc.) ---
# O resto do seu código de ferramentas e prompts permanece exatamente o mesmo.
@mcp.tool()
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    if not palavras: return "Nenhuma palavra encontrada no texto."
    contagem = Counter(palavras)
    resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
    return f"Frequência de palavras: {resultado_str}"