CREATE TABLE IF NOT EXISTS teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teamname VARCHAR(10) NOT NULL,
    user JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
