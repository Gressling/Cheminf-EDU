CREATE TABLE cheminf3_project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE cheminf3_task (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    description VARCHAR(255) NOT NULL,
    content TEXT  -- Plain text column to hold JSON or any other large text
);


INSERT INTO cheminf3_project (name) VALUES ('Asprin synthesis optimization');

INSERT INTO cheminf3_task (project_id, description, content) VALUES
(1, 'Optimize step 1', '{"type": "optimization", "step": 1, "parameters": {"temperature": 100, "time": 10}}'),
(1, 'Optimize step 2', '{"type": "optimization", "step": 2, "parameters": {"temperature": 120, "time": 20}}'),
(1, 'Optimize step 3', '{"type": "optimization", "step": 3, "parameters": {"temperature": 140, "time": 30}}');