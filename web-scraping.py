# PPHA 30537: Python Programming for Public Policy
# Spring 2023
# HW7: Web Scraping
# Author: Danya Sherbini

##################

# Question 2: On the following Harris School website:
# https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics
# There is a list of six bullet points under "Required courses" and ten 
# bullet points under "Elective courses".  Using requests and BeautifulSoup: 
#   - Collect the text of each of these bullet points
#   - Add each bullet point to the csv_doc list below as strings (following 
#     the header already specified). The first string you add should be: 
#     'required,PPHA 30535 or PPHA 30537,Data and Programming for Public Policy I\n'
#     (recall that \n is the new-line character in text)
#   - Using context management, write the contents of csv_doc out to a file named q2.csv
#   - Finally, import Pandas and test loading q2.csv with the read_csv function.
#     Use asserts to test that the dataframe has 16 rows and three columns.

import os

path = '/Users/danya/Documents/GitHub/personal github/homework-7-dsherbini'
os.chdir(path)

csv_doc = ['type,code,course title\n']

import requests
from bs4 import BeautifulSoup

url = 'https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics'
file = os.path.join(path, 'q2.csv')

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

body = soup.find(class_='node--content--main--body')
bullets = body.find_all('li')[5:21]
bullets = [val.text for val in bullets]
bullets[14] = bullets[14].replace('/', 'or')
bullets = [b.split() for b in bullets]

bullets_rows = [
    f"{word_list[0]} {word_list[1]} {word_list[2]} {word_list[3]} {word_list[4]}, {' '.join(word_list[5:])}"
    if i < 3 or i == 14
    else f"{word_list[0]} {word_list[1]}, {' '.join(word_list[2:])}"
    for i, word_list in enumerate(bullets)]

bullets_rows = [
    f"Required, {''.join(word_list[0:])}"
    if i < 6
    else f"Elective, {''.join(word_list[0:])}"
    for i, word_list in enumerate(bullets_rows)]

header = ('type,code,course title')
bullets_rows.insert(0, header)
document = '\n'.join(bullets_rows)

with open(file, 'w') as ofile:
    ofile.write(document)
