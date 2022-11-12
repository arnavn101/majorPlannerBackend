from collections import namedtuple
import pprint  
from apis_extract import keep_only_nums

class cNode:

  def __init__(self, number, name="name", difficulty="Medium"):
    self.name = name #Todo
    self.number = number
    self.difficulty = difficulty

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
          self.edges.add(cEdge(cNode(co), cNode(p)))
  
  def isCourse(self, course: str):
    for courses in self.graph.values():
      if course in courses:
        return True
    return False
  
  def getPrereqs(self, course: str):
    if self.isCourse(course):
      for courses in self.graph.values():
        if course in courses:
          return courses[course]
      return []

  def prereqsSatisfied(self, course: str, taken: list): #Todo
    required = self.getPrereqs(course)
    satisfied = [e for e in self.edges if e.edge.course.number == course and e.edge.preReq.number in taken]
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

  def addFillers(self, interestPath: dict, majorReqs: dict):

    # def getNext(lvl):
      
    path = interestPath
    numElectives = lambda d, f: len([key for key in d if f(key)])
    num300 = numElectives(path, lambda k: keep_only_nums(k) >= "311" and keep_only_nums(k) not in ["311", "305"])
    num400 = numElectives(path, lambda k: keep_only_nums(k) >= "400")

    while num300 < 4 and num400 < 3:
      if num300 < 4:
        pass

  def generatePlan(self, interests: list, majorReqs: dict):
    return self.addFillers(self.addInterests(interests), majorReqs)
    

majorReqs = {
  "100C": ["121", "187"],
  "200C": ["220", "230", "240", "250"],
  "300C": ["305", "311"],
  "300E": [],
  "400E": []
}
    
courses = {
  "100C": {
    "121": [],
    "187": ["121"]
  },
  "200C": {
    "220": ["121", "187"],
    "230": ["121", "187"],
    "240": ["187"],
    "250": ["187"]
  },
  "300C": {
    "305": ["220", "230", "240", "250"],
    "311": ["187", "250"]
  },
  "300E": {
    "345": ["187"],
    "377": ["230"],
    "383": ["220", "240"],
    "320": ["220"],
    "326": ["220", "230"]
  },
  "400E": {
    "420": ["320", "220"],
    "446": ["220", "240"],
    "453": ["230", "377"],
    "445": ["345"],
    "403": ["230", "187"]
  }
}

taken = ["187", "220", "230", "240"]

courseGraph = cGraph(courses)
# pprint.pprint(courseGraph.addInterests(["377"]))
