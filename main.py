# main.py

from dept_page_functions import get_list_of_course_links_from_dept_page

dept_url = "https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=202301&topicid=GE&type=Credit"
# from the department page, grab a list of the urls for course pages
course_page_url_lst = get_list_of_course_links_from_dept_page(dept_url)
