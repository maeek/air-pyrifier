FROM python:3.8-alpine

COPY requirements.txt ./
RUN apk add --no-cache gcc musl-dev git && \
  pip install --no-cache-dir -r requirements.txt && \
  pip3 install -U git+https://github.com/Tanganelli/CoAPthon3 && \
  apk del gcc musl-dev git

WORKDIR /srv
USER 1000

CMD ["./src/air_server.py"]
