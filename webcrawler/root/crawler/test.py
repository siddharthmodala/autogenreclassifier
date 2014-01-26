'''
Created on Nov 27, 2013

@author: Siddharth
'''

import urllib.request
from bs4 import BeautifulSoup


if __name__ == '__main__':

    inputfile = open("F:/AIProject/Crawler/Input.csv","r")
    for inputfilename in inputfile:
        print(inputfilename)
        file = open(inputfilename[:-1],"r")
        outputfilename = inputfile.readline()
        output = open(outputfilename[:-1],"w");
        print(outputfilename)
        for line in file:
            #line = "http://www.imdb.com/title/tt0077402/"

            #reads the Title of the Movie
            print(line)
            response = urllib.request.urlopen(line)
            moviepage = BeautifulSoup(response.read())
            titletag = moviepage.find("h1",class_="header")
            title = '"'+titletag.span.string+'"'

            #Extracts the Genre of a Movie
            genre = moviepage.find("div",class_="infobar")
            genrelist="";
            for a in genre.find_all("span",class_="itemprop"):
                genrelist+=a.string+","

            genrelist = '"'+genrelist[:-1]+'"'

            # Extracts the biggest summary of the Movie
            plotsummary = line[:-1] + "plotsummary"
            response = urllib.request.urlopen(plotsummary);
            summarypage = BeautifulSoup(response.read())
            summary  =""
            for plot in summarypage.find_all("p",class_="plotSummary"):
                plot = plot.get_text()
                if len(summary) < len(plot):
                    summary = plot

            if summary != '':
                summary = '"' +summary.strip()+'"'
                outputstring = title + "," + genrelist + "," + summary +"\n"
                output.write(outputstring)
        file.close()
        output.close()
    inputfile.close()