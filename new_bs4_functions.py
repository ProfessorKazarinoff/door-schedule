# new_bs4_functions.py

import requests
from bs4 import BeautifulSoup
import bs4

def get_CRN_from_table_row(table_row):
    if table_row.th:
        return table_row.th.text.strip()
    else:
        return None

def get_roomnum_from_table_row(table_row):
    if table_row.find_all('td')[0].text.strip().lstrip('and').strip() and len(table_row.find_all('td')[0].text.strip().lstrip('and').strip())>2 and len(table_row.find_all('td')[0].text.strip().lstrip('and').strip())<12:
        return table_row.find_all('td')[0].text.strip().lstrip('and').strip()
    else:
        return None

def get_day_and_time_from_table_row(table_row):
    if table_row.find_all('td')[1].text.rstrip().lstrip():
        return table_row.find_all('td')[1].text.rstrip().lstrip()
    else:
        return None

def get_dates_of_instruction_from_table_row(table_row):
    if table_row.find_all('td')[2].text.rstrip().lstrip():
        return table_row.find_all('td')[2].text.rstrip().lstrip()
    else:
        return None

def get_instructor_from_table_row(table_row):
    if table_row.find_all('td')[-1].text.rstrip().lstrip():
        return table_row.find_all('td')[-1].text.rstrip().lstrip().split('\n')[2].rstrip().lstrip()
    else:
        return None


def pull_time_blocks_from_html_table_rows_list(html_table_rows_list):
    class_time_block_list = []
    prev_crn = ''
    prev_room_num = ''
    for row in html_table_rows_list:
        # create empty class_time_block_dict
        class_time_block = {}

        # pull out the CRN
        CRN_str = get_CRN_from_table_row(row)
        if CRN_str and len(CRN_str) == 5 and CRN_str.isalnum():
            # print(CRN_str)
            prev_crn = CRN_str
        else:
            CRN_str = prev_crn
        class_time_block['CRN'] = CRN_str

        # pull out the room number
        room_num_str = get_roomnum_from_table_row(row)
        if room_num_str and len(room_num_str) < 12 and room_num_str.isalpha:
            prev_room_num = room_num_str
        else:
            room_num_str = prev_room_num
        class_time_block['room_num'] = room_num_str

        # pull out the day and time
        day_and_time_str = get_day_and_time_from_table_row(row)
        if day_and_time_str:
            class_time_block['day_and_time'] = day_and_time_str
        else:
            class_time_block['day_and_time'] = None

        ## pull out days of instruction
        # days_of_instruction_str = get_dates_of_instruction_from_table_row(row)
        # if days_of_instruction_str:
        #    class_time_block['days_of_instruction']=days_of_instruction_str
        # else:
        #    class_time_block['days_of_instruction']=None

        # pull out the instructor name
        instructor_name_str = get_instructor_from_table_row(row)
        if instructor_name_str:
            class_time_block['instructor'] = instructor_name_str
        else:
            class_time_block['instructor'] = None

        # append the time block list
        class_time_block_list.append(class_time_block)

    return class_time_block_list

def main():
    # url ="".join(['https://www.pcc.edu/schedule/', 'default.cfm?fa=dspCourse2&thisTerm=201802&crsCode=CMET235&subjCode=CMET&crsNum=235&topicCode=CMET&subtopicCode=%20'])
    url = "https://www.pcc.edu/schedule/default.cfm?fa=dspCourse2&thisTerm=202001&crsCode=ENGR&subjCode=ENGR&crsNum=101&topicCode=GE&subtopicCode=%20"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html_table = soup.find('table', {'class': 'jxScheduleSortable', 'data-term': '202001'})
    html_table_body = html_table.find('tbody')
    html_table_rows_list = html_table_body.findAll(True, {'class': ['data-row', 'data-row alt-color']})
    time_block_list = pull_time_blocks_from_html_table_rows_list(html_table_rows_list)
    print(time_block_list)

if __name__ == "__main__":
    main()