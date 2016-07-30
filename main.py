from bs4 import BeautifulSoup
import urllib2
import pandas as pd

url = "http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html"

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

table = soup.find_all(class_ = "data large ")[1] #Grabs the second table containing all Gen. Election poll data

columns = [label.get_text() for label in table.find(class_ = "header")]

rows = []

for table_rows in table.find_all("tr")[2:]: #Skip the column headers and RCP average row
          rows.append([item.get_text() for item in table_rows.find_all("td")])

df = pd.DataFrame(rows, columns = columns)

#Clean Data

df["Sample_Size"] = df["Sample"].str.extract("(\d+)")
df["Sample_Type"] = df["Sample"].str.extract("([A-Z]+)")
df["Winner"] = df["Spread"].str.extract("(\D+) ")
df["Spread"] = df["Spread"].str.extract("\+(\d*)")
df["Start_Date"] = df["Date"].str.extract("^(\d+\/\d+)")
df["End_Date"] = df["Date"].str.extract("(\d+\/\d+)$")

df = df.drop(labels=["Sample","Date"], axis=1)

df.to_csv("data.csv", index=False)
