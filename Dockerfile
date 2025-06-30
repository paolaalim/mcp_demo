# Dockerfile CORRIGIDO

# Passo 1: Use uma imagem oficial do Python como base.
FROM python:3.13

# Passo 2: Defina o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Passo 3: Copie a "lista de compras" para dentro do contêiner.
COPY requirements.txt .

# Passo 4: Instale todas as dependências listadas.
RUN pip install --no-cache-dir -r requirements.txt

# Passo 5: Copie todo o código do nosso projeto para o diretório de trabalho no contêiner.
COPY . .

# Passo 6: Exponha a porta que o nosso servidor usará.
EXPOSE 8080

# Passo 7: O comando para iniciar o servidor quando o contêiner rodar.
# A linha abaixo é a única que muda. Agora aponta para 'servidor_web:app'.
CMD ["uvicorn", "servidor_web:app", "--host", "0.0.0.0", "--port", "8080"]
