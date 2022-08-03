FROM alpine:3.15 


WORKDIR /usr/src/app
# Copy files
COPY crontab.* ./
COPY . ./
ENV PATH=$PATH:/.env
# Install required packages
RUN apk add --update --no-cache bash dos2unix tor
RUN apk --update add redis 
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip  install -r requirement.txt
# Fix line endings && execute permissions
RUN dos2unix crontab.* \
    && \
    find . -type f -iname "*.sh" -exec chmod +x {} \;
CMD  ["./my_wrapper_script.sh"]


#run command :-  docker run --env-file ./.env --name crawler chiragjakhariya/hc_crawler_docker
