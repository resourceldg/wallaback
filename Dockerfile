FROM python:3.8.1-slim 


# Copy requirements from host, to docker container in /app 
COPY ./requirements.txt .
# Copy everything from ./app directory to /app in the container
COPY ./app . 
# Install the dependencies
RUN pip install --no-deps -r requirements.txt
RUN pip install psycopg2-binary
# Run the application in the port 8000
ENTRYPOINT [ "uvicorn" ]
CMD ["--host", "0.0.0.0", "--port", "8000", "app.main:app"]
