FROM python:3.13

# set up dependency environment
RUN apt-get update -y && apt-get install -y --no-install-recommends icu-devtools && rm -rf /var/lib/apt/lists/*
# RUN export PATH="/usr/local/opt/icu4c/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy code from action repository to the filesystem path `/` of the container
COPY src/cldr-coverage.py /cldr-coverage.py

# Executes when the Docker container starts up
# GitHub Actions automates arguments from the Action yaml configuration file
ENTRYPOINT ["/cldr-coverage.py"]
