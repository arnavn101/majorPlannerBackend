courses = {
  "121": [], 
  "187": ["121"], 
  "220": ["187"],
  "240": ["132", "187"],
  "230": ["187"],
  "250": ["132", "187"],
  "383": ["220", "240"],
  "311": ["187", "250"]
}

coreCourses = {"121", "187", "220", "240",
               "230", "250", "311", "305", "320/326"}

electives = {"325", "345", "373", "377", "383", "389", "390R", "420", "445", "446", "453", "466", "490U", "491G",
             "496C", "501", "508", "514", "520", "532", "535", "546", "550", "561", "571", "574", "589", "590J", "590K", "591NR"}

def findPath(courses: dict): #, interests: str, required: set):
  interest_classes = ["383", "501"] # getCourses(interests)
  path = []
  cores = coreCourses
  for course in interest_classes:
    currReq = course
    while (currReq not in cores and currReq not in path):
      path.append(currReq)
      currReq = courses[currReq]
  return path

print(findPath(courses))

