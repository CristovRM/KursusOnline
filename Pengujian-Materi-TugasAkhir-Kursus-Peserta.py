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
    with open("Pengujian-Full-Kursus.txt", "a") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

try:
    # === LOGIN PESERTA ===
    driver.get("http://127.0.0.1:8000/login")
    driver.find_element(By.NAME, 'email').send_keys('tes1753031227@gmail.com')
    driver.find_element(By.NAME, 'password').send_keys('tes12345')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)  # delay setelah login

    if "/student/dashboard" in driver.current_url or "/peserta/dashboard" in driver.current_url:
        log_to_file("Login", "Berhasil")
    else:
        log_to_file("Login", "Gagal", f"Redirect ke: {driver.current_url}")

    # === MASUK MENU DASHBOARD ===
    driver.get("http://127.0.0.1:8000/student/dashboard")
    time.sleep(2)
    if "Dashboard" in driver.page_source:
        log_to_file("Dashboard", "Berhasil")
    else:
        log_to_file("Dashboard", "Gagal", "Menu dashboard tidak muncul")
    time.sleep(2)

    # === KLIK MYCOURSE ===
    driver.find_element(By.LINK_TEXT, "MyCourse").click()
    time.sleep(3)

    if "Kursus" in driver.page_source or "popo1" in driver.page_source:
        log_to_file("MyCourse", "Berhasil", "Daftar kursus muncul")
    else:
        log_to_file("MyCourse", "Gagal", "Daftar kursus tidak ditemukan")
    time.sleep(2)

    # === BUKA KURSUS TERTENTU ===
    driver.get("http://127.0.0.1:8000/student/kursus/16/")
    time.sleep(3)
    if "Materi" in driver.page_source:
        log_to_file("Lihat Kursus", "Berhasil")
    else:
        log_to_file("Lihat Kursus", "Gagal", "Konten kursus tidak muncul")
    time.sleep(2)

    # === LIHAT MATERI ===
    try:
        materi_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Lihat Materi")]')))
        time.sleep(1)
        pdf_url = materi_link.get_attribute('href')

        # Buka PDF di tab baru
        driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)
        time.sleep(3)

        # Pindah ke tab PDF
        driver.switch_to.window(driver.window_handles[1])
        log_to_file("Lihat Materi", "Berhasil", f"PDF dibuka: {pdf_url}")
        time.sleep(2)

        # Tutup tab PDF
        driver.close()
        time.sleep(1)

        # Pindah balik ke tab utama (kursus)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

    except Exception as e:
        log_to_file("Lihat Materi", "Gagal", str(e))
        time.sleep(2)

    # === LIHAT TUGAS AKHIR ===
    try:
        tugas_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Lihat Tugas")]')))
        time.sleep(1)
        pdf_url = tugas_link.get_attribute('href')

        # Buka PDF di tab baru
        driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)
        time.sleep(3)

        # Pindah ke tab PDF
        driver.switch_to.window(driver.window_handles[1])
        log_to_file("Lihat Tugas", "Berhasil", f"PDF dibuka: {pdf_url}")
        time.sleep(2)

        # Tutup tab PDF
        driver.close()
        time.sleep(1)

        # Pindah balik ke tab utama (kursus)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

    except Exception as e:
        log_to_file("Lihat Tugas", "Gagal", str(e))
        time.sleep(2)

    # === KUMPULKAN TUGAS AKHIR ===
    try:
        kumpul_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[contains(text(), "Kumpulkan Tugas")]')
        ))
        time.sleep(1)
        kumpul_link.click()
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.NAME, 'file_url')))
        time.sleep(1)

        tugas_path = os.path.abspath("tugas_akhir_dummy.pdf")  # Pastikan file ada di folder yang sama
        driver.find_element(By.NAME, 'file_url').send_keys(tugas_path)
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[contains(text(), "Kirim Jawaban")]').click()
        time.sleep(3)

        if "berhasil" in driver.page_source.lower():
            log_to_file("Kumpulkan Tugas Akhir", "Berhasil", "Tugas berhasil dikirim")
        else:
            log_to_file("Kumpulkan Tugas Akhir", "Gagal", "Tidak ada notifikasi sukses")
        time.sleep(2)
    except Exception as e:
        log_to_file("Kumpulkan Tugas Akhir", "Gagal", str(e))
        time.sleep(2)

    # === LIHAT FILE YANG DIKIRIM ===
    try:
        lihat_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Lihat File yang Dikirim")]')))
        time.sleep(1)
        pdf_url = lihat_link.get_attribute('href')

        # Buka PDF di tab baru
        driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)
        time.sleep(3)

        # Pindah ke tab PDF
        driver.switch_to.window(driver.window_handles[1])
        log_to_file("Lihat File yang Dikirim", "Berhasil", f"PDF dibuka: {pdf_url}")
        time.sleep(2)

        # Tutup tab PDF
        driver.close()
        time.sleep(1)

        # Pindah balik ke tab utama (kursus)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        log_to_file("Lihat File yang Dikirim", "Gagal", str(e))
        time.sleep(2)

except Exception as e:
    log_to_file("Error Umum", "Gagal", str(e))
    time.sleep(2)

finally:
    time.sleep(2)
    driver.quit()
