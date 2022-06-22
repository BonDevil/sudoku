# Dockerfile, Image, Container
FROM python:3.10.5

ADD Button.py .
ADD GameApp.py .
ADD main.py .
ADD Solver.py .
ADD SolverApp.py .

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

CMD ["python", "./main.py"]