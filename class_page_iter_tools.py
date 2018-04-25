# coding: utf-8

#Class Page Inter tools

import requests
from bs4 import BeautifulSoup
import urllib

def get_dept_urls(main_url='https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=200701&type=Credit', dept_lst=['Civil and Mechanical Engineering Technology', 'Engineering', 'Electronic Engineering Technology']):
    """
    A function to return a list of urls for all of the department pages after when the main class schedule page url is given
    :param main_url: str, the main schedule page url default 'https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=200701&type=Credit'
    :param dept_lst: lst, list of strings each a full url or a department schedule page
    :return: lst, a list of strings each a url for a department page
    """
    dept_url_lst=[]
    base_url = 'https://www.pcc.edu/schedule/'
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if link.text in dept_lst:
            extension = link.get("href")
            url = urllib.parse.urljoin(base_url,extension)
            dept_url_lst.append(url)
    
    return dept_url_lst

def get_class_url_lst(dept_url_lst=['https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=201802&topicid=CMET&type=Credit', 'https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=201802&topicid=EET&type=Credit', 'https://www.pcc.edu/schedule/default.cfm?fa=dspTopicDetails&thisTerm=201802&topicid=GE&type=Credit']):
    """
    A function to return a list of urls for all of the course pages when a department page is given
    :param main_url: lst, list of strings. Each string is a department schedule url
    :return: lst, a list of strings each a url for a course page
    """
    class_url_lst=[]
    base_url = 'https://www.pcc.edu/schedule/'
    for url in dept_url_lst:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for course in soup.find_all('dd'):
            if course.a.get("href"):
                ext = course.a.get("href")
                url = urllib.parse.urljoin(base_url,ext)
                class_url_lst.append(url)
                
    return class_url_lst

def main():
    main_url='https://www.pcc.edu/schedule/default.cfm?fa=dspTopic&thisTerm=200701&type=Credit'
    dept_lst=['Civil and Mechanical Engineering Technology', 'Engineering', 'Electronic Engineering Technology']
    dept_url_lst = get_dept_urls(main_url, dept_lst)
    class_url_lst = get_class_url_lst(dept_url_lst)
    for url in class_url_lst:
        print(url)
    #dept_pages_lst = iter_dept_pages(url)
    #for dept_page_url in dept_pages_lst:
        #print(dept_page_url)

if __name__ == "__main__":
    main()