# Dockerfile para o TESTE DE ISOLAMENTO

FROM python:3.13

WORKDIR /app

# Para este teste, vamos instalar as dependências diretamente
# em vez de usar o requirements.txt
RUN pip install fastapi uvicorn

# Copia APENAS o nosso novo arquivo de teste para o contêiner
COPY teste_minimo.py .

EXPOSE 8080

# Executa o nosso servidor de teste mínimo
CMD ["uvicorn", "teste_minimo:app", "--host", "0.0.0.0", "--port", "8080"]
