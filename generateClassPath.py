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


def findPath(courses: dict): #, interests: list):
  # Pre-populate schedule with taken/core courses
  majorReqs = {
    "100C": set(["121", "187"]),
    "200C": set(["220", "230", "240", "250"]),
    "300C": set(["305", "311", "320"]),
    "300E": set(),
    "400E": set(),
  }

  interests = ["383", "311"]
  path = [] + list(majorReqs["100C"]) + list(majorReqs["200C"])

  def dfs(course):
    if course in path:
      return
    path.append(course)

    lvl = ""
    if int(course) >= 400:
      lvl = "400E"
    elif course in {"311", "305", "320", "326"}:
      lvl = "300C"
    elif int(course) >= 300:
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

pprint.pprint(findPath(courses))
    

  
