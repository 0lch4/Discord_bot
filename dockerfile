FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY polecenie_muzyki/ ./polecenie_muzyki/
COPY wyniki/ ./wyniki/
COPY nauka.json ./
COPY olchus.py ./

EXPOSE 8000

CMD [ "python", "./olchus.py" ]