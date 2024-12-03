FROM python:3.13.0-slim-bookworm
WORKDIR /usr/src/app
COPY requirements.txt ./
EXPOSE 8000
RUN apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash" , "build_script_for_dockerfile.sh"]
