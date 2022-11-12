from collections import namedtuple
import pprint  
from apis_extract import keep_only_nums
from parser import cics_courses, getCourseNums

courses = getCourseNums(cics_courses)
# pprint.pprint(courses)

class cNode:

  def __init__(self, number, name="name", difficulty="Medium", credits=4):
    self.name = name #Todo
    self.number = number
    self.difficulty = difficulty
    self.credits = credits

class cEdge:

  def __init__(self, course, preReq, AND=False):
    newEdge = namedtuple('newEdge', ['course', 'preReq', 'AND'])
    self.edge = newEdge(course, preReq, AND)
  
class cGraph:
  
  def __init__(self, gDict: dict = None):
    self.graph = dict() if gDict is None else gDict
    self.edges = set()

    for lvl in gDict.values():
      for co, pre in lvl.items():
        for p in pre:
          self.edges.add(cEdge(co, p))
  
  def isCourse(self, course: str):
    for courses in self.graph.values():
      if course in courses:
        return True
    return False

  # def getNode(self, course, prereqs):
  
  def getPrereqs(self, course: str):
    if self.isCourse(course):
      for courses in self.graph.values():
        if course in courses:
          return courses[course]
    return []

  def prereqsSatisfied(self, course: str, taken: dict): #Todo
    required = self.getPrereqs(course)
    satisfied = [e for e in self.edges if e.edge.course == course and e.edge.preReq in taken]
    return len(satisfied) == len(required)
  
  def addInterests(self, interests: list):
    path = dict()

    def addPrereqs(c):
      for x in self.getPrereqs(c):
        if x not in path:
          path[x] = self.getPrereqs(x)
          addPrereqs(x)

    for course in interests:
      if course not in path:
        path[course] = self.getPrereqs(course)
        addPrereqs(course)
    return path

  def addFillers(self, interestPath: dict, taken: list):

    def getNext(lvl):
      for c in courses[lvl]:
        if self.prereqsSatisfied(c, path) and c not in path:
          return c
      return None
      
    path = interestPath
    numElectives = lambda d, lvl: len([key for key in d if keep_only_nums(key) >= keep_only_nums(lvl) and keep_only_nums(key) not in ["311", "305"]])
    
    for c in courses["200C"]:
      path[c] = courses["200C"][c]
    
    for c in courses["300C"]:
      path[c] = courses["300C"][c]
    
    while numElectives(path, "300E") <= 4:
      next = getNext("300E")
      path[next] = courses["300E"][next]

    while numElectives(path, "400E") <= 3:
      next = getNext("400E")
      path[next] = courses["400E"][next]

    return {key: val for key, val in path.items() if key not in taken}

  def generatePlan(self, interests: list, taken: list):
    return self.addFillers(self.addInterests(interests), taken)
    

# courses = {
#   "100C": {
#     "121": [],
#     "187": ["121"]
#   },
#   "200C": {
#     "220": ["121", "187"],
#     "230": ["121", "187"],
#     "240": ["187"],
#     "250": ["187"]
#   },
#   "300C": {
#     "305": ["220", "230", "240", "250"],
#     "311": ["187", "250"]
#   },
#   "300E": {
#     "345": ["187"],
#     "377": ["230"],
#     "383": ["220", "240"],
#     "320": ["220"],
#     "326": ["220", "230"],
#   },
#   "400E": {
#     "420": ["320", "220"],
#     "446": ["220", "240"],
#     "453": ["230", "377"],
#     "445": ["345"],
#     "403": ["230", "187"]
#   }
# }

taken = ["121", "187", "220", "230"]

courseGraph = cGraph(courses)
pprint.pprint(courseGraph.generatePlan(["377", "383"], taken))
