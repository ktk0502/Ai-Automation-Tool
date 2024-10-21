from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class PipelineData(BaseModel):
    nodes: List[Dict]  
    edges: List[Dict] 

def is_dag(edges):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for edge in edges:
        src = edge['source']  
        dest = edge['target'] 
        graph[src].append(dest)
        in_degree[dest] += 1
        in_degree[src] 
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count == len(in_degree)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(data: PipelineData):
    num_nodes = len(data.nodes)
    num_edges = len(data.edges)
    is_dag_result = is_dag(data.edges)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag_result
    }
