# class_page_functions.py
"""a file of department page functions to scrape out course sections from individual course page urls"""

import requests
from bs4 import BeautifulSoup
import re

from dept_page_functions import get_content_div_from_page

def get_table_from_course_page_content(page_content_div_bs4_element_Tag):
    """
    input: <bs4.element.Tag> object that contains just html in the conent div
    output: <bs4.element.Tag> object that contains just html in the table div, the "table" of course sections
    """
    table_bs4_element_Tag = page_content_div_bs4_element_Tag.find('table', class_="jxScheduleSortable")
    return table_bs4_element_Tag

def get_table_body_from_course_page_content(table_bs4_element_Tag):
    """
    input: <bs4.element.Tag> object that contains just the table div
    output: <bs4.element.Tag> object that contains just the table body div (no table headers)
    """
    table_body_bs4_element_Tag = table_bs4_element_Tag.find('tbody')
    return table_body_bs4_element_Tag

def get_list_of_table_rows(table_body_bs4_element_Tag):
    row_list = table_body_bs4_element_Tag.find_all("tr")
    return row_list

def get_timeblock_dict_from_row(row):
    d = {}
    CRN = row.attrs.get("data-group")
    td_lst = row.find_all("td")
    class_type = td_lst[0].text.replace("and ","").strip()
    location = td_lst[1].text.strip()
    if location == "—Not applicable":
        location = "Remote"
    instructor =""
    if len(td_lst)==5:
        instructor = td_lst[4].text
    elif len(td_lst)>=6:
        instructor = td_lst[5].text
    days = td_lst[2].attrs.get("data-sort-value").replace("A","")
    d["days"] = days
    d["crn"]=CRN
    d["class_type"] = class_type
    d["location"] = location
    d["instructor"] = instructor
    print(d)
    return d

def get_lst_of_time_block_dicts_from_course_page(course_page_url="https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=202301&crsCode=ENGR101&topicCode=GE&subtopicCode=%20"):
    page_content_soup = get_content_div_from_page(course_page_url)
    table_soup = get_table_from_course_page_content(page_content_soup)
    table_body_soup = get_table_body_from_course_page_content(table_soup)
    row_list = get_list_of_table_rows(table_body_soup)
    time_block_lst = []
    for row in row_list:
        time_block_dict = get_timeblock_dict_from_row(row)
        time_block_lst.append(time_block_dict)

def main():
    course_page_url = "https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=202301&crsCode=ENGR101&topicCode=GE&subtopicCode=%20"
    page_content_soup = get_content_div_from_page(course_page_url)
    table_soup = get_table_from_course_page_content(page_content_soup)
    table_body_soup = get_table_body_from_course_page_content(table_soup)
    row_list = get_list_of_table_rows(table_body_soup)
    for row in row_list:
        time_block_dict = get_timeblock_dict_from_row(row)


if __name__ == "__main__":
    main()
