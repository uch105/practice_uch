import requests
from bs4 import BeautifulSoup

link = "https://verify.bmdc.org.bd/regdata/CEX1P9udOA5tYKGUdHtr~vTP5zu~LlXlKm5FOML9wD5M2Lv3rzlt5qGll9PS4Z4cNxRUexULPQgWqioz9UF4Ky4.zCzmEQC8IYVqfAO9BQe7mlRSU531DmkIZe6Cm6M2"

response = requests.get(link)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    bmdc = soup.find("h3",{'class': 'mt-1'}).text
    name = soup.find("h3",{'class': 'mb-4'}).text
    h5s = soup.find_all('h5')
    regyear = h5s[0].text
    regvalidyear = h5s[1].text
    h6s = soup.find_all('h6')
    dob = h6s[0].text
    bg = h6s[1].text
    fname = h6s[2].text
    mname = h6s[3].text
    status = h6s[4].text
    print(bmdc)
    print(name)
    print(regyear)
    print(regvalidyear)
    print(dob)
    print(bg)
    print(fname)
    print(mname)
    print(status)