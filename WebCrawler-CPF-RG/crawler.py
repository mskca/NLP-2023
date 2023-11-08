from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Inicializar o driver do Selenium
driver = webdriver.Chrome()

# Abrir a URL desejada
url = "https://www.4devs.com.br/gerador_de_rg" # Troca tudo que tem CPF por RG e vira gerador de RG
driver.get(url)
cpfs = []
rgs = []


# Execute um script JavaScript para obter o valor do campo textarea
for i in range(100):
    print('aqui')
    bt_gerar_rg = driver.find_element(By.ID, "bt_gerar_rg")
    bt_gerar_rg.click()

    time.sleep(0.5)

    rg = driver.find_element(By.ID, "texto_rg").get_attribute('value')
    rgs.append(rg)



print(rgs)

driver.quit()

'''

for i in range(100):
    botao = driver.find_element(By.ID, "bt_gerar_cpf")
    botao.click()
    time.sleep(0.5)
    saida_cpf = driver.find_element(By.ID, "texto_cpf")
    print(saida_cpf)
    cpf = saida_cpf.text
    print(cpf)
    cpfs.append(cpf)

# Fechar o navegador

print(cpfs)
driver.quit()
'''