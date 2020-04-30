from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.page_load_strategy = 'eager'

# Initialize empty lists for analysis
grossIncome = list()
realIncome = list()

with webdriver.Chrome(options=options) as driver:

    driver.get('https://www.calculador.com.br/calculo/salario-liquido')
    # Set constants for the analysis
    driver.find_element_by_id("Entrada_NumDependentes").send_keys("0")
    driver.find_element_by_id("Entrada_OutrosDescontos").send_keys("0")

    #
    driver.find_element_by_id("Entrada_SalarioBruto").send_keys("500000")
    driver.find_element_by_id("Calcular").click()
    time.sleep(1) # Wait to make sure the calculation was done

    # Identify the element from the table using it's XPath
    resultado = driver.find_element_by_xpath("//*[@id='calculator-result']/div[3]/table/tbody/tr[6]/td[2]")
    # Get the inner HTML, remove the first and second characters (R$) and the "."
    valor = resultado.get_attribute("innerHTML")[2:].replace(".","")
    # Change the cents separator from , to .
    valor = valor.replace(",",".")
    realIncome.append(float(valor))


    print(realIncome)