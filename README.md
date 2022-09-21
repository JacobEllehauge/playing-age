# playing-age
the correct age: 

Intention is to verify the capabilities/current state of apache AGE extension for postgres

1. Spin up postgres with AGE added in docker (y)
2. Add nodes and relations by simulating data (... y)
3. Add viewer container 
4. look at updating, indexing, performance (merging, apoc-likes) 


# random notes
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
GRANT USAGE ON SCHEMA ag_catalog TO db_user;


# Clarify: 
1. use of set path
2. work on python client 
