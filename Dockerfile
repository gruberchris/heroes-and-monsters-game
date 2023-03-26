FROM python:3.11-alpine
WORKDIR /app
ADD heroes_and_monsters_game.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "/app/heroes_and_monsters_game.py"]