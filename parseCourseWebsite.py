#!/usr/bin/python

import bs4
import datetime
import re
import urllib2

def main():
    url = "http://mr-pc.org/t/cisc1600/"
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    table = soup.body.find('table', attrs={'id' : 'weeks'})
    schedule = parseListOfLists(tableToListOfLists(table))
    print describeNextClassTopic(schedule)
    print describeNextAssignment(schedule)


def tableToListOfLists(table):
    data = []
    rows = table.findAll('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # data.append([ele for ele in cols if ele]) # Get rid of empty values
        data.append(cols)
    return data

def parseListOfLists(lol):
    return [(parseDate(row[0]), row[1], row[2].split('\n '))
            for row in lol if len(row) >= 3]
        
def parseDate(dateStr):
    return datetime.datetime.strptime(dateStr.split(u'\xa0')[0], '%Y/%m/%d').date()

def describeNextClassTopic(schedule, today=None):
    if today is None:
        today = datetime.date.today()
        
    for date, topic, due in schedule:
        if date == today:
            return "Today's topic is " + topic
        if date > today:
            dayDiff = (date - today).days
            if dayDiff == 1:
                return "Tomorrow's topic will be " + topic
            else:
                return "The next topic will be " + topic + " in " + dayDiff + " days"
            
def describeNextAssignment(schedule, today=None):
    if today is None:
        today = datetime.date.today()
        
    for date, topic, due in schedule:
        if date == today and len(due) >= 1 and len(due[0]) >= 1:
            return "Today " + formatDue(due)
        if date > today and len(due) >= 1 and len(due[0]) >= 1:
            dayDiff = (date - today).days
            if dayDiff == 1:
                return "Tomorrow " + formatDue(due)
            else:
                return "On " + date.strftime("%A, %B %d, ") + formatDue(due)

def formatDue(due):
    items = [re.sub("(\w+)$", r"is \1", item)
             for item in due if not re.search("[sS]pec", item)]
    return " and ".join(items)


if __name__ == '__main__':
    main()
    
