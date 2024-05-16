
FROM python:3.9
RUN mkdir /xnermusic
WORKDIR /xnermusic
RUN pip install --upgrade  pip

RUN pip install virtualenv

RUN pip install flask
RUN pip install music21
RUN pip install aubio
#RUN pip install music21
#RUN pip install aubio
RUN pip install librosa
RUN pip install Flask Flask-SQLAlchemy psycopg2-binary
#COPY . /srv



COPY . /xnermusic

ENV FLASK_APP=app
CMD ["python","app.py"]