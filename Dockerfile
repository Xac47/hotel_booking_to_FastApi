FROM python:3.12

RUN mkdir /booking
WORKDIR /booking

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl rustc cargo ca-certificates && update-ca-certificates


RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN export PATH="$HOME/.cargo/bin:$PATH" && rustup install stable && rustup default stable


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]