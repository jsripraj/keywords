from neo4j import GraphDatabase
import pandas as pd
import neo4j
import config

URI = config.NEO4J_URI
AUTH = config.NEO4J_AUTH

def get_suggestable_keywords() -> list[str]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (k:Keyword)<-[:INTERESTED_IN]-(:Faculty)
                RETURN DISTINCT k.name AS Keyword
                ORDER BY k.name''',
                database_="neo4j",
            )
        except Exception as e:
            print(e)
    return [record.data('Keyword')['Keyword'] for record in records]

def get_suggested_keywords(seed_keyword) -> list[str]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (k:Keyword)<-[i:INTERESTED_IN]-(f:Faculty)-[:INTERESTED_IN]->(:Keyword {name: $chosen_keyword}) 
                WHERE k.hidden IS NULL OR k.hidden = false
                WITH k.name AS Keyword, sum(i.score) AS totalScore
                RETURN Keyword
                ORDER BY totalScore DESC
                LIMIT 10''',
                chosen_keyword=seed_keyword,
                database_="neo4j",
            )
        except Exception as e:
            print(e)
    return [{'Keyword': record.data('Keyword')['Keyword']} for record in records]

def hide_keywords(keywords) -> None:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                UNWIND $keywords_to_hide AS keyword_to_hide
                CALL (keyword_to_hide) {
                    MATCH (k:Keyword {name: keyword_to_hide})
                    SET k.hidden = true
                }''',
                keywords_to_hide=keywords,
                database_="neo4j"
            )
        except Exception as e:
            print(e)

def unhide_all_keywords() -> None:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (k:Keyword {hidden: true})
                SET k.hidden = false''',
                database_="neo4j",
            )
        except Exception as e:
            print(e)

def get_suggested_institutes(seed_keyword) -> list[str]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (:Keyword {name: $seed_keyword})<-[interest:INTERESTED_IN]-(f:Faculty)-[:AFFILIATION_WITH]->(institute:Institute) 
                WHERE institute.hidden IS NULL OR institute.hidden = false
                WITH institute.name AS institute, sum(interest.score) AS totalScore
                RETURN institute
                ORDER BY totalScore DESC
                LIMIT 10''',
                seed_keyword=seed_keyword,
                database_="neo4j",
            )
        except Exception as e:
            print(e)
    return [{'Institute': record.get('institute')} for record in records]

def hide_institutes(institutes) -> None:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                UNWIND $institutes_to_hide AS institute_to_hide
                CALL (institute_to_hide) {
                    MATCH (i:Institute {name: institute_to_hide})
                    SET i.hidden = true
                }''',
                institutes_to_hide=institutes,
                database_="neo4j"
            )
        except Exception as e:
            print(e)

def unhide_all_institutes() -> None:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (i:Institute {hidden: true})
                SET i.hidden = false''',
                database_="neo4j",
            )
        except Exception as e:
            print(e)

def get_shortest_path(faculty_id, target_keyword) -> list[dict]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            graph_result = driver.execute_query('''
                MATCH path = SHORTEST 1 (:Faculty {id: $faculty_id})-[:INTERESTED_IN]-+(:Keyword {name: $target_keyword})
                RETURN path''',
                faculty_id=faculty_id,
                target_keyword=target_keyword,
                result_transformer_=neo4j.Result.graph,
                database_="neo4j",
            )
        except Exception as e:
            print(e)
    cyto_nodes = [
        {
            'data': {'id': node.get('id'), 'label': node.get('name')},
            'classes': 'faculty' if list(node.labels)[0] == 'Faculty' else 'keyword'
        }
        for node in graph_result.nodes
    ]
    cyto_edges = [
        {
            'data': {'source': edge.start_node.get('id'), 'target': edge.end_node.get('id')},
            'classes': 'edge'
        }
        for edge in graph_result.relationships
    ]
    return cyto_nodes + cyto_edges


def get_faculty() -> list[dict]:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query('''
                MATCH (f:Faculty)
                WHERE f.name IS NOT NULL AND btrim(f.name) <> ""
                RETURN f.id AS id, btrim(f.name) AS name
                ORDER BY name''',
                database_="neo4j",
            )
        except Exception as e:
            print(e)
    return [{"label": record.get('name'), "value": record.get('id')} for record in records]
