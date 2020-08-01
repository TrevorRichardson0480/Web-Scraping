import requests
from os import path
from bs4 import BeautifulSoup as soup


def main():
    # array for storing symbols and for holding containers (a container will hold data from the website)
    symbols = []
    containers = []
    # we will get the stock data from Yahoo Finances
    url = 'https://finance.yahoo.com/quote/'

    # ask user if they want to load previously saved symbols
    option = input("Load previously saved symbols or type new symbols? [l/t] ")

    # if user is typing in symbols
    if option == 't':
        i = 0
        option = 'y'

        # gather symbols and store symbol in symbols array
        while option == 'y' or option == 'Y':
            symbol = input("What is the symbol? ")
            symbols.append(symbol + '\n')
            i += 1
            option = input("Would you like to continue adding symbols? [y/n] ")

        # after user is finished adding symbols, ask to save for next time
        option = input("Save symbol(s) for future use? [y/n] ")

        # if so, save symbols to a text file
        if option =='y' or option == 'Y':
            # open file at the location of the .py
            f = open(__file__[:__file__.rfind('/')] + "savedSymbols.txt", "w")

            # write the symbols and close file
            for symbol in symbols:
                f.write(symbol)

            f.close()

    # if user wished to load from previous symbols
    elif option == 'l' or option == "L":
        # if the file exists, open the file, read all the symbols, close the file
        if path.exists(__file__[:__file__.rfind('/')] + "savedSymbols.txt"):
            f = open(__file__[:__file__.rfind('/')] + "savedSymbols.txt", "r")
            symbols = f.readlines()
            f.close()

        # if the file does not exist, terminate the 
        else:
            print("Error: No previously saved symbols!")
            return 0

    else:
        print("Error: invalid input")
        return 0

    print("\nSearching symbols:")

    i = 0
    # iterate through all the symbols
    while i < len(symbols):
        # create a container, open the client, get the page's html, close the client
        container = []
        client = requests.get(url + symbols[i][:symbols[i].find('\n')])
        page = client.text
        client.close()

        # if the page redirect to Yahoo's "Symbol Lookup", then we know that this symbol does not exist
        if page.__contains__("<title>Symbol Lookup from Yahoo Finance</title>"):
            # remove the symbol and continue the loop
            print(symbols[i][:symbols[i].find('\n')] + " is an invalid symbol, and will be ignored.")
            symbols.remove(symbols[i])
            continue

        # else print the symbol to show that we are extracting data for that symbol, increment i
        else:
            print(symbols[i][:symbols[i].find('\n')])
            i += 1

        # get the soup of the page, fill the container with data that matches the specified span class and td data-test
        stockSoup = soup(page, "html.parser")
        container.append(stockSoup.findAll("span", {"class":"C($primaryColor) Fz(14px) Fw(500)"}))
        container.append(stockSoup.findAll("span", {"class":"Trsdu(0.3s)"}))
        container.append(stockSoup.findAll("td", {"data-test":"DAYS_RANGE-value"}))
        container.append(stockSoup.findAll("td", {"data-test":"FIFTY_TWO_WK_RANGE-value"}))
        # add the container to the list of containers
        containers.append(container)

    # Ask user if they want to export the data
    option = input("\nExport Data? [y/n] ")

    i = 1
    # if yes
    if option == 'y' or option == 'Y':
        # while loop will find an available name for the file to export data
        while(path.exists(__file__[:__file__.rfind('/')] + "ExportStockData" + str(i) + ".csv")):
            i += 1

        # after finding an available name, create the file, write the csv header
        f = open(__file__[:__file__.rfind('/')] + "ExportStockData" + str(i) + ".csv", "w")
        f.write("Symbol:,Price:,,Close:,Open:,Previous Close:,Daily High:,Daily Low:,52-Week High:,52-Week Low:\n")

    i = 0
    # iterate through all the symbols and collect the data for the stock
    for symbol in symbols:
        # Data is arranged differently depending on the time of day,
        # if the first container is empty, we can tell how the data is arranged in each container
        if (len(containers[i][0]) == 0):
            currentPrice = containers[i][1][0].text
            closePrice = containers[i][1][0].text
            currentChange = containers[i][1][1].text
            previousClose = containers[i][1][2].text
            openingPrice = containers[i][1][3].text

        else:
            currentPrice = containers[i][0][0].text
            closePrice = containers[i][1][0].text
            currentChange = containers[i][1][2].text
            previousClose = containers[i][1][3].text
            openingPrice = containers[i][1][4].text

        # To my understanding, this data does not change depending on the time of day
        dailyHigh = containers[i][2][0].text[(containers[i][2][0].text.find(" ") + 3):]
        dailyLow = containers[i][2][0].text[:containers[i][2][0].text.find(" ")]
        fiftyTwoHigh = containers[i][3][0].text[(containers[i][3][0].text.find(" ") + 3):]
        fiftyTwoLow = containers[i][3][0].text[:containers[i][3][0].text.find(" ")]

        i += 1

        # Print the data
        print('\n' + symbol[:symbol.find('\n')] + ':')
        print("Price: " + currentPrice + " " + currentChange)
        print("Previous close: " + previousClose)
        print("Closed: " + closePrice)
        print("Open: " + openingPrice)
        print("Daily Range: " + dailyLow + '-' + dailyHigh)
        print("52-Week Range: " + fiftyTwoLow + '-' + fiftyTwoHigh)

        # Save the data if requested
        if option == 'y' or option == 'Y':
            f.write(symbol[:symbol.find('\n')] + ',' + currentPrice + ',' + currentChange + ',' + closePrice + ',' +
                openingPrice + ',' + previousClose + ',' + dailyHigh + ',' + dailyLow + ',' + fiftyTwoHigh +
                ',' + fiftyTwoLow + '\n')

    # after all the data is printed/exported, complete the export
    if option == 'y' or option == 'Y':
        print("\nData exported as " + f.name[__file__.rfind('/'):])
        f.close()


main()