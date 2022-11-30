# Author: Hazem Ahmed Abdelraouf
# Date: 7th Rabi' Al-Akhir 1444 Hijri | 1st November 2022  
# Purpose: To make a client-server application 
# to scrape famous people information and first quote


import re
from bs4 import BeautifulSoup
import urllib.request as request
from urllib.error import HTTPError, URLError

from famousPerson import FamousPerson

def input_validate_int(*,end, start = 1):
    """
    Function to validate integer input from the user,
    making sure that it is between start and end
    """
    while True:
        usr_input = input()
        if usr_input.isdecimal():
            if start is not None and end is not None:
                usr_input = int(usr_input)
                if start <= usr_input <= end:
                    return usr_input
                else:
                    print(f'Please enter a valid number from {start} to {end}:',end=' ')                
        else:
            print(f'Please enter a valid number from {start} to {end}:',end=' ')


def get_day_month():
    """
    Function to get the day and month from the user
    """
    print("Enter day number or 0 to exit:",end=" ")
    # get input and validate
    day = input_validate_int(start=0, end=31)
    if day == 0:
        return 0 , 0
    print("Enter month number or 0 to exit:",end=" ")
    month = input_validate_int(start=0, end=12)
    return day, month

def get_page(day, month):
    """
    Function to connect to the website and retrieve the html page 
    of the list of people who were born in the passed day and month
    """
    birth_date_url = "/birthdays/{month}_{day}".format(month = month, day = day)
    req= request.Request(PLANE_URL + birth_date_url, headers=headers)
    print('Please wait while getting the information to you.')    
    try:    
        # getting the 9 famous people tags        
        with request.urlopen(req) as response:
            page = response.read()
            return page
    except HTTPError as err:
        if err.code == 404:
            print("This date doesn't exist, please try again")
           
        elif err.code == 403:
            print('Please check your connection and try again later')
            
    except URLError as err:
        print('Please check your connection and try again')
    except:
        print('Error Please try again')

    return None
    
def get_month_name(month_num):
    """Function to get the month name corresponding to the month number"""
    
    month_names = ['january',
                   'february',
                   'march',
                   'april',
                   'may',
                   'june',
                   'july',
                   'august',
                   'september',
                   'october',
                   'november',
                   'december'] 
    return month_names[month_num-1]

def get_famous_ppl(famous_ppl_tags):
    """
    Function to connect to the website and retrieve all the html pages of
    the 9 famous people, then extract their information from it
    """
    ppl_list = []
    # extracting each person info
    for tag in famous_ppl_tags:
        name = tag.text
        famous_url = tag.attrs['href']
        req = request.Request(PLANE_URL + famous_url, headers=headers)
        try:
            with request.urlopen(req) as response:
                famous_page = response.read()
        # In case an error happened while connecting to the server to get the famous people html pages
        except Exception as err:
            if len(ppl_list) == 0:
                print("Unexpected error while connecting to the server.")
                print('Please check your connection and try again')
            else:
                print(f'Error while getting the rest of the famous people information')
                print(f'We have succesfully managed to get {len(ppl_list)} out of {len(famous_ppl_tags)}')
                print('Please check your connection and try again if the following people don\'t interest you.')
            return ppl_list
        
        famous_soup = BeautifulSoup(famous_page, 'html.parser')
        # getting the div that has in it the person's info 
        raw_info = famous_soup.find('div',attrs = {"class": "subnav-below-p"} )
        # extracting each information piece from thier respective html tag 
        nationality = raw_info.find('a', attrs={"href":re.compile(r".nationality.")}).text
        profession = raw_info.find('a', attrs={"href":re.compile(r".profession.")}).text
        birthdate = raw_info.find('a', attrs={"href":re.compile(r".birthdays.")}).text + raw_info.contents[-1].text.strip()
        # getting the first quote tag and extracting the quote text from it
        quote_tag = famous_soup.find('div', attrs={"style":"display: flex;justify-content: space-between"})
        first_quote = quote_tag.text
        
        person = FamousPerson(name, nationality, profession, birthdate, first_quote)
        ppl_list.append(person)
    
    return ppl_list



headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

PLANE_URL = "https://www.brainyquote.com"
if __name__ == '__main__':
    while True:
        # getting the day and month numbers
        day, month_num = get_day_month()
        if day == 0 or month_num == 0:
            print('Bye, see you!')
            break
        
        month_name = get_month_name(month_num)
        # getting the html page that has the list of famous people
        famous_ppl_page = get_page(day, month_name)

        if famous_ppl_page is None:
            continue

        # getting each person page 'a' tag for thier page url extraction
        attrs = {"href": re.compile(r"/authors/.")}
        mysoup = BeautifulSoup(famous_ppl_page,features='html.parser')
        famous_ppl_tags = mysoup.find_all('a', attrs=attrs, limit=9)
        
        # extracting each famous person details 
        famous_ppl_list = get_famous_ppl(famous_ppl_tags)
        if len(famous_ppl_list) == 0:
            continue
        
        print('\n\n\n')
        # promoting the user to select a person from a list    
        for idx, person in enumerate(famous_ppl_list):
            print(f'{idx+1}. {person.get_name()}')
        print('Please enter the number of the person you want:', end=' ')
        user_choice = input_validate_int(start=1, end= len(famous_ppl_list))
        # printing the chosen famous person information and 1st quote
        print(famous_ppl_list[user_choice-1])