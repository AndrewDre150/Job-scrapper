from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

# send request and parse  html
job_scrap = requests.get("https://realpython.github.io/fake-jobs/")
soup = BeautifulSoup(job_scrap.text, "html.parser")

# create csv file
file = open("fakejobs.csv", "w")
writer = csv.writer(file)

writer.writerow(['Position', 'Emploeyer', 'Location', 'Date'])

# Create connection to the database
conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="fakejobs"
    )

# Create a cursor
c = conn.cursor()

# Create a table if it doesnt exist
c.execute('CREATE TABLE IF NOT EXISTS Jobs2(Position TEXT, Employer TEXT, Location TEXT, Date TEXT)')

# Extract data 
positions = soup.find_all("h2", attrs={"class": "title is-5"})
employers = soup.find_all("h3", attrs={"class": "subtitle is-6 company"})
locations = soup.find_all("p", attrs={"class": "location"})
dates = soup.find_all("time")

# print data and add it to database
for position, employer, location, date in zip(positions, employers, locations, dates):
    position_text = position.text
    employer_text = employer.text
    location_text = location.text.strip()
    date_text = date.text.strip()
    print(position_text + " " + employer_text + " " + location_text + " " + date_text)
    writer.writerow([position_text, employer_text, location_text, date_text])   #run the csv file
    c.execute('INSERT INTO Jobs2 VALUES (%s, %s, %s, %s)', (position_text, employer_text, location_text, date_text))

# commit changes and close conneaction
conn.commit()
conn.close()

file.close()