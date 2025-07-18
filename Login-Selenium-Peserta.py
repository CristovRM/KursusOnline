from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

driver = webdriver.Chrome()

def log_to_file(fitur, status):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('Pengujian-Login-Logout-Peserta', 'a') as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status}\n")

### === REGISTER SECTION === ###
try:
    driver.get('http://127.0.0.1:8000/register')

    unique_email = f"tes{int(time.time())}@gmail.com"

    driver.find_element(By.NAME, 'nama').clear()
    driver.find_element(By.NAME, 'nama').send_keys('Tes Otomatis')
    time.sleep(2)
    driver.find_element(By.NAME, 'email').clear()
    driver.find_element(By.NAME, 'email').send_keys(unique_email)
    time.sleep(2)
    driver.find_element(By.NAME, 'pekerjaan').clear()
    driver.find_element(By.NAME, 'pekerjaan').send_keys('Mahasiswa')
    time.sleep(2)
    driver.find_element(By.NAME, 'password').clear()
    driver.find_element(By.NAME, 'password').send_keys('tes12345')
    time.sleep(2)
    driver.find_element(By.NAME, 'confirm_password').clear()
    driver.find_element(By.NAME, 'confirm_password').send_keys('tes12345')
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    if '/login' in driver.current_url:
        log_to_file("Register", "Berhasil (Redirect ke login)")
    else:
        log_to_file("Register", "Gagal (Tidak redirect ke login)")
except Exception as e:
    log_to_file("Register", f"Error: {str(e)}")

### === LOGIN SECTION === ###
try:
    driver.get('http://127.0.0.1:8000/login')

    driver.find_element(By.NAME, 'email').send_keys(unique_email)
    time.sleep(2)
    driver.find_element(By.NAME, 'password').send_keys('tes12345')
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)
    current_url = driver.current_url

    if '/dashboard' in current_url or '/peserta_dashboard' in current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", "Gagal (Tidak redirect ke dashboard)")
except Exception as e:
    log_to_file("Login", f"Error: {str(e)}")

### === LOGOUT SECTION === ###
try:
    logout_link = driver.find_element(By.LINK_TEXT, 'Logout')
    logout_link.click()
    time.sleep(2)

    if '/login' in driver.current_url:
        log_to_file("Logout", "Berhasil (Redirect ke login)")
    else:
        log_to_file("Logout", "Gagal (Tidak redirect ke login)")
except Exception as e:
    log_to_file("Logout", f"Error: {str(e)}")

time.sleep(5)
driver.quit()
