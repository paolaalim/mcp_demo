# servidor.py

import re
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Modelos de Dados para a nossa API ---
# Define a estrutura que o nosso frontend deve enviar
class ToolRequest(BaseModel):
    arguments: dict

# --- Aplicação FastAPI ---
app = FastAPI()

# Configuração do CORS para permitir que o nosso frontend se conecte
# ATENÇÃO: Em produção real, seria mais restrito, mas para o Easypanel e testes, "*" funciona.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Nossas Ferramentas ---
# As funções são as mesmas, mas sem o decorador @mcp.tool()
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    if not palavras:
        return "Nenhuma palavra encontrada no texto."
    contagem = Counter(palavras)
    resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
    return f"Frequência de palavras: {resultado_str}"

def add(a: int, b: int) -> int:
    """Soma dois números inteiros."""
    return a + b

# Um "registo" manual das nossas ferramentas
ferramentas_disponiveis = {
    "contar_frequencia": contar_frequencia_palavras,
    "somar": add,
}

# --- Endpoints da API ---
@app.get("/")
def health_check():
    """Endpoint de saúde para o Easypanel saber que o serviço está no ar."""
    return {"status": "ok"}

@app.post("/tool/{tool_name}")
def execute_tool(tool_name: str, request: ToolRequest):
    """Endpoint principal que recebe o nome da ferramenta e os seus argumentos."""
    if tool_name not in ferramentas_disponiveis:
        raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
    
    try:
        ferramenta = ferramentas_disponiveis[tool_name]
        # Executa a função da ferramenta com os argumentos recebidos
        resultado = ferramenta(**request.arguments)
        return {"result": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar a ferramenta: {e}")
