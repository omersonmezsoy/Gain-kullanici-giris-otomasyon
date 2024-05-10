from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Chrome seçeneklerini ayarlama
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1")
chrome_options.add_argument("--window-size=375,812")  # iPhone XR ekran boyutu
chrome_options.add_argument("--disable-notifications")  # Çerez bildirimi gibi pop-up'ları engelleme

# Chrome sürücüsünü başlatma
driver = webdriver.Chrome(options=chrome_options)

# Web sitesine gir
driver.get("http://www.gain.tv")

# Url yi kontrol et
link = driver.current_url
assert "gain.tv" in link, "HATA: Sayfada değiliz."

# Başlığı kontrol et
baslik = driver.title
assert "GAİN" in baslik, "HATA: Başlık doğru değil."

# Kullanıcı girişi

# 1 - Herhangi bir kullanıcı adı veya şifre girmeden dene
# Beklenen : "E-posta adresi girin. Şifre girin."  Link : https://www.gain.tv/giris-yap

driver.get("https://www.gain.tv/giris-yap")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn:nth-child(6)"))).click()
mesaj_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".validation-summary-errors")))
mesaj = mesaj_element.text.replace("\n", " ")
assert "E-posta adresi girin. Şifre girin." in mesaj, "HATA: Boş kullanıcı adı ve şifre işlevsel değil."

# 2 - Yanlış kullanıcı adı yanlış şifre dene
# Beklenen : "E-posta adresini hatalı girdin."  Link : https://www.gain.tv/giris-yap

driver.get("https://www.gain.tv/giris-yap")
driver.find_element(By.ID, "Email").send_keys("blabla")
driver.find_element(By.ID, "Password").send_keys("heyo")
driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(6)").click()
mesaj1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".validation-summary-errors"))).text
assert "E-posta adresini hatalı girdin." in mesaj1, "HATA: Yanlış kullanıcı adı ve şifre işlevsel değil."

# 3 - Yanlış kullanıcı adı doğru şifre dene
# Beklenen : "E-posta adresini hatalı girdin."  Link : https://www.gain.tv/giris-yap

driver.get("https://www.gain.tv/giris-yap")
driver.find_element(By.ID, "Email").send_keys("blabla")
driver.find_element(By.ID, "Password").send_keys("_Tcjq2a_a39,+JW")
driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(6)").click()
mesaj2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".validation-summary-errors"))).text
assert "E-posta adresini hatalı girdin." in mesaj2, "HATA: Yanlış kullanıcı adı ve doğru şifre işlevsel değil."

# 4 - Yanlış şifre doğru kullanıcı adı dene
# Beklenen : "E-posta adresi veya şifreni hatalı girdin. Tekrar deneyin veya “Şifreni mi unuttun?” linkine tıklayın."  Link : https://www.gain.tv/giris-yap

driver.get("https://www.gain.tv/giris-yap")
driver.find_element(By.ID, "Email").send_keys("omersonmezsoy@gmail.com")
driver.find_element(By.ID, "Password").send_keys("heyoheyo")
driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(6)").click()
mesaj3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".validation-summary-errors > ul:nth-child(1) > li:nth-child(1)"))).text
assert "E-posta adresi veya şifreni hatalı girdin. Tekrar deneyin veya “Şifreni mi unuttun?” linkine tıklayın." in mesaj3, "HATA: Doğru kullanıcı adı yanlış şifre işlevsel değil."

# 5 - Doğru kullanıcı adı doğru şifre

driver.get("https://www.gain.tv/giris-yap")
driver.find_element(By.ID, "Email").send_keys("omersonmezsoy@gmail.com")
driver.find_element(By.ID, "Password").send_keys("_Tcjq2a_a39,+JW")
driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(6)").click()

wait = WebDriverWait(driver, 10)

giris_linki = driver.current_url
assert "gain.tv/kesfet" in giris_linki, "HATA: Doğru kullanıcı adı ve şifre işlevsel değil."

driver.quit()
