# Dynamic Image Scraper

A robust Python-based image scraper specifically designed to bypass advanced bot protections (like DataDome and Cloudflare) and download high-quality images from dynamic, JavaScript-heavy websites such as **Shutterstock**.

## Demo 
[![Watch the demo](DEMO.gif)](DEMO.gif)

## Features

-   **Anti-Bot Bypass**: Uses `undetected-chromedriver` to mimic real human browsing behavior.
-   **Dynamic Content Support**: Executes JavaScript and scrolls the page to trigger lazy-loading of images.
-   **High Quality Prioritization**: Automatically scans `srcset` and `data-src` attributes to find the highest resolution versions of images.
-   **Human-Like Interaction**: Includes randomized delays and gradual scrolling to avoid detection.
-   **Manual Intervention Support**: If a CAPTCHA appears, the script pauses and allows you to solve it manually in the browser window before continuing.
-   **Configurable Downloads**: Specify exactly how many images you want to download.

## Prerequisites

-   **Python 3.10+**
-   **Google Chrome Browser** installed on your system.
-   **Linux/Windows/macOS** (Desktop environment required for CAPTCHA solving).

## Installation

1. **Clone or download** this repository to your local machine.

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the scraper:
   ```bash
   python image_scraper.py
   ```

2. **Enter the URL**: Paste the Shutterstock search result URL or any other image-heavy page.
   - *Example*: `https://www.shutterstock.com/search/nature`

3. **Enter Max Images**: Specify the number of images to download (e.g., `100`).

4. **CAPTCHA Solving**: 
   - A Chrome window will open. If you see a "Verify you are human" challenge, simply click it in the browser window.
   - The script will detect the "Passed" state and automatically begin downloading.



## Troubleshooting

- **No Images Found**: If the script finds 0 images, check the `debug_results.png` screenshot. If it shows a CAPTCHA, make sure you solved it in the pop-up window.
- **Chrome Version Mismatch**: This script is configured for Chrome version 144. If your Chrome is newer/older, update the `version_main` parameter in the `setup_driver` function within `image_scraper.py`.
- **Headless Mode**: The script currently runs with a visible window to bypass anti-bot systems. Do not minimize the window while it is "Establishing session".

---
*Note: This tool is for educational purposes. Always respect the robots.txt and Terms of Service of the websites you scrape.*
