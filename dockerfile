FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY music_recomendation/ ./music_recomendation/
COPY results/ ./results/
COPY data.json ./
COPY bot.py ./

EXPOSE 8000

CMD [ "python", "./bot.py" ]