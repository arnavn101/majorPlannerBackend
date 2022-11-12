from collections import namedtuple
import pprint  
from apis_extract import keep_only_nums
from parser import cics_courses, getCourseNums, getTitle, getCredits, getProfRating, getInstructors

courses = getCourseNums(cics_courses)
# pprint.pprint(courses)

class cNode:

  def __init__(self, number, prof, name, rating=0, credits=4):
    self.name = name
    self.number = number
    self.prof = prof
    self.rating = rating
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

  def getNode(self, course: str):
    name = getTitle(course)
    credits = getCredits(course)
    profs = getInstructors(course)
    maxRating, bestProf = 0, ""
    for p in profs:
      if (best := float(getProfRating(p[0]))) >= maxRating:
        bestProf = p[0]
        maxRating = best
    return cNode(course, bestProf, name, maxRating, credits)
  
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

  def splitCourses(self, path: dict, taken: list):
    coursePlan = []
    keys = sorted(list(path.keys()))
    for course in taken:
      for num in keys:
          if course in path[num]:
            path[num].remove(course)

    maxCourses = 2
    layer = []
    while any([len(path[x]) > 0 for x in path]):
      eligible = sorted([key for key in path if len(path[key]) == 0 and key not in taken])
      if ("220" in taken and "240" in taken) or ("230" in taken and "250" in taken):
        maxCourses = 3
      for course in eligible:
        if len(layer) < maxCourses:
          layer.append(course)
          taken.append(course)
          for num in path:
            if course in path[num]:
              path[num].remove(course)
        else:
          coursePlan.append(layer)
          layer = []
    for num in path:
      if num >= "400" and num not in layer:
        if len(layer) < 3:
          layer.append(num)
        else:
          coursePlan.append(layer)
          layer = []
    
    if len(layer) > 0:
      coursePlan.append(layer)
    return coursePlan

  def addFillers(self, interestPath: dict, taken: list):

    def getBest(lvl):
      maxRating, bestCourse = float("-inf"), ""
      for c in self.graph[lvl]:
        node = self.getNode(c)
        if self.prereqsSatisfied(c, path) and c not in path and node.rating >= maxRating:
          maxRating = node.rating
          bestCourse = c
      return bestCourse
      
    path = interestPath
    numElectives = lambda d, lvl: len([key for key in d if keep_only_nums(key) >= keep_only_nums(lvl) and keep_only_nums(key) not in ["311", "305"]])
    
    for c in self.graph["100C"]:
      if c != "186":
        path[c] = self.graph["100C"][c]

    for c in self.graph["200C"]:
      path[c] = self.graph["200C"][c]
    
    for c in self.graph["300C"]:
      path[c] = self.graph["300C"][c]
    
    while numElectives(path, "300E") < 4:
      next = getBest("300E")
      path[next] = self.graph["300E"][next]

    while numElectives(path, "400E") < 3:
      next = getBest("400E")
      path[next] = self.graph["400E"][next]

    for key in path.keys():
      if "186" in path[key]:
        path[key].remove("186")
    
    return {key: val for key, val in path.items() if key not in taken and key != "186"}

  def generatePlan(self, interests: list, taken: list):
    return self.addFillers(self.addInterests(interests), taken)

taken = ["121", "187"]

courseGraph = cGraph(courses)
# pprint.pprint(courseGraph.generatePlan(["377", "383", "453", "420", "446"], taken))
pprint.pprint(courseGraph.splitCourses(courseGraph.generatePlan([], taken), taken))
