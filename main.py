# main.py

from dept_page_functions import get_list_of_course_links_from_dept_page
from class_page_functions import get_lst_of_time_block_dicts_from_course_page

dept_url = "https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=202301&topicid=GE&type=Credit"
# from the department page, grab a list of the urls for course pages
course_page_url_lst = get_list_of_course_links_from_dept_page(dept_url)
for course_page_url in course_page_url_lst:
    time_block_dict_lst = get_lst_of_time_block_dicts_from_course_page(course_page_url)
