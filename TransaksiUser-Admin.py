from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def log_to_file(fitur, status, keterangan=""):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Pembelian-Kursus.txt", "a") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

try:
    # === LOGIN ===
    driver.get("http://127.0.0.1:8000/login")
    driver.find_element(By.NAME, 'email').send_keys('tes1753031227@gmail.com')
    driver.find_element(By.NAME, 'password').send_keys('tes12345')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)
    
    if "/student/dashboard" in driver.current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", "Gagal", f"Redirect: {driver.current_url}")

    # === PILIH KURSUS ===
    driver.get("http://127.0.0.1:8000/student/kursus/16/")  # ID kursus sesuaikan
    beli_kursus_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "beli kursus")))
    beli_kursus_link.click()

    # === FORM PEMBELIAN ===
    driver.find_element(By.NAME, 'telepon').send_keys("081234567890")
    metode = Select(driver.find_element(By.NAME, 'metode'))
    metode.select_by_index(1)  # index 1 = opsi pertama selain 'Pilih Metode'

    # === UNGGAH FILE ===
    bukti_path = os.path.abspath("bukti_pembayaran_dummy.jpg")  # Pastikan file ada di folder yang sama
    driver.find_element(By.NAME, 'bukti').send_keys(bukti_path)

    driver.find_element(By.XPATH, '//button[contains(text(),"Beli Kursus")]').click()
    time.sleep(2)

    # Tunggu sampai elemen alert sukses muncul di halaman
    alert_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bg-green-600"))
    )

    alert_text = alert_elem.text.lower()

    if "transaksi berhasil dikirim" in alert_text and "menunggu persetujuan admin" in alert_text:
        log_to_file("Pembelian Kursus", "Berhasil", "Tampil alert sukses & redirect ke dashboard")
    else:
        log_to_file("Pembelian Kursus", "Gagal", f"Alert tidak sesuai. Isi: {alert_text}")

except Exception as e:
    log_to_file("Pembelian Kursus", "Gagal", f"Alert tidak muncul - Error: {str(e)}")

finally:
    time.sleep(2)
    driver.quit()
