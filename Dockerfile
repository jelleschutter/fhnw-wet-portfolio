FROM python:3.13 AS builder
RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./portfolio/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13
RUN useradd -m -r appuser && \
  mkdir /app && \
  chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser ./portfolio/ .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "portfolio.wsgi:application"]
