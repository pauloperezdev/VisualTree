from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import subprocess

# Función para obtener la salida del comando tree
def get_tree_output():
    result = subprocess.run(['tree'],capture_output=True, text=True,shell=True)
    return result.stdout

# Función para procesar la salida del comando tree y generar consultas de Cypher
def process_tree_output(output, parent=None):
    queries = []

    for line in output.split('\n'):
        if line.strip():  # Ignorar líneas en blanco
            node_name = line.lstrip()
            query = f'CREATE (:Node {{name: "{node_name}"}})'
            if parent:
                query += f'-[:HAS_PARENT]->(:Node {{name: "{parent}"}})'
            queries.append(query)
    print(queries)
    return queries

# Función para ejecutar las consultas de Cypher en la base de datos Neo4j
def execute_cypher_queries(queries, uri, user, password):
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session() as session:
            for query in queries:
                session.run(query)

# Configuración de la conexión a Neo4j
#neo4j_uri = "neo4j+s://59e70bca.databases.neo4j.io"  # Reemplazar con la URI de tu instancia de Neo4j
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
#URI = "neo4j+s://59e70bca.databases.neo4j.io"
#AUTH = ("neo4j", "mCxGitBz1LoN_e4UD1g5Lntsn5eccEOeFC2Jj7brB30")

# Obtener la salida del comando tree
tree_output = get_tree_output()

# Ejecutar las consultas de Cypher en Neo4j
# execute_cypher_queries(cypher_queries, neo4j_uri, neo4j_user, neo4j_password)

uri = "neo4j+s://59e70bca.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "mCxGitBz1LoN_e4UD1g5Lntsn5eccEOeFC2Jj7brB30"), encrypted=True)

try:
    with driver.session() as session:
        session.run("MATCH (n) RETURN count(n)")
except ServiceUnavailable as e:
    print(f"Unable to connect to database: {e}")
finally:
    driver.close()

# Procesar la salida del comando tree y generar consultas de Cypher
cypher_queries = process_tree_output(tree_output)