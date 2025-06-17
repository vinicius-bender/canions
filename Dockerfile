# Use a imagem oficial do PythonAdd commentMore actions
FROM python:3.12-slim

# Instala as dependências necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho (note que estou usando o nome que aparece no seu erro)
WORKDIR /canionsDoSul

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências
COPY requirements.txt /canionsDoSul/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto
COPY . /canionsDoSul/

# FROM python:3.12-slim

# # Instalar dependências de sistema
# RUN apt-get update && apt-get install -y \
#     postgresql-client \
#     libpq-dev \
#     gcc \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /canionsDoSul

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# COPY requirements.txt /canionsDoSul/
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /canionsDoSul/

# # Use a imagem oficial do Python
# FROM python:3.12-slim

# # Instala as dependências necessárias para psycopg2
# RUN apt-get update && apt-get install -y \
#     postgresql-client \
#     libpq-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Define o diretório de trabalho (note que estou usando o nome que aparece no seu erro)
# WORKDIR /canionsDoSul

# # Define variáveis de ambiente
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Instala as dependências
# COPY requirements.txt /canionsDoSul/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copia o projeto
# COPY . /canionsDoSul/