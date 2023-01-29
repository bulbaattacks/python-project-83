CREATE TABLE IF NOT EXISTS urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(755) unique,
    created_at timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    status_code integer,
    h1 varchar(755),
    title varchar(755),
    description varchar(755),
    created_at timestamp DEFAULT now(),
    url_id bigint REFERENCES urls (id)
);