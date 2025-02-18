# Stock Whisper

## Setup

### Poetry

To install all dependencies and get the venv setup run

```bash
poetry install
```

Note that every python command needs to be run from the venv, the easiest way to do this is to run ```poetry shell```. Note that if you are using Neovim, this well then also help the lsp point to the right executable.


### PostgreSQL

Before running the example code the PostgreSQL server must be setup and populated.

Setup is done via docker, make sure to add the credentials in a .env file at the root of the directory.

```bash
docker run --name stock_db -p 5432:5432 -e POSTGRES_USER=your_user -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=stock_data -v pgdata:/var/lib/postgresql/data -d postgres:latest
```

Connect to the db to check if it's running.

```bash
psql -h localhost -p 5432 -U nacho -d stock_data
```

To populate the db run 

```bash
python populate_db/yfinance_loader.py
```

### Stockwhisper

You should now be able to run files under ```/examples```
