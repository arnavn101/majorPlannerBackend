import pprint
from apis_extract import keep_only_nums
from parser import main, cics_courses, all_topics

pprint.pprint(all_topics)
courses = main(cics_courses)
# {
#   "100C": {
#     "121": [], 
#     "187": ["121"]
#   },
#   "200C": {
#     "220": ["187"],
#     "240": ["132", "187"],
#     "230": ["187"],
#     "250": ["132", "187"]
#   },
#   "300C": {
#     "311": ["187", "250"],
#     "305": ["220", "230", "240", "250"]
#   },
#   "300E": {
#     "383": ["220", "240"],
#     "345": ["187"],
#     "389": ["220", "240"],
#     "360": ["230"],
#     "377": ["230"]
#   },
#   "400E": {
#     "420": ["187", "220"],
#     "446": ["220", "240"],
#     "453": ["230", "377"],
#     "489": ["383"]
#   }
# }

{
  'COMPSCI 250': {
    'prereqs': ['COMPSCI 187', 'MATH 132'], 
    'professors': ['Ghazaleh Parvini'], 
    'description': "Basic concepts of discrete mathematics useful to computer science:  set theory, strings and formal \
                    languages, propositional and predicate calculus, relations and functions, basic number theory. \
                    Induction and recursion: interplay of inductive definition, inductive proof, and recursive algorithms. \
                    Graphs, trees, and search. Finite-state machines, regular languages, nondeterministic finite automata, \
                    Kleene's Theorem.", \
    'credits': 4.0
  }
}

# Get next best course whose prereqs are satisfied
def getCourse(courses, reqs, lvl):

  def eligible(course):
    taken = set()
    for x in reqs.values():
      taken.update(x)
    return all([req in taken for req in courses[lvl][course]])

  for c in courses[lvl].keys():
    if c not in reqs[lvl] and eligible(c):
      return c


def findPath(courses: dict, taken: list, topics: dict, interests: list):
  # Pre-populate schedule with taken/core courses
  majorReqs = {
    "100C": set(["121", "187"]),
    "200C": set(["220", "230", "240", "250"]),
    "300C": set(["305", "311", "320"]),
    "300E": set(),
    "400E": set(),
  }

  path = []

  def dfs(course):
    if course in path:
      return
    path.append(course)

    lvl = ""
    if int(keep_only_nums(course)) >= 400:
      lvl = "400E"
    elif keep_only_nums(course) in {"311", "305", "320", "326"}:
      lvl = "300C"
    elif int(keep_only_nums(course)) >= 300:
      lvl = "300E"
    
    majorReqs[lvl].add(course)
    for c in courses[lvl][course]:
      dfs(c)

  # Add courses based on interest
  for i in interests:
    dfs(i)

  # Add remaining 300+ Electives
  while len(majorReqs["300E"]) < 4:
    next = getCourse(courses, majorReqs, "300E")
    majorReqs["300E"].add(next)
  
  # Add remaining 400+ Electives
  while len(majorReqs["400E"]) < 3:
    next = getCourse(courses, majorReqs, "400E")
    majorReqs["400E"].add(next)

  return majorReqs

# pprint.pprint(findPath(courses))
    

  
