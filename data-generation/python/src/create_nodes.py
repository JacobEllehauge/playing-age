from faker import Faker
from typing import Dict, List, Optional
import psycopg2


def create_person(n=1)->List:
    fake = Faker()
    return [fake.name() for i in range(0,n)]


def make_node(nodetype, properties: Optional[Dict])->None:

    with psycopg2.connect("host=localhost port=5499  password='LOL' dbname=graphs user=postgres") as conn:
        with conn.cursor() as curs:
            for name in create_person(n=100):
                q = f"""
                SET search_path = ag_catalog;
                SELECT *
                FROM cypher('starting_here', $$
                    CREATE (a:Person {{name: "{name}", title: 'Developer'}})
                    RETURN a
                $$) as (a agtype);
                """
                curs.execute(q)


if __name__=="__main__":
    print(f'hey there {create_person()[0]} ')
    make_node(nodetype='Person', properties=None)
