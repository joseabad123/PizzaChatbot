from SPARQLWrapper import SPARQLWrapper, JSON

# URL de archivo OWL
sparql = SPARQLWrapper('http://localhost:3030/loxapizzaV1/sparql')


def get_response_pizzas():
    # Consulta para sacar las pizzas
    sparql.setQuery('''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX saidi: <http://www.semanticweb.org/jmat/ontologies/2020/6/PizzaTutorial#>
        SELECT DISTINCT ?name 
        WHERE { 
            ?s rdfs:subClassOf saidi:NamedPizza .
            ?s rdfs:label ?name
            FILTER (lang(?name) = 'es')
        }
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres

def get_response_ingredients():
    # Consulta de ingredientes
    sparql.setQuery('''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX pizza: <http://www.semanticweb.org/jmat/ontologies/2020/6/PizzaTutorial#>
        SELECT DISTINCT ?name 
                WHERE { 
                    ?s rdfs:subClassOf pizza:Named_pizza .
                    ?s rdfs:label ?name
                    FILTER (lang(?name) = 'es')
        }
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres

if __name__ == '__main__':
    get_response_pizzas()
