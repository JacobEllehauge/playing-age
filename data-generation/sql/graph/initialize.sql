CREATE DATABASE graphs;

CREATE extension age;
LOAD 'age';
GRANT USAGE ON SCHEMA ag_catalog TO postgres;
SET search_path = ag_catalog, "$user", public;

SELECT * FROM ag_catalog.create_graph('starting_here');



SELECT *
FROM cypher('starting_here', $$
    CREATE (a:Person {name: 'Andres', title: 'Developer'})
    RETURN a
$$) as (a agtype);


SELECT *
FROM cypher('starting_here', $$
    CREATE (a:Person {name: 'Ben', title: 'Developer'})
    RETURN a
$$) as (a agtype);


SELECT *
FROM cypher('starting_here', $$
    MATCH (a:Person), (b:Person)
    WHERE a.name = 'Andres' AND b.name = 'Ben'
    CREATE (a)-[e:HAS_ADRESSE]->(b)
    RETURN e
$$) as (e agtype);


SELECT * FROM cypher('starting_here', $$
 Match (p:Person)-[kk]-(pp:Person) return p, pp, kk
$$) AS (result1 agtype, result2 agtype, result3 agtype);


