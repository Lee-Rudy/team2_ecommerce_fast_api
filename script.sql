PRAGMA foreign_keys = ON;

CREATE TABLE
    users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME
    );

CREATE TABLE
    products (
        id_product INTEGER PRIMARY KEY AUTOINCREMENT,
        name_product TEXT NOT NULL,
        description_product TEXT,
        brand TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME
    );

CREATE TABLE
    categories (
        id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name_category TEXT NOT NULL UNIQUE,
        description_category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME
    );

CREATE TABLE
    product_categories (
        id_product INTEGER,
        id_category INTEGER,
        PRIMARY KEY (id_product, id_category),
        FOREIGN KEY (id_product) REFERENCES products (id_product) ON DELETE CASCADE,
        FOREIGN KEY (id_category) REFERENCES categories (id_category) ON DELETE CASCADE
    );

CREATE TABLE
    stock_movements (
        id_stock_movement INTEGER PRIMARY KEY AUTOINCREMENT,
        id_product INTEGER,
        movement_type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_product) REFERENCES products (id_product) ON DELETE CASCADE
    );

CREATE TABLE
    log (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        action TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES users (id_user) ON DELETE SET NULL
    );

CREATE INDEX idx_products_name ON products (name_product);

CREATE INDEX idx_products_price ON products (price);

CREATE INDEX idx_products_stock ON products (stock_quantity);

CREATE INDEX idx_categories_name ON categories (name_category);