CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) NOT NULL,
    usernamecode VARCHAR(10) NOT NULL,
    password VARCHAR(10) NOT NULL,
    BranchDepartment ENUM('01', '02', '03') DEFAULT '03',
    jobposition ENUM('01', '02', '03') DEFAULT '03',
    Branch ENUM('01', '02') DEFAULT '02',
    level ENUM('01', '02') DEFAULT '02',
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    neckname VARCHAR(100),
    mail VARCHAR(50),
    phoneNumber VARCHAR(10),
    internal_contact_number VARCHAR(10),
    LINEID VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);