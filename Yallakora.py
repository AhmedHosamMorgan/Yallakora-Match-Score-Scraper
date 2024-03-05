import csv
import requests
from bs4 import BeautifulSoup

print ("Jalla Kora Match Score By Date.")
date = input("Enter The Date In This Formatting YYYY/MM/DD: ")
page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    match_details = []

    championships = soup.find_all("div", {"class": "matchCard"})

    def Get_Match_Info(championship):
        Championship_Title = championship.contents[1].find('h2').text.strip()
        All_Matches = championship.contents[3].find_all("div", {"class": "teamsData"})

        if All_Matches:
            for i in range(len(All_Matches)):
                # Team Name
                Team_A = All_Matches[i].find('div', {"class": "teams teamA"}).text.strip()
                Team_B = All_Matches[i].find('div', {"class": "teams teamB"}).text.strip()

                # Match Score
                Match_Result = All_Matches[i].find('div', {"class": "MResult"}).find_all("span", {"class": "score"})
                score = f"{Match_Result[0].text.strip()} ||  {Match_Result[1].text.strip()}"
                # Match Time
                Match_Time = All_Matches[i].find('div', {"class": "MResult"}).find("span", {"class": "time"}).text.strip()

                # Save Matches Details
                match_details.append({
                    "نوع البطولة": Championship_Title,
                    "الفريق الاول": Team_A,
                    "الفريق الثاني": Team_B,
                    "نتيجة المباراة": score,
                    "موعد المباراة": Match_Time
                })


    for championship in championships:
        Get_Match_Info(championship)

    keys = match_details[0].keys()

# Save The Result In CSV
    with open("Yallakora.csv", 'w', encoding='utf-8-sig', newline='') as output_file:
        csvwriting = csv.DictWriter(output_file, keys)
        csvwriting.writeheader()
        csvwriting.writerows(match_details)
        print("Yallakora.csv File Created.")

main(page)
