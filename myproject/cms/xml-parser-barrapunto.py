#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

import urllib.request
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):

        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Titulo: " + self.theContent + "."
                myfile.write("<li>" + '\n' + line + "</li>" + '\n')
                print(line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                link = self.theContent
                print(link)
                myfile.write("<li><a href=" + link + ">Link</a></li>")

                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<2:
    print ("Usage: python xml-parser-barrapunto.py <document>")
    print ("<document>: file name of the document to parse")
    sys.exit(1)

myfile = open('/home/alumnos/nalonso/Documentos/saro/GitHub/X-Serv-XML-Barrapunto/Modificaciones/index.html', 'w')
html = "<!DOCTYPE html>" + '\n' + "<html>" + '\n' + "<head>" + '\n' + "HTML CON TITULOS Y LINKS DE BARRAPUNTO" + '\n' + "</head>"+ '\n' + "<body>"+ '\n' + "<ul>"
myfile.write(html + '\n')

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
print("XML FILE: " + str(xmlFile))
theParser.parse(xmlFile)

html = "</ul>" + '\n' + "</body>" + '\n' + "</html>"
myfile.write(html + '\n')


print ("Parse complete")
