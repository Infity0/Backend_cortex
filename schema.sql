CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    token_balance INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_code VARCHAR(6),
    verification_code_expires DATETIME,
    reset_token VARCHAR(255),
    reset_token_expires DATETIME,
    avatar_url VARCHAR(255),
    INDEX idx_email (email),
    INDEX idx_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE SUBSCRIPTION_PLANS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    tokens_included INT NOT NULL,
    duration_days INT NOT NULL,
    description VARCHAR(255),
    note VARCHAR(255),
    INDEX idx_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE SUBSCRIPTIONS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT NOT NULL,
    SUBSCRIPTION_PLANS_id INT NOT NULL,
    start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME NOT NULL,
    status ENUM('active','inactive','cancelled') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    auto_renew TINYINT(1) DEFAULT 1,
    INDEX idx_id (id),
    INDEX idx_user_id (User_id),
    FOREIGN KEY (User_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (SUBSCRIPTION_PLANS_id) REFERENCES SUBSCRIPTION_PLANS(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE TRANSACTIONS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT NOT NULL,
    SUBSCRIPTIONS_id INT,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    INDEX idx_id (id),
    INDEX idx_user_id (User_id),
    FOREIGN KEY (User_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (SUBSCRIPTIONS_id) REFERENCES SUBSCRIPTIONS(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE REQUESTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT NOT NULL,
    request_type VARCHAR(50),
    input_text VARCHAR(500),
    input_image_url VARCHAR(255),
    tokens_used INT,
    status ENUM('pending','processing','completed','failed') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    style VARCHAR(50),
    resolution VARCHAR(20),
    error_message VARCHAR(500),
    INDEX idx_id (id),
    INDEX idx_user_id (User_id),
    INDEX idx_status (status),
    FOREIGN KEY (User_id) REFERENCES User(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IMAGES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT NOT NULL,
    REQUESTS_id INT,
    image_url VARCHAR(255) NOT NULL,
    original_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_favorite BOOLEAN DEFAULT FALSE,
    INDEX idx_id (id),
    INDEX idx_user_id (User_id),
    INDEX idx_favorite (is_favorite),
    FOREIGN KEY (User_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (REQUESTS_id) REFERENCES REQUESTS(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO SUBSCRIPTION_PLANS (name, price, tokens_included, duration_days, description, note) VALUES
('Sirdar', 0.00, 1000, 3, 'Trial plan', 'Free 3-day trial with 1000 tokens'),
('Expert', 1500.00, 24000, 30, 'Advanced plan', '1500 RUB/month with 24000 tokens'),
('Lord', 12000.00, 999999, 365, 'Professional plan', '12000 RUB/year with unlimited tokens');
