CREATE TABLE IF NOT EXISTS users (
    userid    INT  UNIQUE,
    username  TEXT,
    balance   DECIMAL
    dotaid    INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wallets (
    address TEXT UNIQUE,
    name    TEXT
);