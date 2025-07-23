from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()
@app.get("/hello")
def greet_user(request: Request, is_teacher: bool = None, name: str = "Non defini"):
    if is_teacher is None:
        is_teacher = False
    accept_header = request.headers.get("Accept")
    if(accept_header != "text/plain"):
        return JSONResponse(status_code=400, content={"message": "Accept header should be text/plain"})
    if(is_teacher and name != "Non defini"):
        return JSONResponse(status_code=200 , content={f"Message" : f"Hello teacher {name}"})
    if(is_teacher == False and name != "Non defini"):
        return JSONResponse(status_code=400 , content={"message": f"Hello {name}"})
    return JSONResponse(status_code=400 , content={"message": f"Hello nig"})


class greetingRequest(BaseModel):
    name: str
@app.post("/greet-user")
def greet_user(request : greetingRequest):
    return JSONResponse(content={f"message" : f"Hellooooo {request.name} how are you!"}, status_code=200)

class SecretCode(BaseModel):
    secret_key: int

@app.put("/top-secret")
def secret_key_handler(request: Request, secret_keys: SecretCode):
    secret_key_header = request.headers.get("Authorization")
    if secret_key_header != "my-secret_key":
        return JSONResponse(status_code=403, content={"message" : f"You do not have the right to do this shi"})
    secret_key_provided = secret_keys.secret_key
    if len(str(secret_key_provided)) != 4:
        return JSONResponse(status_code=403, content={"message" : f"The secret key is 4 characters, yours is {len(str(secret_key_provided))}"})
    return JSONResponse(status_code=200, content={"message" : f"You are right the secret key is {secret_key_provided}"})