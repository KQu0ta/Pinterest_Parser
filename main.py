from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import Config 
import urllib.request
import time
import os


driver = webdriver.Chrome(options=Options().add_experimental_option("detach", True))


def log_in(email: str, password: str):
    driver.implicitly_wait(10) 
    driver.get("https://ru.pinterest.com/login/")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()





def create_folder(search_name_true_or_false: bool, path_to: str, search_name):
    if not search_name_true_or_false:
        for name_path in search_name:
            try:
                os.mkdir(os.path.join(path_to, name_path))
            except:
                print("File already exists")
        

def main(number_of_photo: int, path_to: str):
    for name in os.listdir(path_to):
        if len(os.listdir(os.path.join(path_to, name))) != (number_of_photo):
            a = driver.find_element(By.XPATH, "//input[@name='searchBoxInput']")
            a.send_keys(name, Keys.ENTER)
            time.sleep(5)

            while len(os.listdir(f"{path_to}{name}")) <= number_of_photo:
                for image in range(1, len(driver.find_elements(By.XPATH, f"(//img[@loading='auto'])"))):
                    try:
                        if not (driver.find_element(By.XPATH, f"(//img[@loading='auto'])[{image}]").get_attribute("srcset")):
                            name_image = driver.find_element(By.XPATH, f"(//img[@loading='auto'])[{image}]").get_attribute("src")
                            urllib.request.urlretrieve(name_image, f"{path_to}{name}\\{name_image.split('/')[-1]}.jpg")
                            
                        else:
                            if len(driver.find_element(By.XPATH, f"(//img[@loading='auto'])[{image}]").get_attribute("srcset").split(" ")) != 1:
                                name_image = driver.find_element(By.XPATH, f"(//img[@loading='auto'])[{image}]").get_attribute("srcset").split(" ")[-2]
                                urllib.request.urlretrieve(name_image, f"{path_to}{name}\\{name_image.split('/')[-1]}.jpg")
                    except:
                        print("Failed dowload photo")
                driver.execute_script("window.scrollBy({top: 1000, left: 0, behavior: 'smooth'});")
                time.sleep(2)
            driver.find_element(By.XPATH, "//input[@name='searchBoxInput']").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.XPATH, "//input[@name='searchBoxInput']").send_keys(Keys.DELETE)








if __name__ == "__main__":
    create_folder(Config.search_name_true_or_false, Config.path_to, Config.search_name)
    log_in(Config.email, Config.password)
    main( Config.number_of_photo, Config.path_to)
    for j in os.listdir(Config.path_to):
        colect = len(os.listdir(f'{Config.path_to}{j}'))
        print(f"{j} - {colect}")