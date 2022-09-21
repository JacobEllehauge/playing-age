from faker import Faker
from typing import Dict, List, Optional
import psycopg2


def create_person(n=1)->List:
    fake = Faker()
    return [[fake.name(), fake.address()] for i in range(0,n)]

def make_node(nodetype, properties: Optional[Dict])->None:

    with psycopg2.connect("host=localhost port=5499  password='LOL' dbname=graphs user=postgres") as conn:
        with conn.cursor() as curs:
            for _list in create_person(n=100):
                q = f"""
                SET search_path = ag_catalog;
                SELECT *
                FROM cypher('starting_here', $$
                    CREATE (a:Person {{name: "{_list[0]}", adresse: "{_list[1]}"}})
                    RETURN a
                $$) as (a agtype);

                SELECT *
                FROM cypher('starting_here', $$
                    CREATE (a:Adresse {{name: "{_list[1]}"}})
                    RETURN a
                $$) as (a agtype);

                SELECT *
                FROM cypher('starting_here', $$
                    MATCH (a:Person), (b:Adresse)
                    WHERE a.name = "{_list[0]}" AND b.name = "{_list[1]}"
                    CREATE (a)-[e:HAS_ADRESSE]->(b)
                    RETURN e
                $$) as (e agtype);

                """
                curs.execute(q)






if __name__=="__main__":
    print(f'hey there {create_person()[0][0]} from {create_person()[0][1]} ')
    make_node(nodetype='Person', properties=None)
