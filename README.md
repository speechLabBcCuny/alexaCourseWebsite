# alexaCourseWebsite

Simple Amazon Lambda backend for alexa cisc 1600 skill to read upcoming lecture topics and assignments. Based on example "Color" skill.

1. Reads the [course website](http://mr-pc.org/t/cisc1600/)
1. Finds the first lecture that is in the future, describes it
1. Finds the first assignment that is in the future, describes it

Makes some assumptions about HTML / CSS details of the course website table organization and naming:
* The table has id="weeks"
* Its first three columns are: date, topic, assignments
* Dates are in YYYY/MM/DD format and class starts at 11am
* Multiple assignments are separated by newlines after being parsed, which happens from BeautifulSoup when they are inline list items

