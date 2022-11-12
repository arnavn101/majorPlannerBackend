from typing import List, Union
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel


class UserProfile(BaseModel):
    email: str
    major: str
    graduation: str
    interests: List[str]
    courses: List[str]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/log")
async def log(profile: UserProfile):
    print(profile)
    return {"message": "Hello World"}
