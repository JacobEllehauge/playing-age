from faker import Faker
from typing import Dict, List, Optional
import psycopg2
from tqdm import tqdm
from time import time


def create_person(n=1)->List:
    fake = Faker()
    return [[fake.name(), fake.address()] for i in range(0,n)]

def timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.2f}seconds')
        return result
    return wrap_func

@timer
def make_node(postgres_connection, nodetype: str, no_nodes: int, properties: Optional[Dict])->None:
    with postgres_connection as conn:
        with conn.cursor() as curs:
            for _list in tqdm(create_person(n=no_nodes)):
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
    no_nodes = 100

    print(f'hey there {create_person()[0][0]} from {create_person()[0][1]} ')
    make_node(
        postgres_connection = psycopg2.connect("host=localhost port=5499  password='LOL' dbname=graphs user=postgres"),
        nodetype='Person',
        no_nodes=no_nodes,
        properties=None)
    print(f"Created { no_nodes} nodes!! GZ")
