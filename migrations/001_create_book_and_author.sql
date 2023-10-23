CREATE TYPE genre AS ENUM ('fiction', 'non_fiction');

CREATE TABLE authors
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE books
(
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(150) NOT NULL,
    genre          genre        NOT NULL,
    date_published DATE         NOT NULL,
    restricted     bool         not null default false,
    file_name       varchar(150) not null default ''
);

CREATE TABLE authors_books
(
    author_id INTEGER NOT NULL REFERENCES authors (id),
    book_id   INTEGER NOT NULL REFERENCES books (id),
    PRIMARY KEY (author_id, book_id)
);