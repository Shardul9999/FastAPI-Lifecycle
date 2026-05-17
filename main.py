from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

#Middleware(1st logging)

@app.middleware("http")
async def middleware_logging(request: Request, call_next):
    print("Logging Middleware Started")

    start = time.time()
    response = await call_next(request)
    end = time.time()
    duration = end - start

    print(f"Logging Middleware End {duration : 4f}s")
    return response

#Middleware(2nd Authentication)
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    print("Auth Middleware Start")

    token = request.headers.get("Authorization")
    if token != "secret-token":
        print("Unauthorized")

        return JSONResponse(
            status_code = 401,
            content={"error" : "Unauthorized"}
        )
    
    response = await call_next(request)
    print("Auth Middleware End")
    return response
    
#Dependency
async def get_db():
    print("Dependency : Connect DB")
    db = {"connection" : "fake-db"}
    yield db
    print("Dependency: Close DB")

#Route
@app.get("/users")
async def get_users(db = Depends(get_db)):
    print("Router is Running")

    return{
        "users" : ["Shardul", "Frank"],
        "db" : db
    }