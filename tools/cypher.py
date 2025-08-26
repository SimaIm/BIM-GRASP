import streamlit as st
from llm import llm
from graph import graph

from langchain_neo4j import GraphCypherQAChain

from langchain.prompts.prompt import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about IFC data.
The IFC data is a building consisting of Elements. These elements are walls.


Convert the user's question based on the schema into a cypher query. 
Use the words in the user query to form the cypher. For example, if user asks: "what is the Structural Material of the wall?",
you use Structural Material in the cypher query by adding ` ` around it to form a cypher.


Example of cypher statements:

1. To find the structural material of a wall:
```
MATCH (w:Wall {id: "name of the wall"})
RETURN w.`Structural Material`
```
2. To find the Thermal resistance of the wall:
```
MATCH (w:Wall {id: "name of the wall"})
RETURN w.`Thermal resistance`
```
3. To find the thermal coefficient of the wall:
```
MATCH (w:Wall {id: "name of the wall"})
RETURN w.name, w.`Heat Transfer Coefficient`
```
4. To find if the wall connected to another wall:
```
MATCH (w:Wall)-[r:CONNECTED_TO]-(other:Wall)
WHERE w.name = 'name'
  AND other.type IN ["IfcWall", "IfcWallStandardCase", "IfcCurtainWall"]
RETURN
  w.name AS Source_Wall,
  type(r) AS Relationship,
  r.type AS ConnectionType,
  other.name AS Connected_Wall,
  other.id AS Connected_Wall_ID,
  other.type AS Connected_Wall_Type
```

Schema:
{schema}

Question:
{question}

Cypher Query:
"""



cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)