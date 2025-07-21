from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def log_to_file(fitur, status, keterangan=""):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Pengujian-Konfirmasi-Transaksi-Admin.txt", "a", encoding="utf-8") as file:
        file.write(f"{fitur} - {current_datetime} - Status: {status} - {keterangan}\n")

driver = webdriver.Chrome()

try:
    # 1. Login Admin
    driver.get("http://127.0.0.1:8000/login-admin")
    driver.find_element(By.NAME, "email").send_keys("cristov@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)

    if "/admin-dashboard" in driver.current_url or "/dashboard" in driver.current_url:
        log_to_file("Login Admin", "Berhasil")
    else:
        log_to_file("Login Admin", "Gagal", f"Tetap di {driver.current_url}")
        driver.quit()
        exit()

    # 2. Akses Halaman Transaksi
    driver.get("http://127.0.0.1:8000/transaksi/")
    time.sleep(2)

    # 3. Cari baris yang belum dikonfirmasi (❌)
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    target_row = None
    transaksi_id = None

    for row in rows:
        if '✘' in row.text or '❌' in row.text or '\u274c' in row.text:
            try:
                # Ekstrak ID dari atribut data-modal-target="crud-modal1-5"
                edit_button = row.find_element(By.XPATH, './/button[contains(@data-modal-target, "crud-modal1-")]')
                modal_target = edit_button.get_attribute("data-modal-target")  # crud-modal1-5
                transaksi_id = modal_target.split("-")[-1]
                target_row = row
                break
            except:
                continue

    if not target_row:
        log_to_file("Cari Transaksi Belum Dikonfirmasi", "Gagal", "Tidak ditemukan transaksi dengan ❌")
        driver.quit()
        exit()

    log_to_file("Cari Transaksi Belum Dikonfirmasi", "Berhasil", f"Transaksi ID: {transaksi_id}")

    # 4. Klik Edit (buka modal)
    edit_button = target_row.find_element(By.XPATH, f'.//button[@data-modal-target="crud-modal1-{transaksi_id}"]')
    edit_button.click()

    wait = WebDriverWait(driver, 10)

    # 5. Tunggu modal muncul dan pastikan checkbox ada
    modal = wait.until(EC.visibility_of_element_located((By.ID, f"crud-modal1-{transaksi_id}")))
    checkbox = wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@id="crud-modal1-{transaksi_id}"]//input[@name="is_paid"]')))

    # Pastikan modal terlihat dan checkbox visible dulu
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[@id="crud-modal1-{transaksi_id}"]//input[@name="is_paid"]')))

    # Scroll ke checkbox (opsional jika tertutup header modal)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
    time.sleep(0.5)

    # Klik checkbox hanya jika belum dicentang
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
    # 6. Klik tombol "Konfirmasi"
    submit_button = driver.find_element(By.XPATH, f'//div[@id="crud-modal1-{transaksi_id}"]//button[contains(text(), "Konfirmasi")]')
    submit_button.click()
    time.sleep(2)

    # 7. Verifikasi perubahan status ke centang
    driver.get("http://127.0.0.1:8000/transaksi/")
    time.sleep(2)

    updated = False
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    for row in rows:
        if "Tes Otomatis" in row.text and "✔" in row.text:
            updated = True
            break

    if updated:
        log_to_file("Konfirmasi Transaksi", "Berhasil", "Status berhasil diubah ke centang (✔)")
    else:
        log_to_file("Konfirmasi Transaksi", "Gagal", "Status belum berubah")

except Exception as e:
    log_to_file("Error Umum", "Gagal", f"Message: {str(e)}")

driver.quit()
