from apis_extract import read_from_file, topics_to_courses, fetch_topics, keep_only_nums
from rate_my_prof import RateMyProfScraper

# tryCourses = {'COMPSCI 250': {'prereqs': ['COMPSCI 187', 'MATH 132'], 'professors': ['Ghazaleh Parvini'], 'description': "Basic concepts of discrete mathematics useful to computer science:  set theory, strings and formal languages, propositional and predicate calculus, relations and functions, basic number theory.  Induction and recursion:  interplay of inductive definition, inductive proof, and recursive algorithms.  Graphs, trees, and search.   Finite-state machines, regular languages, nondeterministic finite automata, Kleene's Theorem.", 'credits': 4.0},
#               'COMPSCI 220': {'prereqs': ['COMPSCI 187'], 'professors': ['Jaime Davila', 'Marius Minea'], 'description': 'Development of individual skills necessary for designing, implementing, testing and modifying larger programs, including: design strategies and patterns, using functional and object-oriented approaches, testing and program verification, code refactoring, interfacing with libraries.', 'credits': 4.0, 'title': 'Programming Methodology'}
#               }

umass_uni = RateMyProfScraper(1513)
umass_uni.read_dict()
profs = umass_uni.dict_professors

cics_courses = read_from_file("spireInfo.pickle")
all_topics = topics_to_courses(cics_courses, fetch_topics())

def tokenize(str):
    courseNum = str.split(" ")[1]
    return courseNum

def getAttribute(courseNumber, courses, attribute):
    result = {}
    for courseNeeded in courses.keys():
        curr = tokenize(courseNeeded)
        if curr == courseNumber:
            return courses[courseNeeded][attribute]
    return "Invalid"

def getTitle(courseNumber):
    return getAttribute(courseNumber, cics_courses, 'title')

def getCredits(courseNumber):
    return getAttribute(courseNumber, cics_courses, 'credits')

def get_prof_rmp():
    proffesors = {}
    for proff in profs.keys():
        proffesors[proff.split(" ")[0] + " " + proff.split(" ")[-1]] = {"rating": profs[proff]["overall_rating"], "numRatings": profs[proff]["tNumRatings"]}
    return proffesors

# print(getTitle("220") + " credits:" + str(getCredits("220")))



def getCourseNums(courses):
    result = {"100C": {
        "121": [],
        "186": ["121"],
        "187": ["121"],
        "198C": [],
    }, "200C": {
        "220": ["187"],
        "230": ["187", "198C"],
        "240": ["187"],
        "250": ["187"],
    }, "300C": {
        "311": ["187", "250"],
        "305": ["220", "230", "240", "250"]
    },
        "300E": {}, "400E": {}}
    i = 0
    for courseObj in courses:
        mainCourse = list(courses.keys())[i]
        curr = tokenize(mainCourse)
        if curr != "311" and curr != "305" and curr[0] != "1" and curr[0] != "2" and curr[0] != "H":
            lvl = findlvl(curr)
            result[lvl][curr] = []
            preReqArr = courses[mainCourse]['prereqs']
            for elem in preReqArr:
                result[lvl][curr].append(tokenize(elem))
        i += 1
    return result


def findlvl(courseNum):
    lvlHere = keep_only_nums(courseNum)[0]
    lvl = ""
    if lvlHere == "1":
        lvl = "100C"
    elif lvlHere == "2":
        lvl = "200C"
    elif lvlHere == "3":
        lvl = "300E"
    elif lvlHere == "4":
        lvl = "400E"
    else:
        return "Not Valid"
    return lvl

# print(getCourseNums(cics_courses))