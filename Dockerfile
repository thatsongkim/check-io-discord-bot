FROM python:3

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        discord.py \
        pymongo

CMD [ "python", "./main.py" ]