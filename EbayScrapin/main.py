from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.ebay.com/sch/richwav-wxpok2mby/m.html?_nkw=&_armrs=1&_ipg=&_from='

uClient = uReq(my_url)
page = uClient.read()
uClient.close()

soup = soup(page, "html.parser")

container = soup.findAll("li", {"class":"lvformat"})
containerName = soup.findAll("a", {"class":"vip"})

print("\n")

for i in range(int(len(container) / 2)):
    print(containerName[i]["title"][26:])
    print(container[i * 2].text + "\n")

f = open("MyBidInfo.csv", "w")
f.write("Ad Name:,Bids:\n\n")

for i in range(int(len(container) / 2)):
    f.write(containerName[i]["title"][26:].replace(",", " ") + "," + container[i * 2].text + "\n")

f.close()

print("File Exported")