import requests
import time
from tqdm import tqdm
import pickle
from bs4 import BeautifulSoup


BASE_URL = "https://spire-api.melanson.dev/subjects/COMPSCI"
INTERESTS_URL = "https://cics-consultant.herokuapp.com/html/fields.html"


def keep_only_nums(s):
    return ''.join(c for c in s if c.isdigit())


def fetch_courses():
    courses_info = dict()
    all_courses = requests.get(BASE_URL).json()["courses"]

    for course in tqdm(all_courses):
        course_num = keep_only_nums(course["id"].split()[1])
        if int(course_num) >= 500:
            continue

        while True:
            course_info = requests.get(course["url"]).json()
            if "enrollment_information" in course_info:
                break
            time.sleep(60)

        enroll_info = course_info["enrollment_information"]

        prereq_info = "" if not enroll_info else enroll_info["enrollment_requirement"]
        pre_reqs = list()

        split_prereqs = prereq_info.split() if prereq_info else []
        for i, word in enumerate(split_prereqs):
            word = keep_only_nums(word) if ")" not in word else ""
            if word.isdigit() and 99 < int(word) <= 999:
                pre_reqs.append(f"{split_prereqs[i-1]} {word}")

        list_professors = list()
        all_offerings = course_info["offerings"]
        if len(all_offerings) > 0:
            first_offering_url = all_offerings[0]["url"]
            all_sections = requests.get(first_offering_url).json()["sections"]
            if(len(all_sections)) > 0:
                first_section_url = all_sections[0]["url"]
                sections_info = requests.get(first_section_url).json()
                list_professors = [d["name"] for d in sections_info["meeting_information"][0]["instructors"]
                                   if sections_info["meeting_information"]]

        courses_info[course["id"]] = {"prereqs": pre_reqs, "professors": list_professors,
                                      "description": course_info["description"],
                                      "credits": course_info["details"]["units"]["base"]
                                      if course_info["details"] else 0,
                                      "title": course_info["title"]}
        time.sleep(1)

    return courses_info


def write_to_file(courses_info):
    with open('spireInfo.pickle', 'wb') as handle:
        pickle.dump(courses_info, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_from_file():
    with open('spireInfo.pickle', 'rb') as handle:
        d = pickle.load(handle)
    return d


def fetch_topics():
    resp = requests.get(INTERESTS_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    return list(map(lambda d: d.text, soup.findAll("h5")))


def topics_to_courses(courses, topics):
    topics_mappings = dict()
    for t in topics:
        list_classes = [c for c in courses if all([courses[c]["description"] and w.lower() in courses[c]["description"]
                                                   for w in t.split()])]
        topics_mappings[t] = list_classes
    return topics_mappings


# write_to_file(fetch_courses())
# all_info = read_from_file()
# all_topics = topics_to_courses(all_info, fetch_topics())
