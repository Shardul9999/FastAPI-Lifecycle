from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
import time

app = FastAPI()

#Middleware(1st logging)

@app.middleware("http")
async def middleware_logging(request: Request, call_next):
    print("Logging Middleware Started")

    start = time.time()
    try:
        response = await call_next(request)

    except Exception as e:
        print(f"MiddleWare caught an error", {e})
        raise e
    
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
        raise HTTPException(
            status = 401,
            detail="Unauthorized"
        )
    
    response = await call_next(request)
    print("Auth Middleware End")
    return response

#Global Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code = exc.status_code,
        content={
            "error":{
                "message" : exc.detail,
                "status_code" : exc.status_code
            }
        }
    )
    

#Generic Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unexpected Error : {exc}")

    return JSONResponse(
        status_code = 500,
        content = {
            "error":{
                "message" : "Internal Server Error",
                "status_code": 500
            }
        }
    )

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