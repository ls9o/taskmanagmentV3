CREATE TABLE IF NOT EXISTS subtasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idtask INT(50) NOT NULL,
    subinfodetails VARCHAR(50) NOT NULL,
    subinfostart DATE NOT NULL,
    subinfoend DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
