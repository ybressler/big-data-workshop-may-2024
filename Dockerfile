FROM python:3.11-slim

RUN pip install poetry

COPY poetry.lock pyproject.toml README.md ./
RUN poetry install


COPY src ./src/

CMD ["poetry", "run", "python", "src/create_data/main.py"]
