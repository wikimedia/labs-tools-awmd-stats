import urllib2
import json

# fetch HTML from url and select the wikitable only
def fetchUser(userId):

    url = 
    if userId!="":
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        htmlTable = result.read()

        # make sure the response is not empty
        if htmlTable !="":
            soup = BeautifulSoup(htmlTable,"html.parser")
            htmlTable = soup.find_all('table', attrs={'class': 'wikitable'})[0] #grab the first table
    return htmlTable
