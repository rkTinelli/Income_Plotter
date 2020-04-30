from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt

options = Options()
options.page_load_strategy = 'eager'

def createAnalysisList(starValue,endValue,step):
    grossList = list()
    aux = startValue
    while endValue > aux:
        grossList.append(aux)
        aux = aux + step
    grossList.append(endValue)
    return grossList

# Initial variables
startValue = 1000.00
endValue = 10000.00
step = 250.00

# Initialize empty lists for analysis
grossIncome = createAnalysisList(startValue,endValue,step)
realIncome = list()

with webdriver.Chrome(options=options) as driver:

    driver.get('https://www.calculador.com.br/calculo/salario-liquido')
    # Set constants for the analysis
    driver.find_element_by_id("Entrada_NumDependentes").send_keys("0")
    driver.find_element_by_id("Entrada_OutrosDescontos").send_keys("0")

    # Loop through the gross income list to gather real income data
    for x in range(len(grossIncome)):
        # format the value to have 2 decimal places and convert it to string
        valueUsed = str("{:.2f}".format(grossIncome[x]))
        driver.find_element_by_id("Entrada_SalarioBruto").clear()
        driver.find_element_by_id("Entrada_SalarioBruto").send_keys(valueUsed)
        driver.find_element_by_id("Calcular").click()
        time.sleep(1) # Wait to make sure the calculation was done

        # Identify the element from the table using it's XPath
        resultado = driver.find_element_by_xpath("//*[@id='calculator-result']/div[3]/table/tbody/tr[6]/td[2]")
        # Get the inner HTML, remove the first and second characters (R$) and the "."
        valor = resultado.get_attribute("innerHTML")[2:].replace(".","")
        # Change the cents separator from , to .
        valor = valor.replace(",",".")
        realIncome.append(float(valor))

plt.plot(grossIncome, realIncome)
plt.xlabel("Gross Income", fontsize=14)
plt.ylabel("Real Income", fontsize=14)
plt.axis([0, grossIncome[-1] + step, 0, realIncome[-1] + step])
plt.show()