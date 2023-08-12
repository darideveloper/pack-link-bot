import os
from time import sleep
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper

load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")
PARCEL_WEIGTH = os.getenv ("PARCEL_WEIGTH")
PARCEL_LENGTH = os.getenv ("PARCEL_LENGTH")
PARCEL_WIDTH = os.getenv ("PARCEL_WIDTH")
PARCEL_HEIGHT = os.getenv ("PARCEL_HEIGHT")

class PackLinkBot (): 
    
    def __init__ (self, driver:ChromDevWrapper):
        
        # Connect to chrome dev tools
        self.driver = driver
        
        self.selectors = {
            "menu_item": 'button[role="menuitem"]',
            "shipment": {
                "country": 'input[name="to.country"]',
                "post_code": 'input[name="to.postalCode"]',
                "next": 'button[type="submit"]',
                "weigth": 'input[name="parcels.0.weight"]',
                "lenght": 'input[name="parcels.0.length"]',
                "width": 'input[name="parcels.0.width"]',
                "height": 'input[name="parcels.0.height"]',
            },
            "service": {
                "button": ".service-list-wrapper article button"
            }
        }
        
    def __select_item__ (self, selector:str, value:str) -> bool:
        """ Select an item in a dropdown menu

        Args:
            selector (str): css selector of the dropdown menu
            value (str): value to select
        
        Returns: 
            bool: True if option was selected
        """
        
        # Click dropdown menu and write value
        self.driver.click (selector)
        sleep (1)
        self.driver.send_data (selector, value)
        sleep (1)
        
        # Validate if optiopn exists
        option = self.driver.get_text (self.selectors ["menu_item"])
        if option == "No results found":
            self.set_prop (selector, "value", "")
            return False
        
        self.driver.click (self.selectors ["menu_item"])
        return True
        
    def create_draft (self, country:str, first_name:str, last_name:str, street:str, 
                     city:str, zip_code:str, phone:str, email:str) -> bool: 
        """ Create a draft in pack link pro

        Args:
            country (str): client country 
            first_name (str): client first name
            last_name (str): client last name
            street (str): client street
            city (str): client city
            zip_code (str): client zip code
            phone (str): client phone
            email (str): client email

        Returns:
            bool: True if draft was created
        """
                        
        self.driver.set_page ("https://pro.packlink.com/private/shipments/create/info")
        
        # Select country and post code
        current_step = "shipping details"
        country_found = self.__select_item__ (self.selectors ["shipment"]["country"], country)
        zip_code_found = self.__select_item__ (self.selectors ["shipment"]["post_code"], zip_code)
        if not zip_code_found:
            zip_code_found = self.driver.send_data (self.selectors ["shipment"]["post_code"], city)
        
        # Validate if country and post code were found
        if not country_found:
            error = f"country not found for {country}"
            self.summary.append (["error", current_step, error])
            return False
        
        if not zip_code_found:
            error = f"zip code and city not found for {zip_code, city}"
            self.summary.append (["error", current_step, error])
            return False
        
        # Write parcel data (if its required)
        current_weight = self.driver.get_prop (self.selectors ["shipment"]["weigth"], "value")
        if not current_weight:
            self.driver.send_data (self.selectors ["shipment"]["weigth"], PARCEL_WEIGTH)
            self.driver.send_data (self.selectors ["shipment"]["lenght"], PARCEL_LENGTH)
            self.driver.send_data (self.selectors ["shipment"]["width"], PARCEL_WIDTH)
            self.driver.send_data (self.selectors ["shipment"]["height"], PARCEL_HEIGHT)
        
        self.driver.click (self.selectors ["shipment"]["next"])
        sleep (2)
        
        # Select service
        current_step = "choose a service"
        self.driver.click (self.selectors ["service"]["button"])
        sleep (2)
        