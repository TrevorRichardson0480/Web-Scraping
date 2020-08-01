import requests
from os import path
from bs4 import BeautifulSoup as soup


def main():
    symbols = []
    containers = []
    url = 'https://finance.yahoo.com/quote/'

    option = input("Load previously saved symbols or type new symbols? [l/t] ")

    if option == 't':
        i = 0
        option = 'y'

        while option == 'y' or option == 'Y':
            symbol = input("What is the symbol? ")
            symbols.append(symbol + '\n')
            i += 1
            option = input("Would you like to continue adding symbols? [y/n] ")

        option = input("Save symbol(s) for future use? [y/n] ")

        if option =='y' or option == 'Y':
            f = open(__file__[:__file__.rfind('/')] + "savedSymbols.txt", "w")

            for symbol in symbols:
                f.write(symbol)

            f.close()

    elif option == 'l' or option == "L":
        if path.exists(__file__[:__file__.rfind('/')] + "savedSymbols.txt"):
            f = open(__file__[:__file__.rfind('/')] + "savedSymbols.txt", "r")
            symbols = f.readlines()
            f.close()

        else:
            print("Error: No previously saved symbols!")
            return 0

    else:
        print("Error: invalid input")
        return 0

    print("\nSearching symbols:")

    i = 0
    while i < len(symbols):
        container = []
        client = requests.get(url + symbols[i][:symbols[i].find('\n')])
        page = client.text

        if page.__contains__("<title>Symbol Lookup from Yahoo Finance</title>"):
            print(symbols[i][:symbols[i].find('\n')] + " is an invalid symbol, and will be ignored.")
            symbols.remove(symbols[i])
            continue
        else:
            print(symbols[i][:symbols[i].find('\n')])
            i += 1

        client.close()
        stockSoup = soup(page, "html.parser")
        container.append(stockSoup.findAll("span", {"class":"C($primaryColor) Fz(14px) Fw(500)"}))
        container.append(stockSoup.findAll("span", {"class":"Trsdu(0.3s)"}))
        container.append(stockSoup.findAll("td", {"data-test":"DAYS_RANGE-value"}))
        container.append(stockSoup.findAll("td", {"data-test":"FIFTY_TWO_WK_RANGE-value"}))
        containers.append(container)

    option = input("\nExport Data? [y/n] ")

    i = 1
    if option == 'y' or option == 'Y':
        while(path.exists(__file__[:__file__.rfind('/')] + "ExportStockData" + str(i) + ".csv")):
            i += 1

        f = open(__file__[:__file__.rfind('/')] + "ExportStockData" + str(i) + ".csv", "w")
        f.write("Symbol:,Price:,,Close:,Open:,Previous Close:,,Daily High:,Daily Low:,52-Week High:,52-Week Low:\n")

    i = 0
    for symbol in symbols:
        currentPrice = containers[i][0][0].text
        closePrice = containers[i][1][0].text
        changeSincePreviousClose = containers[i][1][1].text
        currentChange = containers[i][1][2].text
        previousClose = containers[i][1][3].text
        openingPrice = containers[i][1][4].text
        dailyHigh = containers[i][2][0].text[(containers[i][2][0].text.find(" ") + 3):]
        dailyLow = containers[i][2][0].text[:containers[i][2][0].text.find(" ")]
        fiftyTwoHigh = containers[i][3][0].text[(containers[i][3][0].text.find(" ") + 3):]
        fiftyTwoLow = containers[i][3][0].text[:containers[i][3][0].text.find(" ")]

        i += 1

        print('\n' + symbol[:symbol.find('\n')] + ':')
        print("Price: " + currentPrice + " " + currentChange)
        print("Previous close: " + previousClose + " " + changeSincePreviousClose)
        print("Closed: " + closePrice)
        print("Open: " + openingPrice)
        print("Daily Range: " + dailyLow + '-' + dailyHigh)
        print("52-Week Range: " + fiftyTwoLow + '-' + fiftyTwoHigh)

        if option == 'y' or option == 'Y':
            f.write(symbol[:symbol.find('\n')] + ',' + currentPrice + ',' + currentChange + ',' + closePrice + ',' + openingPrice + ',' +
                    previousClose + ',' + changeSincePreviousClose + ',' + dailyHigh + ',' + dailyLow + ',' + fiftyTwoHigh +
                    ',' + fiftyTwoLow + '\n')


    if option == 'y' or option == 'Y':
        print("\nData exported as " + f.name[__file__.rfind('/') + 1:])
        f.close()


main()