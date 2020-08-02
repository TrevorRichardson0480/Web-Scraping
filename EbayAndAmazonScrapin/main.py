import requests
from bs4 import BeautifulSoup as soup


def main():
    print("Searching lowest priced items on eBay and Amazon")
    search = input("What is the search? Be specific! ")

    eBayUrl = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='

    for chars in search:
        if chars != ' ':
            eBayUrl += chars
        else:
            eBayUrl += '+'

    eBayUrl += '&_sop=15&rt=nc&LH_BIN=1'

    AmazonUrl = 'https://www.amazon.com/s?k='

    for chars in search:
        if chars != ' ':
            AmazonUrl += chars
        else:
            AmazonUrl += '+'

    AmazonUrl += '&s=price-asc-rank'

    print("searching " + search + ", please wait . . .\n")

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}

    eBayClient = requests.get(eBayUrl, headers=headers)
    AmazonClient = requests.get(AmazonUrl, headers=headers)

    eBayPage = eBayClient.content
    AmazonPage = AmazonClient.content

    eBayClient.close()
    AmazonClient.close()

    eBaySoup = soup(eBayPage, "html.parser")
    AmazonSoup = soup(AmazonPage, "html.parser")

    eBayContainer = eBaySoup.findAll("a", {"class": "s-item__link"})
    AmazonContainer = AmazonSoup.findAll("a", {"class": "a-link-normal a-text-normal"})

    eBaySelectedItem = ""
    AmazonSelectedItem = ""

    print("eBay Results:")

    for item in eBayContainer:
        print(item.h3.text)
        option = input("Is this the item your are looking for? [y/n] ")

        if len(option) > 0:
            if option[0] == 'y' or option[0] == 'Y':
                eBaySelectedItem = item
                break

        print('\n')

    if eBaySelectedItem == "":
        print("It seems like we couldn't find you item. Try to be more specific with your search.")
        return 0

    print("\n\nAmazon Results:")

    for item in AmazonContainer:
        print(item.span.text)
        option = input("Is this the item your are looking for? [y/n] ")

        if len(option) > 0:
            if option[0] == 'y' or option[0] == 'Y':
                AmazonSelectedItem = item
                break

        print('\n')

    if AmazonSelectedItem == "":
        print("It seems like we couldn't find you item. Amazon failed to respond (try again), or you need to "
              + "try to be more specific with your search.")
        return 0

    print("\nPLease wait . . .\n")

    selectedEbayUrl = eBaySelectedItem["href"]
    selectedAmazonUrl = "https://www.amazon.com" + AmazonSelectedItem["href"]

    eBayClient = requests.get(selectedEbayUrl, headers=headers)
    AmazonClient = requests.get(selectedAmazonUrl, headers=headers)

    selectedEbayPage = eBayClient.content
    selectedAmazonPage = AmazonClient.content

    eBayClient.close()
    AmazonClient.close()

    selectedEbaySoup = soup(selectedEbayPage, "html.parser")
    selectedAmazonSoup = soup(selectedAmazonPage, "html.parser")

    eBayPrice = selectedEbaySoup.findAll("span", {"id": "prcIsum"})[0].text
    AmazonPrice = selectedAmazonSoup.findAll("span", {"id": "priceblock_ourprice"})[0].text
    eBayShipping = selectedEbaySoup.findAll("span", {"id": "shSummary"})
    AmazonShipping = selectedAmazonSoup.findAll("span", {"class": "a-color-secondary a-size-base"})[0].text

    eBayPriceIndex = 0
    AmazonPriceIndex = 0

    for i in range(0, len(eBayPrice)):
        if 47 < eBayPrice[i] < 58:
            eBayPriceIndex = i
            break

    for i in range(0, len(AmazonPrice)):
        if 47 < AmazonPrice[i] < 58:
            AmazonPriceIndex = i
            break

    if float(eBayPrice[eBayPriceIndex:]) < float(AmazonPrice[AmazonPriceIndex:]):
        print("eBay had the best price!")
        print("@ this url: " + selectedEbayUrl)

    elif float(eBayPrice[eBayPriceIndex:]) > float(AmazonPrice[AmazonPriceIndex:]):
        print("Amazon had the best price!")
        print("@ this url: " + selectedAmazonUrl)

    else:
        print("Both eBay and Amazon have the same price for the item!")
        print("@ these urls:")
        print("eBay: " + selectedEbayUrl)
        print("Amazon " + selectedAmazonUrl)

main()
