-- Create users table
CREATE TABLE users (
    username text PRIMARY KEY,
    password text,
    following text[],
    one text,
    two text,
    three text,
    description text
);
