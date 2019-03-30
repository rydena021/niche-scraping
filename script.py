# the first link is what I used mostly to write this script but the other two links 
# might be helpful if you want to try another approach

# https://docs.python-guide.org/scenarios/scrape/
# https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
# https://codeburst.io/web-scraping-101-with-python-beautiful-soup-bb617be1f486


# to execute this script, you must have python3 installed as well as pip3
# from the console:
# `pip3 install lxml`
# `pip3 install requests`
# `pip3 install csv`
# `pip3 install re`

# make sure there is a blank .csv file named 'top_districts.csv' before execution

# to execute the script:
# `python3 script.py`

from lxml import html
import requests
import csv
import re

# initialize empty array
export_array = []
# array of states (Hawaii is missing bc it only has one district and it was fucking up my script)
states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia', 'Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New-Hampshire','New-Jersey','New-Mexico','New-York','North-Carolina','North-Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode-Island','South-Carolina','South-Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West-Virginia','Wisconsin','Wyoming']
# index
i = 0
# loop over each state
while i < len(states):
    # set page url
    page = requests.get('https://www.niche.com/k12/search/largest-school-districts/s/%s/' % states[i])
    # idk what this does
    tree = html.fromstring(page.content)
    #This will create a list of districts:
    districts = tree.xpath('//h2[@class="search-result__title"]/text()')
    # This will create a list of # of schools and # of students.
    # These are combined because the html elements share the same class name
    # and I didn't want to spend the time working out how to separate the two
    schools_students = tree.xpath('//span[@class="search-result-fact__value"]/text()')
    # uncomment the line below to print output to console
    # print(schools_students)
    # intialize empty array that will contain hashes of the top districts
    hash_array = []
    # indices 
    j = 0
    k = 0
    # Derek wanted the top ten for each state but I am looping through 11 times because
    # there was typically one sponsored district in the top ten
    while j < 11:
        # does the district exist
        if (districts[j]):
            # for each district, create a hash of the name, # schools, and # students
            new_hash = { 
                "district": districts[j], 
                "schools": schools_students[k],
                "students": schools_students[k + 1]
            }
            # add the hash entry to our array
            hash_array.append(new_hash)
        # increment indices
        j += 1
        k += 2 # +2 because #schools and #students are combined
    # after looping through the top 10 districts, add the array of hashes to our export array
    export_array.append( { states[i]: hash_array})
    # increment index, on to next state
    i += 1

# open a blank csv file named 'top_districts.csv' in write mode
with open('top_districts.csv', mode='w') as csv_file:
    # the csv file's headers
    fieldnames = ['state', 'district', 'schools', 'students']
    # write the headers
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # initialize index
    i = 0 
    # loop through our entries (by state)
    while i < len(export_array):
        # this makes an array of our top ten districts for each state
        group = export_array[i][states[i]]
        # initialize index
        j = 0 
        # for each entry in our group array
        while j < len(group):
            # for the sponsored districts , instead of a number for students,
            # they give the teacher:student ratio
            # this evaluates to true if there's a semicolon
            sponsored = (':' in group[j]["students"]) 
            # if it's not a sponsored district, write to the csv
            if not sponsored :
                writer.writerow({'state': states[i], 'district': group[j]["district"], 'schools': group[j]["schools"], 'students': group[j]["students"]})
            # increment index, on to next district for current state
            j += 1
        # increment index, on to our next state
        i += 1
