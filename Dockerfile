# Passo 1: Use uma imagem oficial do Python como base.
# A versão 'slim' é menor e ideal para produção.
FROM python:3.13

# Passo 2: Defina o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Passo 3: Copie a "lista de compras" para dentro do contêiner.
COPY requirements.txt .

# Passo 4: Instale todas as dependências listadas.
# O '--no-cache-dir' ajuda a manter a imagem final menor.
RUN pip install --no-cache-dir -r requirements.txt

# Passo 5: Copie todo o código do nosso projeto para o diretório de trabalho no contêiner.
COPY . .

# Passo 6: Exponha a porta que o nosso servidor usará.
# O Easypanel usará essa informação para direcionar o tráfego.
EXPOSE 8080

# Passo 7: O comando para iniciar o servidor quando o contêiner rodar.
# Usamos o 'uvicorn' para rodar nosso app em modo de produção.
CMD ["uvicorn", "servidor_web:mcp.streamable_http_app", "--host", "0.0.0.0", "--port", "8080"]
