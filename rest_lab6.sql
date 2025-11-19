DROP DATABASE IF EXISTS rest_lab6;
CREATE DATABASE rest_lab6 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rest_lab6;

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(120) NOT NULL,
    last_name VARCHAR(120) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    active TINYINT(1) NOT NULL DEFAULT 1,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_first_name (first_name),
    INDEX idx_users_last_name (last_name),
    INDEX idx_users_birth_date (birth_date),
    INDEX idx_users_role (role),
    INDEX idx_users_active (active)
);

ALTER TABLE users
    ADD CONSTRAINT chk_users_role CHECK (role IN ('user','admin'));

CREATE TABLE posts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    link VARCHAR(512),
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_posts_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_posts_title (title),
    INDEX idx_posts_user (user_id)
);

CREATE TABLE comments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    body TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_comments_post FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_comments_user (user_id),
    INDEX idx_comments_post (post_id)
);

INSERT INTO users (first_name, last_name, birth_date, email, active, role) VALUES
    ('Іван', 'Петренко', '1997-05-04', 'ivan.petrenko@example.com', 1, 'admin'),
    ('Марія', 'Сидоренко', '1999-09-17', 'mariia.sydorenko@example.com', 1, 'user'),
    ('Андрій', 'Левченко', '2001-02-11', 'andrii.levchenko@example.com', 0, 'user');

INSERT INTO posts (title, body, link, user_id) VALUES
    ('Нові можливості застосунку', 'Ділимося планами з оновлень...', 'https://example.com/news/roadmap', 1),
    ('Поради з безпеки', 'Перевірте налаштування 2FA...', NULL, 1),
    ('Огляд нашої конференції', 'Коротко про враження та матеріали...', 'https://example.com/blog/conference', 2);

INSERT INTO comments (body, user_id, post_id) VALUES
    ('Чекаю на реліз!', 2, 1),
    ('Дякую за нагадування', 3, 2),
    ('Було дуже корисно, дякую!', 1, 3);
