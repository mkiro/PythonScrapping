import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

print('Este es el principio de mi scrapping')
#driver = webdriver.Chrome('/path/to/chromedriver') 
#driver=webdriver.Chrome(executable_path='chromedriver')
#Abrimos el chrome con la pagina a tratar
driver = webdriver.Chrome("C:/DriversPersonales/chromedriver.exe")
driver.get("https://www.fotocasa.es/es/")
driver.maximize_window()
time.sleep(2)
#Nos saltamos la confidencialidad de aceptar cookies
consentimiento=driver.find_element_by_xpath('//button[@data-testid="TcfAccept"]')
consentimiento.click()
time.sleep(2)
#Vamos a darle al boton de alquilar vivienda
alquilar=driver.find_element_by_xpath('.//div[@class="re-Search-selectorContainer re-Search-selectorContainer--rent"]')
alquilar.click()
time.sleep(2)
#Vamos a buscar la población que queramos
buscador=driver.find_element_by_xpath('.//div[@class="sui-MoleculeAutosuggest-input-container"]/input')
buscador.click()
buscador.send_keys('Badalona')
time.sleep(2)
buscador.send_keys(Keys.ENTER)
time.sleep(2)
#LLegamos a la pagina del listado
#Filtraremos por Tipo de Vivienda
#Class sui-MoleculeSelectPopover title Precio
#Sin probar 
filtraje_precio=driver.find_element_by_xpath('.//div[@title="Precio"]')
filtraje_precio.click()
time.sleep(2)
#precio = driver.find_element_by_xpath('.//div[@class="sui-MoleculeSelect-inputSelect-container"]')
precio = driver.find_element_by_xpath('.//ul[@class="sui-MoleculeDropdownList sui-MoleculeDropdownList--small"]')
precio.click()
#sin probar
#Examples https://stackoverflow.com/questions/38212644/selenium-select-item-from-list-by-the-ul-li-value-text
#1.
#String value = "10929";
#WebElement dropdown = driver.findElement(By.id("grdAvailableGroups"));
#dropdown.click(); // assuming you have to click the "dropdown" to open it
#dropdown.findElement(By.cssSelector("li[value=" + value + "]")).click();

#2
#String searchText = "AppraisersGroupTest";
#WebElement dropdown = driver.findElement(By.id("grdAvailableGroups"));
#dropdown.click(); // assuming you have to click the "dropdown" to open it
#List<WebElement> options = dropdown.findElements(By.tagName("li"));
#for (WebElement option : options)
#{
#    if (option.getText().equals(searchText))
#    {
#        option.click(); // click the desired option
#        break;
#    }
#}

#3
#String text = "AppraisersGroupTest";
#WebElement el = driver.findElement(By.xpath("//div[@id = 'colLeft_OrderGroups']/descendant::li[text() = '" + text + "']"));
#el.click();


for i in range(15):   
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt)
    listaProductos=[]
    productos = soup.find_all('div',class_="re-Card-priceComposite")
    for producto in productos:
        titulo=producto.find('span').getText()       
        listaProductos.append(titulo)
    ActionChains(driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(0.5)
print(listaProductos)