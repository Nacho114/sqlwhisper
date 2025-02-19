CREATE TABLE testing_data (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(19, 4)
);
