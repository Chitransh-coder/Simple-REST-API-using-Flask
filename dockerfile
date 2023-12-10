FROM python
EXPOSE 5000
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
CMD [ "flask", "run", "--host", "0.0.0.0" ]