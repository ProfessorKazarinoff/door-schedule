# GUI.py

"""A Python Gooey application that builds a faculty door schedule from the
Portland Community College main class listing web site"""

from pathlib import Path
import os
import pickle
import shutil
from gooey import Gooey, GooeyParser

from class_page_iter_tools import get_dept_urls, get_class_url_lst
from bs4_functions import get_instr_sec_lst
from schedule_functions import (
    instructorObj,
    insert_gen_info,
    insert_class_sec,
    get_24h_dec_time,
)
from openpyxl import load_workbook


@Gooey(dump_build_config=True, program_name="Door Schedule Building GUI")
def main():
    desc = "A Python GUI App to build a door schedule"
    year_help_msg = "Enter the year like 2019"
    quarter_help_msg = "Enter the quarter like Fall or 01"
    first_name_select_help_msg = "Enter your last name, use a capital first letter"
    last_name_select_help_msg = "Enter your last name, use a capital first letter"
    template_select_help_msg = (
        "select a .xlsx template to use as the base of your schedule"
    )
    dir_select_help_msg = "select an output directory"
    depts_select_help_msg = (
        "Enter the department codes separated by a comma. Like: CMET, ENGR"
    )
    email_address_help_msg = "Enter your email address like: first.last@pcc.edu"
    phone_help_msg = "Enter your office phone number like 971-722-8065"

    my_parser = GooeyParser(description=desc)
    my_parser.add_argument(
        "Year", default="2020", help=year_help_msg, widget="TextField"
    )
    my_parser.add_argument(
        "Quarter", default="Winter", help=quarter_help_msg, widget="TextField"
    )
    my_parser.add_argument(
        "Last_Name",
        default="Kazarinoff",
        help=last_name_select_help_msg,
        widget="TextField",
    )
    my_parser.add_argument(
        "First_Name",
        default="Peter",
        help=first_name_select_help_msg,
        widget="TextField",
    )
    my_parser.add_argument(
        "Departments",
        default="CMET, ENGR",
        help=depts_select_help_msg,
        widget="TextField",
    )
    my_parser.add_argument(
        "Email_Address",
        # required=False,
        default="peter.kazarinoff@pcc.edu",
        help=email_address_help_msg,
        widget="TextField",
    )
    my_parser.add_argument(
        "Phone",
        # required=False,
        default="971-722-8065",
        help=phone_help_msg,
        widget="TextField",
    )

    args = my_parser.parse_args()
    # URL of main class listing page:
    # https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=202001&type=Credit
    q_dict = {
        "winter": "01",
        "spring": "02",
        "summer": "02",
        "fall": "04",
        "1": "01",
        "2": "02",
        "3": "03",
        "4": "04",
    }
    q_num_str = q_dict[args.Quarter.lower()]
    main_url = f"https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm={args.Year}{q_num_str}&type=Credit"
    print(main_url)
    dept_code_lst = args.Departments.strip().split(",")
    dept_code_dict = {
        "CMET": "Civil and Mechanical Engineering Technology",
        "ENGR": "Engineering",
        "EET": "Electronic Engineering Technology",
    }
    dept_name_lst = [dept_code_dict[dept_code.strip()] for dept_code in dept_code_lst]
    year_str = args.Year
    quarter_str = args.Quarter
    email_str = args.Email_Address
    phone_str = args.Phone
    depts_str = args.Departments
    first_name_str = args.First_Name
    last_name_str = args.Last_Name
    # get a list of the department page urls
    dept_url_lst = get_dept_urls(main_url, dept_name_lst)
    print("/n List of Department URL's")
    print(dept_url_lst)

    # get a long list of all the class page urls
    class_url_lst = get_class_url_lst(dept_url_lst)
    print("/n List of Class Pages URL's")
    print(class_url_lst)

    # iterate through all class page urls and build a list of SectionObjects
    instr_section_list = []
    for url in class_url_lst:
        instr_section_list.extend(get_instr_sec_lst(url))

    # for sec in instr_section_list:
    # print(sec)
    instructor_set = {"Peter Kazarinoff"}

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
            [inst_name, "_", year_str, "Q", q_num_str, ".xlsx"]
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
        full_name_str = " ".join([first_name_str, last_name_str])
        wb = load_workbook(template_path)
        ws = wb.active
        ws = insert_gen_info(
            ws, quarter_str, year_str, full_name_str, depts_str, email_str, phone_str,
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
