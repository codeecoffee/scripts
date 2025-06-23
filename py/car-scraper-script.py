import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re

def extract_cargurus_data(driver):
    """Extract car data from CarGurus page"""
    data = {}
    
    try:
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Get URL
        data['URL'] = driver.current_url
        
        # Get year - usually in the title
        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-cg-ft="vdp-listing-title"]')))
            title_text = title.text
            year_match = re.search(r'\b(19|20)\d{2}\b', title_text)
            data['Year'] = year_match.group() if year_match else 'N/A'
        except:
            data['Year'] = 'N/A'
        
        # Get price
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, '[data-cg-ft="vdp-price"]')
            data['Price'] = price_elem.text
        except:
            try:
                price_elem = driver.find_element(By.CLASS_NAME, 'cg-dealFinder-priceAndRatings-price')
                data['Price'] = price_elem.text
            except:
                data['Price'] = 'N/A'
        
        # Get mileage
        try:
            mileage_elem = driver.find_element(By.XPATH, "//span[contains(text(), 'Mileage')]/following-sibling::span")
            data['Mileage'] = mileage_elem.text
        except:
            try:
                # Alternative approach
                specs = driver.find_elements(By.CSS_SELECTOR, '.cg-listingDetail-specs-spec')
                for spec in specs:
                    if 'miles' in spec.text.lower():
                        data['Mileage'] = spec.text
                        break
                else:
                    data['Mileage'] = 'N/A'
            except:
                data['Mileage'] = 'N/A'
        
        # Get fuel type
        try:
            fuel_elem = driver.find_element(By.XPATH, "//span[contains(text(), 'Fuel type')]/following-sibling::span")
            data['Fuel Type'] = fuel_elem.text
        except:
            try:
                # Look in specs section
                specs = driver.find_elements(By.CSS_SELECTOR, '.cg-listingDetail-specs-spec')
                for spec in specs:
                    if 'gas' in spec.text.lower() or 'diesel' in spec.text.lower() or 'electric' in spec.text.lower() or 'hybrid' in spec.text.lower():
                        data['Fuel Type'] = spec.text
                        break
                else:
                    data['Fuel Type'] = 'N/A'
            except:
                data['Fuel Type'] = 'N/A'
        
        # Get location
        try:
            location_elem = driver.find_element(By.CSS_SELECTOR, '[data-cg-ft="dealer-location"]')
            data['Location'] = location_elem.text
        except:
            try:
                # Alternative approach
                dealer_info = driver.find_element(By.CSS_SELECTOR, '.cg-dealerInfo-address')
                data['Location'] = dealer_info.text
            except:
                data['Location'] = 'N/A'
        
    except Exception as e:
        print(f"Error extracting CarGurus data: {e}")
        
    return data

def extract_cars_com_data(driver):
    """Extract car data from Cars.com page"""
    data = {}
    
    try:
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Get URL
        data['URL'] = driver.current_url
        
        # Get year - usually in the title
        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.listing-title')))
            title_text = title.text
            year_match = re.search(r'\b(19|20)\d{2}\b', title_text)
            data['Year'] = year_match.group() if year_match else 'N/A'
        except:
            data['Year'] = 'N/A'
        
        # Get price
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, '.primary-price')
            data['Price'] = price_elem.text
        except:
            try:
                price_elem = driver.find_element(By.CSS_SELECTOR, 'span[class*="price"]')
                data['Price'] = price_elem.text
            except:
                data['Price'] = 'N/A'
        
        # Get mileage
        try:
            mileage_elem = driver.find_element(By.XPATH, "//dt[contains(text(), 'Mileage')]/following-sibling::dd")
            data['Mileage'] = mileage_elem.text
        except:
            try:
                # Alternative approach
                basics = driver.find_elements(By.CSS_SELECTOR, '.fancy-description-list dd')
                for i, basic in enumerate(basics):
                    if i > 0 and 'mi' in basic.text:
                        data['Mileage'] = basic.text
                        break
                else:
                    data['Mileage'] = 'N/A'
            except:
                data['Mileage'] = 'N/A'
        
        # Get fuel type
        try:
            fuel_elem = driver.find_element(By.XPATH, "//dt[contains(text(), 'Fuel Type')]/following-sibling::dd")
            data['Fuel Type'] = fuel_elem.text
        except:
            try:
                # Look for MPG info which often indicates fuel type
                mpg_elem = driver.find_element(By.XPATH, "//dt[contains(text(), 'MPG')]/following-sibling::dd")
                data['Fuel Type'] = 'Gasoline'  # Default if MPG is shown
            except:
                data['Fuel Type'] = 'N/A'
        
        # Get location
        try:
            dealer_elem = driver.find_element(By.CSS_SELECTOR, '.dealer-address')
            data['Location'] = dealer_elem.text.replace('\n', ', ')
        except:
            try:
                # Alternative approach
                location_elem = driver.find_element(By.CSS_SELECTOR, '[data-linkname="dealer-name"]')
                parent = location_elem.find_element(By.XPATH, '..')
                location_text = parent.text.split('\n')
                if len(location_text) > 1:
                    data['Location'] = location_text[1]
                else:
                    data['Location'] = 'N/A'
            except:
                data['Location'] = 'N/A'
        
    except Exception as e:
        print(f"Error extracting Cars.com data: {e}")
        
    return data

def main():
    # Connect to existing browser session
    # You'll need to start Chrome with debugging enabled:
    # chrome.exe --remote-debugging-port=9222
    
    try:
        # Option 1: Connect to existing Chrome instance
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        
    except:
        print("Could not connect to existing Chrome instance.")
        print("Please start Chrome with: chrome --remote-debugging-port=9222")
        print("Or uncomment the code below to use a new browser instance.")
        
        # Option 2: Create new browser instance (uncomment if needed)
        # driver = webdriver.Chrome()
        # print("Please open your CarGurus and Cars.com tabs, then press Enter to continue...")
        # input()
        return
    
    all_car_data = []
    
    try:
        # Get all open tabs
        original_window = driver.current_window_handle
        all_windows = driver.window_handles
        
        print(f"Found {len(all_windows)} open tabs")
        
        # Iterate through all tabs
        for window in all_windows:
            driver.switch_to.window(window)
            time.sleep(1)  # Give time for page to be active
            
            current_url = driver.current_url
            print(f"Checking: {current_url}")
            
            # Check if it's a CarGurus detail page
            if 'cargurus.com' in current_url and '/Cars/inventorylisting/' in current_url:
                print("Found CarGurus listing")
                car_data = extract_cargurus_data(driver)
                if car_data:
                    all_car_data.append(car_data)
                    
            # Check if it's a Cars.com detail page
            elif 'cars.com' in current_url and '/vehicledetail/' in current_url:
                print("Found Cars.com listing")
                car_data = extract_cars_com_data(driver)
                if car_data:
                    all_car_data.append(car_data)
        
        # Switch back to original window
        driver.switch_to.window(original_window)
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    # Create DataFrame and save to Excel
    if all_car_data:
        df = pd.DataFrame(all_car_data)
        
        # Reorder columns
        column_order = ['Year', 'Mileage', 'Fuel Type', 'Price', 'Location', 'URL']
        columns_present = [col for col in column_order if col in df.columns]
        df = df[columns_present]
        
        # Save to Excel
        filename = 'car_listings.xlsx'
        df.to_excel(filename, index=False)
        print(f"\nData saved to {filename}")
        print(f"Total cars scraped: {len(all_car_data)}")
        
        # Display the data
        print("\nScraped data:")
        print(df.to_string())
    else:
        print("\nNo car data was extracted. Make sure you have CarGurus or Cars.com detail pages open.")
    
    # Don't close the browser since we're using an existing session
    # driver.quit()

if __name__ == "__main__":
    main()