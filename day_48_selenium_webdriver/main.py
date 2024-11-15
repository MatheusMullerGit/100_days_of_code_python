from selenium import webdriver
import time

chrome_driver_path = "C:/Users/Mathe/Documents/Repositorios/100_days_of_code_python/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get("https://orteil.dashnet.org/cookieclicker/")

#Get cookie to click on.
cookie = driver.find_element_by_id("bigCookie")

#Get upgrade item ids.


timeout = time.time() + 10
minutos = 60
stop_time = time.time() + 60*minutos # 5minutes

while True:
    cookie.click()

    #Every 5 seconds:
    if time.time() > timeout:

        item_prices=[]
        item_ids=[]
        #Get all upgrade <b> tags
        all_prices = driver.find_elements_by_css_selector("#products.storeSection span")
        prices = [price.text for price in all_prices if price!=""]
        all_ids = [price.get_attribute("id") for price in all_prices]
#        print(prices)
#        print(all_ids)
        
        #Convert <b> text into an integer price.
        count = 0
        for price in prices:
            element_text = price
            if element_text != "":
                try:
                    cost = int(element_text.replace(",", ""))
                except:
                    cost_str = element_text.split(" ")
                    if cost_str[1] == 'million' or cost_str[1] == 'millions':
                        cost = int(float(cost_str[0])*1000000)
                item_prices.append(cost)
                item_ids.append(all_ids[count])
            count +=1

#        print(item_prices)
#        print(item_ids)
        
        #Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #Get current cookie count
        money_element_comma = driver.find_element_by_id("cookies").text
        money_element = money_element_comma.replace(",", "")
        cookie_count = int(money_element.split(" ")[0])
        cookie_per_sec = float(money_element.split(" ")[4])

        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id

        #Purchase the most expensive affordable upgrade
        try:
            highest_price_affordable_upgrade = min(affordable_upgrades)
            print(highest_price_affordable_upgrade)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
#            print(to_purchase_id)
#            print(driver.find_element_by_id(to_purchase_id).text)
            element = driver.find_element_by_id(to_purchase_id)
            driver.execute_script("arguments[0].click();", element)
        except:
            pass
        
        print(cookie_per_sec)
        
        #Add another 5 seconds until the next check
        timeout = time.time() + 10

    #After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > stop_time:
        print(cookie_per_sec)
        break