FROM ubuntu:latest

# Create a working directory
WORKDIR /app/service

# Copy source code to working directory
COPY . /app/service/

# update apt packages, install python and pip Install packages from requirements.txt and run migrations
RUN apt-get update && \
    apt-get install --no-install-recommends -y locales python3.10 python3-pip python3.10-dev && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py collectstatic

ENV LANG en_US.utf8

# Expose port 80
EXPOSE 80

# Run server at container launch
CMD [ "python3", "manage.py", "runserver", "80" ]

