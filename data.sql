CREATE DATABASE todo_app;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE todos (
    todo_id SERIAL PRIMARY KEY,
    todo VARCHAR(255) NOT NULL,
    deadline TIMESTAMP,
    priority INTEGER,
    finish_flg BOOLEAN DEFAULT FALSE,
    estimated_time INTEGER,
    user_id INTEGER NOT NULL,
    delete_flg BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);


CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE todo_to_tag (
    id SERIAL PRIMARY KEY,
    todo_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    delete_flg BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_todo
        FOREIGN KEY(todo_id)
        REFERENCES todos(todo_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_tag
        FOREIGN KEY(tag_id)
        REFERENCES tags(tag_id)
        ON DELETE CASCADE,
    CONSTRAINT unique_todo_tag UNIQUE (todo_id, tag_id) -- 同じ組み合わせの重複を防ぐ
);
