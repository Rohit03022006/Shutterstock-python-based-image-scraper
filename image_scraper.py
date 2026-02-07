import os
import time
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup undetected Chrome driver"""
    options = uc.ChromeOptions()
   
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,1024")
    
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    try:
        # User has Chrome 144
        driver = uc.Chrome(options=options, version_main=144)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None

def download_image(url, folder, count):
    """Download a single image from URL"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.shutterstock.com/"
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            ext = 'jpg'
            # Simple extension check
            clean_url = url.split('?')[0].lower()
            if clean_url.endswith('.png'): ext = 'png'
            elif clean_url.endswith('.webp'): ext = 'webp'
            elif clean_url.endswith('.gif'): ext = 'gif'
            
            filename = os.path.join(folder, f"img_{count}.{ext}")
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except:
        pass
    return False

def main():
    url = input("Enter URL: ").strip()
    if not url:
        print("Please enter a valid URL")
        return

    max_images_str = input("Enter max images to download (default 100): ").strip()
    max_images = int(max_images_str) if max_images_str.isdigit() else 100

    folder = "images"
    os.makedirs(folder, exist_ok=True)
    
    print("Initializing browser (Bypass mode)...")
    driver = setup_driver()
    
    if not driver:
        print("Failed to initialize browser.")
        return

    try:
        print("Establishing session...")
        driver.get("https://www.google.com")
        time.sleep(random.uniform(1, 2))
        
        print(f"Accessing {url}...")
        driver.get(url)
        
        print("Verifying browser (if you see a CAPTCHA, please solve it)...")
        time.sleep(10) 
        
        print(f"Page Title: {driver.title}")
        
        if "shutterstock" not in driver.title.lower() or "challenge" in driver.page_source.lower():
            print("\n!!! ACTION REQUIRED !!!")
            print("The website is showing a 'Human Verification' challenge.")
            print("Please solve it in the browser window that just opened.")
            print("Waiting for you to solve it (60 seconds max)...")
           
            for _ in range(60):
                if "shutterstock" in driver.title.lower() and "challenge" not in driver.page_source.lower():
                    print("Challenge passed! Continuing...")
                    break
                time.sleep(1)
            else:
                print("Timed out waiting for challenge solution.")
        
        print("Scrolling to load high-quality images...")
        total_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, 6):
            scroll_to = total_height * (i / 5)
            driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            time.sleep(random.uniform(1.5, 3))
            
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        img_tags = soup.find_all("img")
        image_urls = []
        
        print(f"Total images found on page: {len(img_tags)}")
        
        if len(img_tags) == 0:
            print("No images found. Saving debug info for troubleshooting...")
            with open("debug_results.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.save_screenshot("debug_results.png")
            print("Check debug_results.png and debug_results.html")
        
       
        for img in img_tags:
            src = img.get("src")
            srcset = img.get("srcset")
            data_src = img.get("data-src")
            
            potential_urls = []
            if srcset:
                urls = [u.strip().split(' ')[0] for u in srcset.split(',')]
                potential_urls.extend(urls)
            if data_src: potential_urls.append(data_src)
            if src: potential_urls.append(src)
                
            for p_url in potential_urls:
                if p_url and not p_url.startswith("data:"):
                    full_url = urljoin(url, p_url)
                    
                    if "asset" in full_url.lower() or "shutterstock.com/image-" in full_url.lower():
                         image_urls.append(full_url)
                    elif any(ext in full_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                         width = img.get("width")
                         if width and width.isdigit() and int(width) < 100:
                             continue
                         image_urls.append(full_url)

        image_urls = list(set(image_urls))
        print(f"Found {len(image_urls)} unique potential high-quality images")
        
        count = 0
        print(f"Starting download (limit {max_images})...")
        
        for i, img_url in enumerate(image_urls):
            if count >= max_images:
                break
            print(f"[{i+1}/{len(image_urls)}] Downloading image...", end="\r")
            if download_image(img_url, folder, count + 1):
                count += 1

                
        print(f"\n\nDone! Successfully downloaded {count} images to '{folder}' folder.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
