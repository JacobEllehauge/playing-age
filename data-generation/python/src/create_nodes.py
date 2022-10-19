from faker import Faker
from typing import Dict, List, Optional
import psycopg2
from tqdm import tqdm
from  utils.decorators import timer


def create_person(n=1)->List:
    fake = Faker()
    return [{"Name": fake.name(), "Adresse": fake.address()} for i in range(0,n)]

def replace_key(object: Dict, old_key: str, new_key: str)->Dict:
    object[new_key] = object.pop(old_key)
    return object

def delete_key(object: Dict, key)->Dict:
    return

def create_node_query(node_name: str, source_object: Dict)->str:
    properties = list(source_object.keys())
    string = f"""
    SET search_path = ag_catalog;
    SELECT *
    FROM cypher('starting_here', $$
        CREATE (a:{node_name} {source_object})
        RETURN a
    $$) as (a agtype);
    """
    # format keys to cypher dict without quotes in loop:
    for key in properties:
        string = string.replace(f"'{key}'", f"{key}")

    return string

def create_relation(start_node: str, end_node: str, start_node_property_value, end_node_property_value, relation_name):
    return f"""
        SELECT *
        FROM cypher('starting_here', $$
            MATCH (a:{start_node}), (b:{end_node})
            WHERE a.Name = "{start_node_property_value}" AND b.Name = "{end_node_property_value}"
            CREATE (a)-[e:{relation_name}]->(b)
            RETURN e
        $$) as (e agtype);
    """

@timer
def make_node_from_person(
        postgres_connection,
        no_nodes: int,
    )->None:

    with postgres_connection as conn:
        with conn.cursor() as curs:
            for person_object in tqdm(create_person(n=no_nodes)):

                # Person
                query_person = create_node_query(node_name="Person", source_object=person_object)

                # Adresse
                adresse_part = replace_key(object=person_object, old_key="Adresse", new_key="Name")
                query_adresse = create_node_query(node_name="Adresse", source_object=adresse_part)

                # relationship (note: 1000 nodes (no batching, no optimization) without relations -> 0.5 sec, with -> 33 sec)
                query_person_adresse = create_relation(
                    start_node="Person",
                    end_node="Adresse",
                    start_node_property_value=person_object.get("Name"),
                    end_node_property_value=adresse_part.get("Name"),
                    relation_name="HAR_ADRESSE"
                    )

                # execute
                curs.execute(query_person)
                curs.execute(query_adresse)
                curs.execute(query_person_adresse)


if __name__=="__main__":
    no_nodes = 1000
    you = create_person()[0]
    print(f'hey there {you.get("Name")} from {you.get("Adresse")} ')
    make_node_from_person(
        postgres_connection = psycopg2.connect("host=localhost port=5499  password='LOL' dbname=graphs user=postgres"),
        nodetype='Person',
        no_nodes=no_nodes,
        properties=None)
    print(f"Created { no_nodes} nodes!! GZ")
