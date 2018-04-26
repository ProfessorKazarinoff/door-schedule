
# coding: utf-8
"""
Main script will webscrape PCC class schedule course pages for instructors, rooms and times.
Using the class schedule webpage data, schedules for each instructor is created in the output directory
"""
import pickle
import shutil
from class_page_iter_tools import get_dept_urls, get_class_url_lst
from bs4_functions import get_instr_sec_lst
from schedule_functions import instructorObj
import os
from schedule_functions import insert_gen_info, insert_class_sec
from openpyxl import load_workbook

import os


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

    #empty the out/ directory and all of its contents
    if os.path.exists(os.path.join(os.getcwd(), 'out')):
        shutil.rmtree(os.path.join(os.getcwd(), 'out'))

    #instr__obj_list[5].print_schedule()

    for instr in instr__obj_list:
        inst_name = "_".join([x.strip() for x in instr.name.split(" ")[:]])
        xlsx_file_name = "".join([inst_name, instr.quarter, instr.year, '.xlsx'])
        template_path = os.path.join(os.getcwd(),'templates','schedule_template.xlsx')
        wb = load_workbook(template_path)
        ws = wb['Sheet1']
        
        ws = insert_gen_info(ws, instr.quarter, instr.year, instr.name, " ".join(instr.departments), instr.email, instr.phone)
        
        for sect in instr.classes:
            ws = insert_class_sec(ws, sect.course_number, sect.building, sect.room_number, sect.day, sect.start_time, sect.end_time)
        
        # save schedule in output folder with instructor name and year, quarter
        wkbk_path = os.path.join(os.getcwd(),'out',xlsx_file_name)
        if not os.path.exists(os.path.join(os.getcwd(),'out')):
            os.mkdir('out')
        wb.save(wkbk_path)

    picklepath = os.path.join(os.getcwd(),'out','data.pkl')
    output = open(picklepath, 'wb')
    pickle.dump(instr__obj_list, output)
    output.close()


if __name__ == "__main__":
    main()
