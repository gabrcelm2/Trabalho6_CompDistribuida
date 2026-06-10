import uvicorn
import threading
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from strawberry.fastapi import GraphQLRouter

from database import init_db
from rest_api import rest_router
from graphql_api import schema
from soap_api import soap_wsgi_app
from grpc_api import serve_grpc

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    import anyio
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000

# 1. REST
app.include_router(rest_router, prefix="/api")

# 2. GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# 3. SOAP
app.mount("/ws", WSGIMiddleware(soap_wsgi_app))

if __name__ == "__main__":
    print("Inicializando banco de dados...")
    init_db()
    
    # Inicia gRPC em background
    print("Iniciando gRPC...")
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    
    # Inicia Uvicorn (FastAPI) para REST, GraphQL e SOAP
    print("Iniciando Uvicorn para REST (8000), GraphQL (8000) e SOAP (8000)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
