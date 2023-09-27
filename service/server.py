import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.routers import api

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = FastAPI()
app.include_router(api.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
def healthcheck():
    return {"Running": "Fast"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
