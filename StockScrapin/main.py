import requests
from bs4 import BeautifulSoup as soup

print("Searching lowest priced items on eBay and Amazon")
search = input("What is the search?\n")

eBayUrl = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='

for chars in search:
    if chars != ' ':
        eBayUrl += chars;
    else:
        eBayUrl += '+'

eBayUrl += '&_sop=15'

AmazonUrl = 'https://www.amazon.com/s?k='

for chars in search:
    if chars != ' ':
        AmazonUrl += chars;
    else:
        AmazonUrl += '+'

AmazonUrl += '&s=price-asc-rank'

print("searching " + search)

eBayClient = requests.get(eBayUrl)
AmazonClient = requests.get(AmazonUrl)

eBayPage = eBayClient.text
AmazonPage = AmazonClient.text

eBayClient.close()
AmazonClient.close()

eBaySoup = soup(eBayPage, "html.parser")
AmazonSoup = soup(AmazonPage, "html.parser")

eBayContainer = eBaySoup.findAll("a", {"class":"s-item__link"})
AmazonContainer = AmazonSoup.findAll("a", {"class":"a-link-normal a-text-normal"})
print(AmazonUrl)

print("eBay Results:")

for item in eBayContainer:
    print(item.h3.text)
    option = input("Is this the item your are looking for? [y/n]")

    if len(option) > 0:
        if option[0] == 'y' or option[0] == 'Y':
            cheapestItem = item.h3.text;
            break

    print('\n')

print('\n')
print("Amazon Results:")

for item in AmazonContainer:
    print(item.span.text)
    option = input("Is this the item your are looking for? [y/n]")

    if len(option) > 0:
        if option[0] == 'y' or option[0] == 'Y':
            cheapestItem = item.span.text;
            break

    print('\n')

