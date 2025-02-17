ALTER TABLE testing_data
ADD CONSTRAINT uq_symbol UNIQUE (symbol);  -- Add unique constraint
