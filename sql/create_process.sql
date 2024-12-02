CREATE TABLE IF NOT EXISTS process (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idtask INT(50) NOT NULL,
    procesname VARCHAR(50) NOT NULL,
    procesdetails VARCHAR(50) NOT NULL,
    processtart INT NOT NULL,
    procesend DATE NOT NULL,
    processisvisible BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
