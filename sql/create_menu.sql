CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Menuname VARCHAR(100) NOT NULL,
    MenuUrl VARCHAR(100) NOT NULL,
    Menuview VARCHAR(100) NOT NULL,
    icon VARCHAR(100)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);