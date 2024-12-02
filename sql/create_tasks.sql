CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    infoname VARCHAR(50) NOT NULL,
    infodetails VARCHAR(50) NOT NULL,
    infostart DATE NOT NULL,
    infoend DATE NOT NULL,
    infotype VARCHAR(50) NOT NULL,
    manager VARCHAR(50) NOT NULL,
    userandteam JSON NOT NULL,
    dayDiff INT(50) NOT NULL,
    progressPercentage INT(50) NOT NULL,
    statusprogress INT(50) NOT NULL,
    create_by   VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
