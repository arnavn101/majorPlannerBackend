from apis_extract import keep_only_nums

# pprint.pprint(all_topics)
# courses = getCourseNums(cics_courses)
# pprint.pprint(courses)


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


def findPath(courses: dict):  # , taken: list, topics: dict, interests: set):
    # Pre-populate schedule with taken/core courses
    majorReqs = {
        "100C": {"121", "187"},
        "200C": {"220", "230", "240", "250"},
        "300C": {"305", "311", "320"},
        "300E": set(),
        "400E": set(),
    }

    path = []
    interests = ["383", "420", "377"]

    # impCourses = []
    # for i in interests:
    #   impCourses.extend(all_topics[i])

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
        elif int(keep_only_nums(course)) >= 200:
            lvl = "200C"
        else:
            lvl = "100C"

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
