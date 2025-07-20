from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def log_to_file(fitur, status):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('Pengujian-Login-Logout-Pengajar.txt', 'a') as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status}\n")
        
### === LOGIN SECTION === ###
try:
    driver.get('http://127.0.0.1:8000/login')

    driver.find_element(By.NAME, 'email').send_keys('pascol@gmail.com')
    time.sleep(2)
    driver.find_element(By.NAME, 'password').send_keys('test123')
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)
    current_url = driver.current_url

    if '/dashboard' in current_url or '/dashboard_pengajar' in current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", "Gagal (Tidak redirect ke dashboard)")
except Exception as e:
    log_to_file("Login", f"Error: {str(e)}")

### === LOGOUT SECTION === ###
try:
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Logout'))
    )
    logout_link.click()
    time.sleep(2)

    current_url = driver.current_url
    page_source = driver.page_source.lower()
    print("Redirect setelah logout:", current_url)

    # Tanpa cek URL, hanya cek apakah login form muncul
    if (
        'input type="email"' in page_source or
        'name="email"' in page_source or
        'login' in page_source or
        'masuk' in page_source
    ):
        log_to_file("Logout", "Berhasil (Login form terdeteksi)")
    else:
        log_to_file("Logout", f"Gagal (Form login tidak ditemukan, redirect ke {current_url})")
except Exception as e:
    log_to_file("Logout", f"Error: {str(e)}")

driver.quit()

