FROM python:3.9-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs python (opcional, mas previne erros com pandas/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copia e instala requerimentos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8050

# Comando para iniciar a aplicação usando Gunicorn
# app:server significa -> arquivo 'app.py' : objeto 'server'
# --workers=2 é suficiente para um app leve. Se tiver muita memória, pode aumentar.
CMD ["gunicorn", "--workers=2", "--threads=2", "-b", "0.0.0.0:8050", "app:server"]