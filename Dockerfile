FROM python:3.8

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY cldr-coverage.py /cldr-coverage.py

# Executes when the Docker container starts up 
ENTRYPOINT ["/cldr-coverage.py"]
