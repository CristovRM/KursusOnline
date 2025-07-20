from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def log_to_file(fitur, status, keterangan=""):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Pengajar.txt", "a") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

try:
    # === LOGIN SEBAGAI PENGAJAR ===
    driver.get("http://127.0.0.1:8000/login")
    driver.find_element(By.NAME, 'email').send_keys('romi@gmail.com')
    driver.find_element(By.NAME, 'password').send_keys('romi123')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)

    if "/teacher/dashboard" in driver.current_url or "/pengajar/dashboard" in driver.current_url:
        log_to_file("Login Pengajar", "Berhasil")
    else:
        log_to_file("Login Pengajar", "Gagal", f"Redirect ke: {driver.current_url}")

    # === MASUK KE SALAH SATU KURSUS ===
    driver.get("http://127.0.0.1:8000/teacher/my-course/10/")
    time.sleep(2)
    if "Materi" in driver.page_source:
        log_to_file("Masuk Kursus", "Berhasil")
    else:
        log_to_file("Masuk Kursus", "Gagal", "Halaman kursus tidak ditemukan")

    # === KLIK TOMBOL TAMBAH MATERI ===
    driver.find_element(By.XPATH, '//a[contains(text(), "Tambah Materi")]').click()
    time.sleep(2)

    # === ISI FORM TAMBAH MATERI ===
    wait.until(EC.presence_of_element_located((By.NAME, 'judul')))
    driver.find_element(By.NAME, 'judul').send_keys('Materi Otomatis')
    driver.find_element(By.NAME, 'deskripsi').send_keys('Ini adalah materi otomatis dari selenium')

    # Pilih tipe materi
    tipe_select = driver.find_element(By.NAME, 'tipe_materi')
    for option in tipe_select.find_elements(By.TAG_NAME, 'option'):
        if option.text.lower() == 'modul':
            option.click()
            break

    driver.find_element(By.NAME, 'urutan').send_keys('2')

    # Upload file
    file_path = os.path.abspath("modul_dummy.pdf")  # Pastikan file ini ada
    driver.find_element(By.NAME, 'file_url').send_keys(file_path)
    time.sleep(2)

    # Klik submit
    driver.find_element(By.XPATH, '//button[contains(text(), "Simpan")]').click()
    time.sleep(3)

    if "Materi Otomatis" in driver.page_source:
        log_to_file("Tambah Materi", "Berhasil", "Materi muncul di list")
    else:
        log_to_file("Tambah Materi", "Gagal", "Materi tidak muncul setelah submit")

except Exception as e:
    log_to_file("Error Umum", "Gagal", str(e))

# === TAMBAH TUGAS AKHIR (Final Project) ===
try:
    # 1) Klik tombol “Tambah Tugas Akhir”
    driver.find_element(By.XPATH, '//a[contains(text(), "Tambah Tugas Akhir")]').click()
    time.sleep(2)

    # 2) Isi form
    wait.until(EC.presence_of_element_located((By.NAME, 'judul')))
    driver.find_element(By.NAME, 'judul').send_keys('Tugas Akhir Otomatis')
    driver.find_element(By.NAME, 'deskripsi').send_keys(
        'Silakan kerjakan tugas akhir yang dibuat otomatis via Selenium'
    )

    # Upload file
    file_path = os.path.abspath("modul_ta_dummy.pdf")  # Pastikan file ini ada
    driver.find_element(By.NAME, 'file_url').send_keys(file_path)
    time.sleep(2)

    # 4) Submit
    driver.find_element(By.XPATH, '//button[contains(text(), "Simpan")]').click()
    time.sleep(3)

    if "Tugas Akhir Otomatis" in driver.page_source:
        log_to_file("Tambah Tugas Akhir", "Berhasil", "Tugas Akhir muncul di list")
    else:
        log_to_file("Tambah Tugas Akhir", "Gagal", "Tugas Akhir tidak muncul setelah submit")

except Exception as e:
    log_to_file("Tambah Tugas Akhir", "Gagal", str(e))

finally:
    time.sleep(2)
    driver.quit()