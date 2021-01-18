FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update
RUN apt-get install curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -y install nodejs
RUN apt-get -y install python3-dev graphviz libgraphviz-dev pkg-config

COPY ./backend /app
RUN pip install -r requirements.txt

COPY ./frontend /frontend
RUN mkdir -p /app/static
RUN npm install --prefix /frontend
RUN npm run build --prefix /frontend
RUN mv /frontend/build/* /app/static/
RUN rm -rf /frontend
