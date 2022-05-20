FROM python:3.9 as build-app

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Update apt and install node.js
RUN apt-get update && apt-get install -y nodejs npm

ADD ./admin/ /app/admin
ADD ./plugins/ /app/admin/plugins/
ADD ./client/ /app/client
ADD ./plugins/ /app/client/plugins/
ADD ./misago/bootstrap /app/
ADD ./misago/requirements.txt /app/
ADD ./misago/requirements-dev.txt /app/
ADD ./misago/setup.py /app/
ADD ./misago/misago/ /app/misago/
ADD ./plugins/ /app/plugins/

RUN cd ./app/admin && npm install
RUN cd ./app/admin && ./bootstrap deploy
RUN cd ./app/client && npm install
RUN cd ./app/client && ./bootstrap deploy
RUN pip install --upgrade pip
RUN ./app/bootstrap dependencies
RUN ./app/bootstrap plugins

# Build final (slim) image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/"
ENV IN_MISAGO_DOCKER 1

# Copy python dependencies from previous image
COPY --from=build-app /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-app /usr/local/bin/ /usr/local/bin/
COPY --from=build-app /app/admin/build/ /app/admin/build/
COPY --from=build-app /app/admin/build/ /app/client/build/

# Update apt and install postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# Re-add misago
ADD ./misago/bootstrap /app/bootstrap
ADD ./misago/misagocli.py /app/misagocli.py
ADD ./misago/setup.py /app/
ADD ./misago/misago/ /app/misago/
ADD ./plugins/ /app/plugins/

WORKDIR /app/

# Run APP
EXPOSE 8000

CMD uvicorn misago.asgi:app --host 0.0.0.0
