from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from course_graph import return_good
from fastapi.middleware.cors import CORSMiddleware
from parser import cics_courses, getInstructors, profs
from statistics import mean

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


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def parse_major_graph(initial_courses):
    all_sems = dict()
    parsed_cics_courses = {(k.split()[1]): v for k, v in cics_courses.items()}
    for sem_num, list_courses in enumerate(initial_courses):
        cur_courses = []
        for course in list_courses:
            list_ratings = [float(profs[p]["overall_rating"])
                            for p in getInstructors(course)
                            if p in profs and is_float(profs[p]["overall_rating"])]
            cur_courses.append({"number": course, "title": parsed_cics_courses[course]["title"],
                                "credits": float(parsed_cics_courses[course]["credits"]),
                                "rating": mean(list_ratings) if list_ratings else 0})
        all_sems[f"Semester {sem_num + 1}"] = cur_courses
    return all_sems


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/graph")
async def get_major_graph(profile: UserProfile):
    list_courses = return_good(profile.interests, profile.courses)
    resp = parse_major_graph(list_courses)
    print(resp)
    return resp
