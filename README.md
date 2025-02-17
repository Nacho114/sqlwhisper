# Stock Whisper

## PostgreSQL

It was run using (it persists data in volume)

```bash
docker run --name stock_db -p 5432:5432 -e POSTGRES_USER=your_user -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=stock_data -v pgdata:/var/lib/postgresql/data -d postgres:latest
```

Connect to the db

```bash
psql -h localhost -p 5432 -U nacho -d stock_data
```
