from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from course_graph import return_good
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


class UserProfile(BaseModel):
    email: str
    major: str
    graduation: str
    interests: List[str]
    courses: List[str]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/graph")
async def get_major_graph(profile: UserProfile):
    list_courses = return_good(profile.interests, profile.courses)
    return list_courses
