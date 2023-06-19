
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from . import auths, users, profile, conversations
from .errors import ValidationException

# TODO 環境変数で設定できるようにする
origins = [
    "http://localhost:3000",
]
app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["*"], allow_headers=["*"])


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


app.include_router(users.router)
app.include_router(auths.router)
app.include_router(profile.router)
app.include_router(conversations.router)
