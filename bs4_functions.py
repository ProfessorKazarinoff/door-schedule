
# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import bs4

def get_course_num(soup):
    """
    input: bs4 Soup Object, from a PCC Class Schedule Course Page
    output: str, string that is the course number, Example: 'CMET235'
    """
    return soup.h2.text.split(" ")[0]

def get_course_name(soup):
    """
    input: bs4 Soup Object, from a PCC Class Schedule Course Page
    output: str, string that is the course name, Example: 'Machine Design'
    """
    return " ".join(soup.h2.text.split(" ")[1:]).strip()

def get_dept(soup):
    """
    input: bs4 Soup Object, from a PCC Class Schedule Course Page
    output: str, string that is the department name, Example: 'CMET'
    """
    course_num = soup.h2.text.split(" ")[0]
    return ''.join([i for i in course_num if not i.isdigit()])

def get_CRN(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    return row_lst[0].td.text

def get_campus(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if " / " in td.text.strip():
            campus = td.text.strip().split(" ")[0]
            return campus

def get_building(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if " / " in td.text.strip():
            building = td.text.strip().split(" / ")[1]
            return building.strip()

def get_room_num(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if " / " in td.text.strip():
            room = td.text.strip().split(" / ")[2]
            return room.strip()

def get_start_time(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if ":" in td.text.strip():
            start_time = td.text.strip().split("-")[0]
            return start_time.strip()

def get_end_time(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if ":" in td.text.strip():
            end_time = td.text.strip().split("-")[1]
            return end_time.strip()

def get_days(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    regexes = [
        # your regexes here
        re.compile('M'),
        re.compile('Tu'),
        re.compile('W'),
        re.compile('Th'),
        re.compile('F'),
        re.compile('Sa'),
        re.compile('Su')
    ]
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
        if len(td.text.strip())<3 and td.text.strip().isalpha:
            #re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad') will return ['The','Long','And','Winding','Road']
            return td.text.strip()

def get_start_date(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if " thru " in td.text.strip():
            start_date = td.text.strip().split(" thru ")[0]
            return start_date.strip()

def get_end_date(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[0].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if " thru " in td.text.strip():
            end_date = td.text.strip().split(" thru ")[1]
            return end_date.strip()

def get_cancelled(row_lst):
    ### Function needs work. Does not quite work right
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[1].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if "Canceled!" in td.text.strip():
            return True
        else:
            return False

def get_instructor(row_lst):
    """
    input: row_lst, a list of bs4Tag objects with 2 elements, one data-row and one info-row
    """
    td_lst = row_lst[1].find_all("td")
    for td in td_lst:
    #print(td.text.strip())
        if "Instructor: " in td.text.strip():
            instructor = td.text.strip().rstrip().lstrip().split('\n')[0].strip('Instructor: ')
            return instructor     

def get_instrSect(row_lst):
    one_instr_sec = InstrSect()
    one_instr_sec.campus = get_campus(row_lst)
    one_instr_sec.CRN = get_CRN(row_lst)
    one_instr_sec.building = get_building(row_lst)
    one_instr_sec.room_number = get_room_num(row_lst)
    one_instr_sec.start_time = get_start_time(row_lst)
    one_instr_sec.end_time= get_end_time(row_lst)
    one_instr_sec.day = get_days(row_lst)
    one_instr_sec.start_date = get_start_date(row_lst)
    one_instr_sec.end_date = get_end_date(row_lst)
    one_instr_sec.instructor = get_instructor(row_lst)
    one_instr_sec.cancelled = get_cancelled(row_lst) # function needs work, does not quite work right.
    return one_instr_sec

class InstrSect():
    def __init__(self):
        self.ID=''
        self.CRN=''
        self.building=''
        self.day=''
        self.start_time=''
        self.end_time=''
        self.room_number= ''
        self.instructor=''
        self.campus=''
        self.course_name=''
        self.course_number=''
        self.department=''
        self.start_date=''
        self.end_date=''
        self.textbook_cost=''
        self.tuition=''
        self.fees=''
        self.cancelled=False
        self.year=''
        self.quarter=''


def get_instr_sec_lst(url):
    """
    Function takes in a PCC class schedule page URL and outputs a list of InstrSect objects. Each InstrSect Object has a number of different attributes such as:

    InstrSect.CRN
    InstrSect.start_time
    InstrSect.end_time

    :param url: str, a url of a pcc class schedule page such as: 'https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=201802&crsCode=EET112&subjCode=EET&crsNum=112&topicCode=EET&subtopicCode=%20'
    :return: lst: a list of InstrSect objects. Each object in the list corresponds to on instructor session of time.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    course_num = get_course_num(soup)
    course_name = get_course_name(soup)
    dept = get_dept(soup)    

    rows = soup.findAll('tr', attrs={'class': ['data-row ','info-row ','data-row alt-color','info-row alt-color']})
    inst_sec_lst = []
    for i in range(int(len(rows)/2)):
        #print('This is instructor time block {}'.format(i))
        row_lst = rows[i*2:i*2+2]
        instr_sec = get_instrSect(row_lst)
        instr_sec.course_number = course_num
        instr_sec.course_name = course_name
        instr_sec.department = dept
        inst_sec_lst.append(instr_sec)
        
    return inst_sec_lst


def main():
    url = 'https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=201802&crsCode=ENGR&subjCode=ENGR&crsNum=262&topicCode=GE&subtopicCode=%20'
    print(url)
    print("getting instructor section objects")
    instr_section_list = get_instr_sec_lst(url)
    for section in instr_section_list:
        pprint(section.__dict__)
        print()



if __name__ == "__main__":
    main()

