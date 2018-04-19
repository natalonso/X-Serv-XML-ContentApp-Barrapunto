from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from .models import Page
import urllib.request
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys


html = "hola"


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

        global html

        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Titulo: " + self.theContent + "."
                html += "<li>" + '\n' + line + "</li>" + '\n'
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                link = self.theContent
                html += "<li><a href=" + link + ">Link</a></li>"

                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


formulario = """
<form action="" method="POST">
    Name: <input type="text" name="name"><br>
    Page: <input type="text" name="page"><br>
    <input type="submit" value="Enviar">
</form>
"""

@csrf_exempt
def home_anotated(request): #PAGINA PRINCIPAL

    global html

    html = "<br>LINKS DE BARRAPUNTO<br><br>"
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(xmlFile)


    if request.method == 'POST':

        newpage= Page(name=request.POST['name'], page=request.POST['page'])
        newpage.save()

    if request.user.is_authenticated():
        logged = 'Logged in as: ' + request.user.username + "<br><a href='/logout'>Logout</a><br><br>"
        permiso = True
    else:
        logged = "Not logged in. <br><a href='/login'>Login</a><br><br>"
        permiso = False

    lista = Page.objects.all()
    salida = "<h4>" + logged + "</h4><br>"
    salida += "<h1>Bienvenido al servidor CMS, estas son las paginas disponibles hasta el momento: </h1><br>"
    salida += "<ul>"
    for pagina in lista:
        salida += '<li><h3><a href=' + str(pagina.name) + '>' + pagina.name + '</a></h3>'
    salida += "</ul>"
    salida += "<h4>" + html + "</h4>"

    if permiso == True: #estas logeado
        salida += formulario
        template = get_template("terrafirma/index.html")
        c =({'title' : "SERVIDOR CMS", 'contenido' : salida})
        return HttpResponse(template.render(c) + html)
    else: #no estas logeado
        template = get_template("terrafirma/index.html")
        c =({'title' : "SERVIDOR CMS", 'contenido' : salida})
        return HttpResponse(template.render(c))


@csrf_exempt
def home(request): #PAGINA PRINCIPAL

    global html

    html = "<!DOCTYPE html>" + '\n' + "<html>" + '\n' + "<head>" + '\n' + "TITULOS Y LINKS DE BARRAPUNTO" + '\n' + "</head>"+ '\n' + "<body>"+ '\n' + "<ul>"

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(xmlFile)

    html += "</ul>" + '\n' + "</body>" + '\n' + "</html>"

    if request.method == 'POST':
        newpage= Page(name=request.POST['name'], page=request.POST['page'])
        newpage.save()

    if request.user.is_authenticated():
        logged = 'Logged in as: ' + request.user.username
        permiso = True
    else:
        logged = 'Not logged in.'
        permiso = False

    lista = Page.objects.all()
    salida = "Bienvenido al servidor CMS, estas son las paginas disponibles hasta el momento: "
    salida += "<ul>"
    for pagina in lista:
        salida += '<li><a href=' + str(pagina.name) + '>' + pagina.name + '</a>'
    salida += "</ul>"

    if permiso == True: #estas logeado
        return HttpResponse(logged + '<br><a href= "/logout">Logout</a><br><br>' + salida + formulario + html)
    else: #no estas logeado
        return HttpResponse(logged + '<br><a href= "/login">Login</a><br><br>' + salida + html)

@csrf_exempt
def pagina(request, pagina):

    global html

    html = "<!DOCTYPE html>" + '\n' + "<html>" + '\n' + "<head>" + '\n' + "TITULOS Y LINKS DE BARRAPUNTO" + '\n' + "</head>"+ '\n' + "<body>"+ '\n' + "<ul>"

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(xmlFile)

    html += "</ul>" + '\n' + "</body>" + '\n' + "</html>"

    lista = Page.objects.all()
    for elemento in lista:
        if elemento.name == pagina:
            salida = elemento.page
            break
        else:
            salida = None
    if salida == None:
        return HttpResponse('Lo sentimos. La pagina no esta en la base de datos por el momento.' + html)
    else:
        return HttpResponse(salida + html)

@csrf_exempt
def edit(request, nombre):

    global html

    html = "<!DOCTYPE html>" + '\n' + "<html>" + '\n' + "<head>" + '\n' + "TITULOS Y LINKS DE BARRAPUNTO" + '\n' + "</head>"+ '\n' + "<body>"+ '\n' + "<ul>"

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(xmlFile)

    html += "</ul>" + '\n' + "</body>" + '\n' + "</html>"


    if request.method == 'POST':

        if request.user.is_authenticated():
            logged = 'Logged in as: ' + request.user.username
            permiso = True
        else:
            logged = 'Not logged in.'
            permiso = False

        lista = Page.objects.all()
        for elemento in lista:
            if elemento.name == nombre:
                salida = elemento.page
                break
            else:
                salida = None
        if salida == None:
            if permiso == True:
                newpage= Page(name=nombre, page=request.POST['page'])
                newpage.save()
                return HttpResponse('La pagina no estaba en nuestra BD, ha sido añadida.' + "<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>" + html)
            else:
                return HttpResponse("No estás autenticado.<br><a href='/login'>Login</a><br><br>" + html)
        else:
            if permiso == True:
                elemento.page = request.POST['page']
                elemento.save()
                return HttpResponse("ACTUALIZADO" + "<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>" + html)
            else:
                return HttpResponse("No estas autenticado.<br><a href='/login'>Login</a><br><br>" + html)
    else:
        lista = Page.objects.all()
        for elemento in lista:
            if elemento.name == pagina:
                salida = elemento.page
                break
            else:
                salida = None
        if salida == None:
            return HttpResponse("<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page'><br><input type='submit' value='Enviar'></form>" + html)
        else:
            return HttpResponse("<form action='' method='POST'>Nuevo contenido:<br><input type='text' name='page' placeholder='" + str(elemento.page) + "'><br><input type='submit' value='Enviar'></form>" + html)
