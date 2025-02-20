# SQL Whisper

![Demo Video](./demo.gif)

## Summary

The project is split into two parts:

1. SQL Whisper: a [workflow](sqlwhisper/workflow.py) that goes from text to `pd.DataFrame`
2. A small [problem set](./PROBLEM.md) to [study](solutions/) edge cases in the text to sql problem space.

> The only code and ideas that were generated with llm's are under `populate_db` and some .md formatting.
> Everything else was written without gpt.

### SQL Whisper

1. User inputs query
2. LLM validates it
3. If valid, creates SQL query
4. SQL query is executed.

![image](./workflow.png)

## Missing features

- Better file organization
- Error handling (e.g. try catch during sql execution)
- Linting/Formatting
- Comments

## Setup

### Poetry

Make sure to have poetry installed, and then install all dependencies and get the venv setup run

```bash
poetry install
```

Note that every python command needs to be run from the venv, the easiest way to do this is to run ```poetry shell```. Note that if you are using Neovim, this well then also help the lsp point to the right executable.

### PostgreSQL

Before running the example code the PostgreSQL server must be setup and populated.

Setup is done via docker, make sure to add the credentials in a .env file at the root of the directory.

```bash
docker run --name db_name -p 5432:5432 -e POSTGRES_USER=your_user -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=stock_data -v pgdata:/var/lib/postgresql/data -d postgres:latest
```

Connect to the db to check if it's running.

```bash
psql -h localhost -p 5432 -U your_user -d table_name
```

To populate the db run 

```bash
python populate_db/yfinance_loader.py
python populate_db/toy_loader.py
python populate_db/artist_loader.py
```

### Demo

Once you have everything setup you should be able to run the demo

`python demo.py`
