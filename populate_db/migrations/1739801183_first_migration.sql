CREATE TABLE futures_data (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    trade_date TIMESTAMPTZ NOT NULL,  -- Using TIMESTAMPTZ
    open_price DECIMAL(19, 4),
    high_price DECIMAL(19, 4),
    low_price DECIMAL(19, 4),
    close_price DECIMAL(19, 4),
    volume BIGINT,
    source VARCHAR(50),        -- Added source column
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Added updated_at column
    CONSTRAINT unique_data_point UNIQUE (symbol, trade_date)
);

CREATE INDEX idx_symbol_trade_date ON futures_data (symbol, trade_date);
