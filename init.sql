-- COMMENT: setup
CREATE DATABASE graphs;
CREATE extension age;
LOAD 'age';
GRANT USAGE ON SCHEMA ag_catalog TO postgres;
SET search_path = ag_catalog, postgres, public;

-- COMMENT: from here we can start to dig into stuff
SELECT * FROM ag_catalog.create_graph('starting_here');
