CREATE TABLE IF NOT EXISTS subprocess (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idprocess INT(50) NOT NULL,
    subprocesdetails VARCHAR(50) NOT NULL,
    subprocesstart INT NOT NULL,
    subprocesend DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
