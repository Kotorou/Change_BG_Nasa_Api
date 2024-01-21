import requests
import os
from urllib.request import urlretrieve
import ctypes
from datetime import datetime, timedelta

def main(api_key):
    try:
        # Download NASA image for today
        image_filename = download_nasa_image(api_key)

        if image_filename:
            # Set desktop wallpaper
            set_wallpaper(image_filename)
        else:
            print("Failed to download the NASA image for today.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def download_nasa_image(api_key):
    try:
        # Get yesterday's date (to ensure the latest image is used)
        yesterday = datetime.now() - timedelta(days=1)
        formatted_date = yesterday.strftime("%Y-%m-%d")

        # NASA API URL for a specific date
        api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={formatted_date}'

        # Fetch astronomy picture of the day (APOD) data for yesterday
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()

        # Extract image URL
        image_url = data['url']

        # Download the image
        image_filename, _ = urlretrieve(image_url, os.path.basename(image_url))

        return image_filename
    except requests.exceptions.RequestException as re:
        print(f"Request to NASA API failed: {str(re)}")
    except Exception as e:
        print(f"An error occurred during image download: {str(e)}")

def set_wallpaper(image_filename):
    try:
        # Set the desktop wallpaper (platform-specific)
        if os.name == 'nt':  # Windows
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(image_filename), 3)
            print("Wallpaper set successfully.")
        else:
            print("Unsupported operating system for wallpaper setting.")
    except Exception as e:
        print(f"An error occurred while setting the wallpaper: {str(e)}")

if __name__ == "__main__":
    NASA_API_KEY = 'byezwFqoO1FLk4785DMziSERLL1ZWgE85ORIQbp4'
    main(NASA_API_KEY)
