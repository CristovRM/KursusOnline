from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def log_to_file(fitur, status):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('Pengujian-Login-Logout-Admin.txt', 'a') as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status}\n")

### === LOGIN SECTION === ###
try:
    driver.get('http://127.0.0.1:8000/login-admin')

    driver.find_element(By.NAME, 'email').send_keys('amin@gmail.com')
    time.sleep(1)
    driver.find_element(By.NAME, 'password').send_keys('amin123')
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)
    current_url = driver.current_url
    print("Redirect setelah login:", current_url)

    if '/dashboard' in current_url or '/admin_dashboard' in current_url or '/admin-dashboard' in current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", f"Gagal (Redirect ke {current_url})")

except Exception as e:
    log_to_file("Login", f"Error: {str(e)}")

### === LOGOUT SECTION === ###
try:
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Logout'))
    )
    logout_link.click()
    time.sleep(2)

    # Arahkan paksa ke halaman login
    driver.get("http://127.0.0.1:8000/login-admin")
    time.sleep(2)

    # Cek apakah input email tersedia
    email_fields = driver.find_elements(By.NAME, 'email')
    if len(email_fields) > 0:
        log_to_file("Logout", "Berhasil (Login form terdeteksi)")
    else:
        log_to_file("Logout", f"Gagal (Form login tidak ditemukan, redirect ke {driver.current_url})")

except Exception as e:
    log_to_file("Logout", f"Error: {str(e)}")
driver.quit()
