FROM python:3.12-slim

ARG INDEX_DIR=index
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY prompts/ prompts/
COPY schema/ schema/
COPY ${INDEX_DIR}/ index/

RUN useradd -m -u 10001 appuser
USER 10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
