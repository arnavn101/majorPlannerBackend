import requests
import json
import math
from apis_extract import write_to_file, read_from_file


class RateMyProfScraper:
    def __init__(self, school_id):
        self.university_id = school_id
        self.dict_professors = dict()

    def get_all_professors(self):
        num_of_prof = self.get_num_professors(self.university_id)
        num_of_pages = math.ceil(num_of_prof / 20)

        i = 1
        while i <= num_of_pages:
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                self.university_id))
            json_page = json.loads(page.content)
            temp_list = json_page['professors']
            for prof in temp_list:
                pname = prof["tFname"] + " " + prof["tLname"]
                self.dict_professors[pname] = prof
            i += 1

        return {}

    def get_num_professors(self, uni_id):
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A"
            "*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                uni_id))
        temp_json_page = json.loads(page.content)
        num_of_prof = temp_json_page[
                          'remaining'] + 20
        return num_of_prof

    def write_dict(self):
        write_to_file("rmfInfo.pickle", self.dict_professors)

    def read_dict(self):
        self.dict_professors = read_from_file("rmfInfo.pickle")


# umass_uni = RateMyProfScraper(1513)
# umass_uni.get_all_professors()
# umass_uni.write_dict()
# umass_uni.read_dict()
# print(umass_uni.dict_professors)
