from collections import namedtuple, defaultdict
from apis_extract import keep_only_nums
from parser import cics_courses, getCourseNums, getTitle, getCredits, getProfRating, getInstructors, all_topics, \
    tokenize

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

    def prereqsSatisfied(self, course: str, taken: dict):  # Todo
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

    def splitCourses(self, path, taken):
        if not path:
            return []

        viable_courses = list(filter(lambda d: len(path[d]) == 0, path))[:3]
        for c in viable_courses:
            del path[c]

        for other_courses in path:
            for to_rem in viable_courses:
                if to_rem in path[other_courses]:
                    path[other_courses].pop(path[other_courses].index(to_rem))

        return [viable_courses] + self.splitCourses(path, taken)

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
        numElectives = lambda d, lvl: len([key for key in d if
                                           keep_only_nums(key) >= keep_only_nums(lvl) and keep_only_nums(key) not in [
                                               "311", "305"]])

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
            if "248" in path[key]:
                path[key].remove("248")

        ret_dict = {key: val for key, val in path.items() if key not in taken and key != "186" and key != "248"}
        return ret_dict

    def generatePlan(self, interests: list, taken: list):
        return self.addFillers(self.addInterests(interests), taken)


def flatten(l):
    return [item for sublist in l for item in sublist]


def return_good(good_topics, taken):
    courses = getCourseNums(cics_courses)
    courseGraph = cGraph(courses)
    good_courses = flatten([all_topics[t] for t in good_topics])
    parsed_good = list(set(list(filter(lambda d: d[1] != "9" and d[0] != "1", (list(map(tokenize, good_courses)))))))[
                  :3]
    taken = list(map(tokenize, taken))
    list_courses_req = courseGraph.generatePlan(parsed_good, taken)
    list_course_plan = courseGraph.splitCourses(list_courses_req, taken)
    return list_course_plan
