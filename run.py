# coding: utf-8
"""
Main script will webscrape PCC class schedule course pages for instructors, rooms and times.
Using the class schedule webpage data, schedules for each instructor is created in the output directory
"""

from class_page_iter_tools import get_dept_urls, get_class_url_lst
from bs4_functions import get_instr_sec_lst
from schedule_functions import instructorObj


def main():
    # get a list of the department page urls
    dept_url_lst = get_dept_urls()

    # get a long list of all the class page urls
    class_url_lst = get_class_url_lst(dept_url_lst)

    # iterate through all class page urls and build a list of SectionObjects
    instr_section_list = []
    for url in class_url_lst:
        instr_section_list.extend(get_instr_sec_lst(url))

    # make a unique set of instructor names
    instructor_set = set([x.instructor for x in instr_section_list])

    # a list of instructor Objects, each instructor has a list of class schedule objects
    instr__obj_list = []
    for instructor in list(instructor_set):
        # print(instructor)
        inst_Obj = instructorObj(instructor)
        # print(inst_Obj.name)
        # print(type(inst_Obj))
        inst_Obj.classes = [x for x in instr_section_list if x.instructor == instructor]
        inst_Obj.departments = list(set([x.department for x in instr_section_list if x.instructor == instructor]))
        instr__obj_list.append(inst_Obj)

    instr__obj_list[5].print_schedule()

    for instr_obj in instr__obj_list:
        # schedule = makexl_schedule_object
        pass
        for sect_obj in instr_obj.classes:
            #add sect_obj to schedule
            pass
    # save schedule in output folder with instructor name and year, quarter


if __name__ == "__main__":
    main()
