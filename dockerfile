# --- Estágio 1: Build da Aplicação ---
# Define a imagem base do Python que será usada.
# 'python:3.9-slim' é uma boa escolha por ser leve e estável.
FROM python:3.11-alpine

# Define o diretório de trabalho dentro do contêiner.
# Todos os comandos a seguir serão executados a partir deste diretório.
WORKDIR /app

# Atualiza o pip para garantir que temos a versão mais recente.
RUN pip install --upgrade pip

# Copia o arquivo de dependências (requirements.txt) para o contêiner.
# Copiamos este arquivo primeiro para aproveitar o cache do Docker.
# Se o requirements.txt não mudar, o Docker não precisará reinstalar as dependências a cada build.
COPY requirements.txt requirements.txt

# Instala as dependências Python definidas no requirements.txt.
RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copia todo o resto do código da sua aplicação para o diretório de trabalho no contêiner.
COPY . .

# Expõe a porta que sua aplicação Python usa para se comunicar.
# Altere 5000 para a porta correta se sua aplicação usar uma diferente (ex: 8000 para FastAPI).
EXPOSE 5000

# O comando que será executado quando o contêiner iniciar.
# Altere "app.py" para o nome do seu arquivo principal da aplicação Python.
CMD [ "python", "-u", "main.py" ]
