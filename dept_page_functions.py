# dept_page_functions.py
"""a file of department page functions to scrape out individual course page urls"""

import requests
from bs4 import BeautifulSoup
import re


def get_content_div_from_page(
    dept_url="https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=202301&topicid=GE&type=Credit",
):
    """
    dept_url = <str>
    returns <bs4.element.Tag>

    """
    page = requests.get(dept_url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_content_div = soup.find(
        "div",
        attrs={"id": "content"},
    )
    return page_content_div


def get_course_list_dl_from_content_div(page_content_div_bs4_element_Tag):
    """
    input: <bs4.element.Tag> object that contains just html in the conent div
    output: <bs4.element.Tag> object that contains just html in the dl div, the "table" of links
    """
    dl_bs4_element_Tag = page_content_div_bs4_element_Tag.find(
        "dl", class_="course-list"
    )
    return dl_bs4_element_Tag


def get_list_of_course_links_from_dl(dl_bs4_element_Tag):
    """
    input: <bs4.element.Tag> object that contains just html in the dl div, the "table" of links
    output: <list> a list of urls from the "table" of links
    """
    link_lst = []
    dd_bs4_element_Tag = dl_bs4_element_Tag.find_all("dd")
    for dd in dd_bs4_element_Tag:
        a_tag = dd.find("a", href=True)
        link_str = a_tag.get("href")
        link_lst.append(link_str)
    return link_lst


def get_list_of_course_links_from_dept_page(
    dept_url="https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=202301&topicid=GE&type=Credit",
):
    """
    input: <str> the url of a department page showing courses offered that quarter
    output: <list> a list of urls from the "table" of links
    """
    content_div = get_content_div_from_page(dept_url)
    dl = get_course_list_dl_from_content_div(content_div)
    link_lst = get_list_of_course_links_from_dl(dl)
    return link_lst


def main():
    dept_page_url = "https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=202301&topicid=GE&type=Credit"
    link_lst = get_list_of_course_links_from_dept_page(dept_page_url)
    print(link_lst)
    return link_lst


if __name__ == "__main__":
    main()
