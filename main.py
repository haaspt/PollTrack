from bs4 import BeautifulSoup
import urllib2
import pandas as pd


url_dict = {
    "general_2way": "http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html",
    "general_3way": "http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton_vs_johnson-5949.html",
    "general_4way": "http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton_vs_johnson_vs_stein-5952.html",
    "fl_2way": "http://www.realclearpolitics.com/epolls/2016/president/fl/florida_trump_vs_clinton-5635.html",
    "fl_4way": "http://www.realclearpolitics.com/epolls/2016/president/fl/florida_trump_vs_clinton_vs_johnson_vs_stein-5963.html",
    "oh_2way": "http://www.realclearpolitics.com/epolls/2016/president/oh/ohio_trump_vs_clinton-5634.html",
    "oh_4way": "http://www.realclearpolitics.com/epolls/2016/president/oh/ohio_trump_vs_clinton_vs_johnson_vs_stein-5970.html",
    "pa_2way": "http://www.realclearpolitics.com/epolls/2016/president/pa/pennsylvania_trump_vs_clinton-5633.html",
    "pa_4way": "http://www.realclearpolitics.com/epolls/2016/president/pa/pennsylvania_trump_vs_clinton_vs_johnson_vs_stein-5964.html",
    "mi_2way": "http://www.realclearpolitics.com/epolls/2016/president/mi/michigan_trump_vs_clinton-5533.html",
    "mi_4way": "http://www.realclearpolitics.com/epolls/2016/president/mi/michigan_trump_vs_clinton_vs_johnson_vs_stein-6008.html",
    "nh_2way": "http://www.realclearpolitics.com/epolls/2016/president/nh/new_hampshire_trump_vs_clinton-5596.html",
    "nh_4way": "http://www.realclearpolitics.com/epolls/2016/president/nh/new_hampshire_trump_vs_clinton_vs_johnson_vs_stein-6022.html",
    "va_2way": "http://www.realclearpolitics.com/epolls/2016/president/va/virginia_trump_vs_clinton-5542.html",
    "va_4way": "http://www.realclearpolitics.com/epolls/2016/president/va/virginia_trump_vs_clinton_vs_johnson_vs_stein-5966.html",
    "nc_2way": "http://www.realclearpolitics.com/epolls/2016/president/nc/north_carolina_trump_vs_clinton-5538.html",
    "nc_4way": "http://www.realclearpolitics.com/epolls/2016/president/nc/north_carolina_trump_vs_clinton_vs_johnson_vs_stein-5972.html"
}
    

def scrape_data(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)

    table = soup.find_all(class_ = "data large ")[1] #Grabs the second table containing all Gen. Election poll data

    columns = [label.get_text() for label in table.find(class_ = "header")]

    rows = []

    for table_rows in table.find_all("tr")[2:]: #Skip the column headers and RCP average row
          rows.append([item.get_text() for item in table_rows.find_all("td")])

    df = pd.DataFrame(rows, columns = columns)
    return df

def clean_data(df):
    df["Sample_Size"] = df["Sample"].str.extract("(\d+)")
    df["Sample_Type"] = df["Sample"].str.extract("([A-Z]+)")
    df["Winner"] = df["Spread"].str.extract("(\D+) ")
    df["Spread"] = df["Spread"].str.extract("\+(\d*)")
    df["Spread"] = df["Spread"].fillna(0)
    df["Start_Date"] = df["Date"].str.extract("^(\d+\/\d+)")
    df["End_Date"] = df["Date"].str.extract("(\d+\/\d+)$")

    df = df.drop(labels=["Sample","Date"], axis=1)
    return df
