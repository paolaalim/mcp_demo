# Dockerfile para o TESTE DE ISOLAMENTO com a PORTA 8000

FROM python:3.13

WORKDIR /app

# Para este teste, vamos instalar as dependências diretamente
RUN pip install fastapi uvicorn

# Copia APENAS o nosso novo arquivo de teste para o contêiner
COPY servidor_web.py .

# MUDANÇA 1: Expondo a nova porta
EXPOSE 8000

# MUDANÇA 2: Executando o servidor na nova porta
CMD ["uvicorn", "servidor_web:app", "--host", "0.0.0.0", "--port", "8000"]
