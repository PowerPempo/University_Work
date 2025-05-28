CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

CREATE TABLE shares (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) NOT NULL,
    ticker_symbol VARCHAR(10) UNIQUE NOT NULL,
    total_shares BIGINT NOT NULL,
    outstanding_shares BIGINT NOT NULL,
    par_value DECIMAL(10, 2) DEFAULT 0.00,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL, -- Помните о безопасности!
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    balance DECIMAL(15, 2) DEFAULT 0.00
);

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    share_id INTEGER REFERENCES shares(id) NOT NULL,
    quantity BIGINT NOT NULL,
    average_purchase_price DECIMAL(10,2),
    UNIQUE (user_id, share_id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    share_id INTEGER REFERENCES shares(id) NOT NULL,
    order_type VARCHAR(4) NOT NULL CHECK (order_type IN ('BUY', 'SELL')),
    quantity BIGINT NOT NULL,
    price DECIMAL(10, 2), -- NULLable for market orders
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'EXECUTED', 'CANCELLED', 'PARTIALLY_EXECUTED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    buy_order_id INTEGER REFERENCES orders(id),
    sell_order_id INTEGER REFERENCES orders(id),
    buyer_id INTEGER REFERENCES users(id),
    seller_id INTEGER REFERENCES users(id),
    share_id INTEGER REFERENCES shares(id) NOT NULL,
    quantity BIGINT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    trade_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);