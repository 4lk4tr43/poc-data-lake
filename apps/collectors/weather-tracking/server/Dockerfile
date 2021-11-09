FROM python

ADD requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -U pylint pyyaml watchdog
RUN pip install -r requirements.txt

ADD . /app

ENTRYPOINT watchmedo auto-restart --directory="./" --pattern="*.py" --recursive -- python -u /app/src/main.py