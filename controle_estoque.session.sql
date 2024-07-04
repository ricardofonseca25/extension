CREATE TABLE materiais (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(50),
    tipo VARCHAR(50),
    unidademed VARCHAR(50),
    quantidade NUMERIC(10, 2)
);

SELECT * from materiais