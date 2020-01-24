# new_bs4_functions.py

import requests
from bs4 import BeautifulSoup
import bs4
from time_block_functions import fix_start_time
from bs4_functions import get_course_num, get_course_name, get_dept
from pprint import pprint


def get_CRN_from_table_row(table_row):
    if table_row.th:
        return table_row.th.text.strip()
    else:
        return None


def get_room_num_from_table_row(table_row):
    if (
        table_row.find_all("td")[0].text.strip().lstrip("and").strip()
        and len(table_row.find_all("td")[0].text.strip().lstrip("and").strip()) > 2
        and len(table_row.find_all("td")[0].text.strip().lstrip("and").strip()) < 12
    ):
        return table_row.find_all("td")[0].text.strip().lstrip("and").strip()
    else:
        return None


def get_day_and_time_from_table_row(table_row):
    if table_row.find_all("td")[1].text.rstrip().lstrip():
        return table_row.find_all("td")[1].text.rstrip().lstrip()
    else:
        return None


def get_day_from_day_and_time(day_and_time_str):
    day_str = day_and_time_str.split(" from ")[0].rstrip().lstrip()
    return day_str.split("\n")[-1]


def get_time_from_day_and_time(day_and_time_str):
    return day_and_time_str.split(" from ")[-1].rstrip().lstrip()


def get_start_time_from_time_str(time_str):
    return time_str.split("- to ")[0]


def get_stop_time_from_time_str(time_str):
    return time_str.split("- to ")[-1]


def get_dates_of_instruction_from_table_row(table_row):
    if table_row.find_all("td")[2].text.rstrip().lstrip():
        return table_row.find_all("td")[2].text.rstrip().lstrip()
    else:
        return None


def get_instructor_from_table_row(table_row):
    if table_row.find_all("td")[-1].text.rstrip().lstrip():
        return (
            table_row.find_all("td")[-1]
            .text.rstrip()
            .lstrip()
            .split("\n")[2]
            .rstrip()
            .lstrip()
        )
    else:
        return None


def get_instructor_first_name_from_instructor_str(instructor_str):
    return instructor_str.split(" ")[0]


def get_instructor_last_name_from_instructor_str(instructor_str):
    return instructor_str.split(" ")[-1]


def pull_time_blocks_from_html_table_rows_list(html_table_rows_list):
    time_block_list = []
    prev_crn = ""
    prev_room_num = ""
    for row in html_table_rows_list:
        # create empty class_time_block_dict
        time_block = {}

        # pull out the CRN
        CRN_str = get_CRN_from_table_row(row)
        if CRN_str and len(CRN_str) == 5 and CRN_str.isalnum():
            # print(CRN_str)
            prev_crn = CRN_str
        else:
            CRN_str = prev_crn
        time_block["CRN"] = int(CRN_str)

        # pull out the room number
        room_num_str = get_room_num_from_table_row(row)
        if room_num_str and len(room_num_str) < 12 and room_num_str.isalpha:
            prev_room_num = room_num_str
        else:
            room_num_str = prev_room_num
        time_block["room_number"] = room_num_str[-3:].strip()
        time_block["building"] = room_num_str[3:-3].strip()
        time_block["campus"] = room_num_str[:2].strip()

        # pull out the day and time
        day_and_time_str = get_day_and_time_from_table_row(row)
        if day_and_time_str:
            time_block["day"] = get_day_from_day_and_time(day_and_time_str)
            time_str = get_time_from_day_and_time(day_and_time_str)
            time_block["start_time"] = get_start_time_from_time_str(time_str)
            time_block["stop_time"] = get_stop_time_from_time_str(time_str)
        else:
            time_block["day"] = None
            time_block["time"] = None

        # fix the start time so that it is in the format of 11:00am
        time_block = fix_start_time(time_block)

        # pull out the instructor name
        instructor_name_str = get_instructor_from_table_row(row)
        if instructor_name_str:
            time_block[
                "instructor_first_name"
            ] = get_instructor_first_name_from_instructor_str(instructor_name_str)
            time_block[
                "instructor_last_name"
            ] = get_instructor_last_name_from_instructor_str(instructor_name_str)
        else:
            time_block["instructor_first_name"] = None
            time_block["instructor_last_name"] = None

        # append the time block list
        time_block_list.append(time_block)

    return time_block_list


def pull_time_block_list_from_url(url):
    # grab the page with bs4
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # pull out course number, title and department. These fields are the same for all time blocks on the page
    course_num_str = get_course_num(soup)
    course_title_str = get_course_name(soup)
    department_str = get_dept(soup)
    # pull out the html_table from the page
    html_table = soup.find(
        "table", {"class": "jxScheduleSortable", "data-term": "202001"}
    )
    html_table_body = html_table.find("tbody")
    # create a list of table rows
    html_table_rows_list = html_table_body.findAll(
        True, {"class": ["data-row", "data-row alt-color"]}
    )
    # from the list of table rows, pull out the time blocks as dicts and create a big list of time blocks
    time_block_list = pull_time_blocks_from_html_table_rows_list(html_table_rows_list)

    # Add the course listing to each time block. Each time block on one page has the same course listing.
    for time_block in time_block_list:
        time_block["course_num"] = course_num_str
        time_block["course_title"] = course_title_str
        time_block["department"] = department_str

    return time_block_list


def main():
    url = "https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=202001&crsCode=ENGR&subjCode=ENGR&crsNum=101&topicCode=GE&subtopicCode=%20"
    time_block_list = pull_time_block_list_from_url(url)
    pprint(time_block_list)


if __name__ == "__main__":
    main()
