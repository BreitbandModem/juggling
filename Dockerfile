FROM python:3.8.2-slim-buster

RUN pip install Flask

ENTRYPOINT ["python3"]
CMD ["/app.py"]