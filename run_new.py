# run_new.py

from class_page_iter_tools import get_dept_urls, get_class_url_lst
from new_bs4_functions import pull_time_block_list_from_url
from pprint import pprint


def main():
    main_url = (
        main_url
    ) = "https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=202001&type=Credit"
    dept_lst = [
        "Civil and Mechanical Engineering Technology",
        "Engineering",
        "Electronic Engineering Technology",
    ]

    # get a list of the department page urls
    dept_url_lst = get_dept_urls(main_url, dept_lst)

    # get a long list of all the class page urls
    class_url_lst = get_class_url_lst(dept_url_lst)
    time_block_lst = []
    # for each class url, pull out a time block list and add it to the big time block list
    for class_url in class_url_lst:
        class_time_block_lst = pull_time_block_list_from_url(class_url)
        time_block_lst.extend(class_time_block_lst)

    pprint(time_block_lst)

    return time_block_lst


if __name__ == "__main__":
    main()
