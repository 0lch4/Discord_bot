FROM python:3.11

WORKDIR /bot

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY ./ .

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 3000

CMD [ "python","-m", "bot.bot" ]
