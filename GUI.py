# GUI.py

from pathlib import Path
import os
import pickle
import shutil
from gooey import Gooey, GooeyParser

from class_page_iter_tools import get_dept_urls, get_class_url_lst
from bs4_functions import get_instr_sec_lst
from schedule_functions import instructorObj, insert_gen_info, insert_class_sec, get_24h_dec_time
from openpyxl import load_workbook

@Gooey(dump_build_config=True, program_name="Door Schedule Building GUI")
def main():
    desc = "A Python GUI App to build a door schedule"
    url_select_help_msg = "Enter the main URL like https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=201902&type=Credit"
    name_select_help_msg = "Enter your last name, use a capital first letter"
    template_select_help_msg = "select a .xlsx template to use as the base of your schedule"
    dir_select_help_msg = "select an output directory"
    depts_select_help_msg = "Enter the department codes separated by a comma. Like: CMET, ENGR"


    my_parser = GooeyParser(description=desc)
    my_parser.add_argument(
        "URL_of_credit_class_schedule",
        help=url_select_help_msg,
        widget="TextField") 
    my_parser.add_argument(
        "Last Name",
        help=name_select_help_msg,
        widget="TextField")
    my_parser.add_argument(
        "Departments",
        help=depts_select_help_msg,
        widget="TextField")

    args = my_parser.parse_args()
    main_url = args.URL_of_credit_class_schedule
    dept_code_lst = args.Departments.strip().split(',')
    dept_code_dict = {"CMET":"Civil and Mechanical Engineering Technology", "ENGR":"Engineering", "EET":"Electronic Engineering Technology"}
    dept_name_lst = [dept_code_dict[dept_code.strip()] for dept_code in dept_code_lst]
    
    # get a list of the department page urls
    dept_url_lst = get_dept_urls(main_url, dept_name_lst)
    print(dept_url_lst)
    
    # get a long list of all the class page urls
    class_url_lst = get_class_url_lst(dept_url_lst)
    print(class_url_lst)

    # iterate through all class page urls and build a list of SectionObjects
    instr_section_list = []
    for url in class_url_lst:
        instr_section_list.extend(get_instr_sec_lst(url))

    #for sec in instr_section_list:
        #print(sec)
    instructor_set = {'Peter Kazarinoff'}

    # form a list of instructor Objects, each instructor has a list of class schedule objects
    instr_obj_list = []
    for instructor in list(instructor_set):
        # print(instructor)
        inst_Obj = instructorObj(instructor)
        # print(inst_Obj.name)
        # print(type(inst_Obj))
        inst_Obj.classes = [x for x in instr_section_list if x.instructor == instructor]
        inst_Obj.departments = list(
            set(
                [x.department for x in instr_section_list if x.instructor == instructor]
            )
        )
        inst_Obj.year = "".join(
            list(
                set([x.year for x in instr_section_list if x.instructor == instructor])
            )
        )

        instr_obj_list.append(inst_Obj)


    # empty the out/ directory and all of its contents
    if os.path.exists(os.path.join(os.getcwd(), "out")):
        shutil.rmtree(os.path.join(os.getcwd(), "out"))

    # instr__obj_list[5].print_schedule()

    for instr in instr_obj_list:
        template_path = os.path.join(os.getcwd(), "templates", "schedule_template.xlsx")
        # Build the name of the excel file from the instructor object's name attribute
        inst_name_no_double_space = " ".join(instr.name.split())
        inst_name = "_".join(
            [x.strip() for x in inst_name_no_double_space.split(" ")[:]]
        )
        xlsx_file_name = "".join(
            [inst_name, instr.quarter, ".xlsx"]
        )  # can put instr.year into the list to add the year to the excel file name

        # pick between reg day or day including evening templates
        end_time_lst = [
            get_24h_dec_time(x.end_time) for x in instr.classes if x.end_time
        ]
        if end_time_lst:
            latest_class = max(end_time_lst)
            if latest_class < 12 + 5:
                print("use day template")
                template_path = os.path.join(
                    os.getcwd(), "templates", "day_schedule_template.xlsx"
                )
                print(template_path)
            else:
                template_path = os.path.join(
                    os.getcwd(), "templates", "schedule_template.xlsx"
                )
                print(template_path)

        wb = load_workbook(template_path)
        ws = wb.active
        if not instr.quarter:
            instr.quarter = 'Winter'
        ws = insert_gen_info(
            ws,
            instr.quarter,
            instr.year,
            " ".join(instr.name.split()[:]),
            " ".join(instr.departments),
            instr.email,
            instr.phone,
        )

        # iterate over the class list for each instructor, then if there are muiltiple days in one class, iterate over those days
        for sect in instr.classes:
            if sect.days_list:
                for day in sect.days_list:
                    ws = insert_class_sec(
                        ws,
                        sect.course_number,
                        sect.building,
                        sect.room_number,
                        day,
                        sect.start_time,
                        sect.end_time,
                    )

        # save schedule in output folder with instructor name and year, quarter
        wkbk_path = os.path.join(os.getcwd(), "out", xlsx_file_name)
        if not os.path.exists(os.path.join(os.getcwd(), "out")):
            os.mkdir("out")
        wb.save(wkbk_path)

    # save the list of instrutor objects with pickle so that it can be unpickled and used later if needed
    picklepath = os.path.join(os.getcwd(), "out", "data.pkl")
    output = open(picklepath, "wb")
    pickle.dump(instr_obj_list, output)
    output.close()





if __name__ == "__main__":
    main()
