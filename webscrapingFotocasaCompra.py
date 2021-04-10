import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import csv
from datetime import datetime
import numpy as np


tiempo = 1

print('Este es el principio de mi scrapping fotocasa de compra')
#driver = webdriver.Chrome('/path/to/chromedriver') 
#driver=webdriver.Chrome(executable_path='chromedriver')
#Abrimos el chrome con la pagina a tratar
driver = webdriver.Chrome("C:/DriversPersonales/chromedriver.exe")
weburl = 'https://www.fotocasa.es/es/'
driver.get(weburl)
driver.maximize_window()
time.sleep(tiempo)
#Nos saltamos la confidencialidad de aceptar cookies
consentimiento=driver.find_element_by_xpath('//button[@data-testid="TcfAccept"]')
consentimiento.click()
time.sleep(tiempo)
#Vamos a darle al boton de alquilar vivienda
comprar=driver.find_element_by_xpath('.//div[@class="re-Search-selectorContainer re-Search-selectorContainer--buy"]')
comprar.click()
time.sleep(tiempo)
#Vamos a buscar la población que queramos
buscador=driver.find_element_by_xpath('.//div[@class="sui-MoleculeAutosuggest-input-container"]/input')
buscador.click()
buscador.send_keys('Badalona')
#buscador.send_keys('Bonavista - Bufalà - Morera, Badalona')
time.sleep(tiempo)
buscador.send_keys(Keys.ENTER)
time.sleep(tiempo)
#LLegamos a la pagina del listado
#Filtraremos por Tipo de Vivienda

#Inicio - FPP Filtraremos por precio
filtraje_precio = driver.find_element_by_xpath("//div[@title='Precio']")
filtraje_precio.click()
time.sleep(tiempo)

texto_minimo = "50.000 €";
texto_maximo = "100.000 €";
#texto_maximo = "75.000 €";

#Filtrar por precio
precio_minimo = driver.find_element_by_xpath("//div[@class='sui-MoleculeSelect']")
precio_minimo.click()
time.sleep(tiempo)
list_precio_minimo= driver.find_element_by_xpath(".//div[@class='sui-MoleculeSelect']/ul/li/span[.='" + texto_minimo + "']")
list_precio_minimo.click()
time.sleep(tiempo)

precio_maximo = driver.find_element_by_xpath("//input[@id='Máximo']//ancestor::div[@class='sui-MoleculeSelect']")
precio_maximo.click()
time.sleep(tiempo)
list_precio_maximo = driver.find_element_by_xpath("//input[@id='Máximo']//ancestor::div[@class='sui-MoleculeSelect']/ul/li/span[.='" + texto_maximo + "']")
list_precio_maximo.click()

#Ver anuncios
buttonFilter=filtraje_precio.find_element_by_css_selector('.sui-AtomButton--solid')
ActionChains(driver).click(buttonFilter).perform()

#Fin - FPP Filtraremos por precio
time.sleep(tiempo)

for i in range(15):   
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt)
    listaPrecios=[]
    listaTitulos=[]
    listaUbicacion=[]
    listaUrl=[]
    productos = soup.find_all('div',class_="re-Card-priceComposite")
    for producto in productos:
        titulo=producto.find('span').getText()       
        listaPrecios.append(titulo)
    
    productos_titulo = soup.find_all('div',class_="re-Card-wrapperTitle")
    for producto_titulo in productos_titulo:
        titulo=producto_titulo.find('span').getText()       
        ubicacion = producto_titulo.find('h3',class_="re-Card-title").getText()
        listaTitulos.append(titulo)      
        listaUbicacion.append(ubicacion)
    
    productos_url= soup.find_all('a',class_="re-Card-link")
    for producto_url in productos_url:
        url = producto_url['href']
        startwith = '/es/comprar/vivienda'
        if url[0:len(startwith)] == startwith:
            listaUrl.append(weburl + url[4:len(url)])

# Añadir mas caracteristicas re-CardFeatures-wrapper"
# Meter que se haga link
# Poder paginar todas las paginas
# Refactorizar codigo para hacerlo mas usable -- como modular funciones en python
# Scrapping de BOE - subastas
# Scrapping https://www.idealista.com/venta-viviendas/barcelona-barcelona/
# Configurar el excel para que vaya metiendo y descartando los que ya vi.. BdD ?? 
# Machine Learning con fotos para nota .. link .. fotos descargar en una carpeta visualizaar .. para nota :)

        

    ActionChains(driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(0.5)
print(listaPrecios)
print(listaTitulos)
print(listaUrl)

#Recuperar mas valores de la lista - pensar -- meter en una funcion en una archivo e importamos luego
#añadirlo en un archivo css
#myData = [["price", "second_name", "Grade"],
#          ['Alex', 'Brian', 'A'],
#          ['Tom', 'Smith', 'B']]


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
print("timestamp =", timestamp)

##Dataframe
#df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
#                   'mask': ['red', 'purple'],
#                   'weapon': ['sai', 'bo staff']})
#df.to_csv(index=False)

csvHeader = ["price","titulo","ubicacion","href"]
csvPrice = np.array(listaPrecios)
csvUbicacion = np.array(listaUbicacion)
csvTitulo = np.array(listaTitulos)
csvUrl = np.array(listaUrl)
csvData = [csvHeader,csvPrice,csvTitulo,csvUbicacion,csvUrl]

df = pd.DataFrame({'price': listaPrecios,
                   'titulo': listaTitulos,
                   'ubicacion': listaUbicacion,
                   'href':listaUrl
                  })


namefile = 'listFotocasaCompra_{}.csv'.format(timestamp) 
myFile = open(namefile, 'w')
with myFile:
    writer = csv.writer(myFile,delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerows(df.to_records())
    
     
print("Writing complete")