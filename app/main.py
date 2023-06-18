
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from . import auths, users, profile

from .errors import ValidationException

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for err in exc.errors():
        keys = err['loc']
        if keys[0] == 'body':
            keys = keys[1:]
        message = err['msg']
        error_key = ".".join(str(key) for key in keys)
        if error_key not in errors:
            errors[error_key] = []
        errors[error_key].append(message)
    response = ValidationException(content=errors)

    return JSONResponse(
        status_code=response.status_code,
        content=jsonable_encoder(response.content),
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


app.include_router(users.router)
app.include_router(auths.router)
app.include_router(profile.router)
