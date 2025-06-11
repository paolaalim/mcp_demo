# servidor_web.py

# --- Imports ---
# Importamos FastMCP, a forma mais fácil de criar um servidor,
# e Context, para acessar funcionalidades internas do MCP.
from mcp.server.fastmcp import FastMCP, Context

# --- 1. Inicialize o Servidor ---
# Criamos uma instância do nosso servidor com um nome único.
# O parâmetro 'stateless_http=True' é importante! Ele configura o servidor
# para rodar em modo HTTP sem manter estado de sessão, ideal para deploy.
mcp = FastMCP("MeuServidorWeb", stateless_http=True)
print(f"Servidor MCP '{mcp.name}' configurado para rodar via HTTP.")


# --- 2. Defina um RESOURCE (Informação de Contexto) ---
# Resources fornecem contexto sobre o que seu servidor pode fazer.
# Usamos o decorador @mcp.resource com uma URI estática.
@mcp.resource("meuServidorWeb://about")
def get_server_description() -> str:
    """
    Descreve o propósito e as ferramentas deste servidor.
    Esta informação é lida pelo cliente MCP para entender as capacidades.
    """
    print("-> Resource 'meuServidorWeb://about' foi solicitado.")
    description = (
        "Olá! Eu sou um servidor MCP de exemplo, criado com o Parceiro de Programação.\n"
        "Minhas capacidades atuais incluem:\n"
        "1. **Saudação Personalizada:** Uma ferramenta que gera uma saudação para um nome específico."
    )
    return description


# --- 3. Defina uma TOOL (Ação que a IA pode chamar) ---
# Tools são as funções que a IA pode decidir executar para responder a um pedido.
# A docstring (o texto entre aspas triplas) é MUITO importante, pois o LLM a usa
# para entender o que a ferramenta faz e quais são seus parâmetros.
@mcp.tool()
def saudacao_personalizada(nome: str, ctx: Context) -> str:
    """
    Gera uma mensagem de saudação calorosa para uma pessoa específica.

    :param nome: O nome da pessoa a ser saudada.
    :param ctx: O objeto de contexto do MCP, usado aqui para logar informações.
    """
    # Usamos o logger do contexto para registrar o que está acontecendo.
    ctx.info(f"-> Ferramenta 'saudacao_personalizada' chamada com o nome: {nome}")
    
    resultado = f"Olá, {nome}! Que seu dia seja repleto de código e sucesso! 🚀"
    
    print(f"Resultado da ferramenta: {resultado}")
    return resultado


# --- 4. Bloco Principal de Execução ---
# Este bloco garante que o servidor só vai rodar quando executarmos o script diretamente.
if __name__ == "__main__":
    # Em vez de mcp.run(), usamos mcp.run(transport="streamable-http")
    # para iniciar o servidor no modo web, pronto para o deploy.
    print("Iniciando o servidor em modo HTTP. Use 'mcp dev servidor_web.py' para testar.")
    # A linha abaixo é para execução direta, mas o modo 'dev' é melhor para testes.
    # mcp.run(transport="streamable-http")
