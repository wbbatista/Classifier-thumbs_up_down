FROM python:3.7

COPY . /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit","run", "app.py"]

