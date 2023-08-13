import os
from time import sleep
from dotenv import load_dotenv
from scraping.web_scraping import WebScraping
from scraping.web_scraping import Keys

load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")
PARCEL_WEIGTH = os.getenv ("PARCEL_WEIGTH")
PARCEL_LENGTH = os.getenv ("PARCEL_LENGTH")
PARCEL_WIDTH = os.getenv ("PARCEL_WIDTH")
PARCEL_HEIGHT = os.getenv ("PARCEL_HEIGHT")
CONTENT_SHIPPED = os.getenv ("CONTENT_SHIPPED")
RIST_SHIPMENT = os.getenv ("RIST_SHIPMENT") == "True"

class PackLinkBot (): 
    
    def __init__ (self, driver:WebScraping, summary:list):
        """ Create a draft for each commission

        Args:
            driver (ChromDevWrapper): chrome dev tools wrapper
            summary (list): summary of the process
            price (float): price of the service
        """
        
        
        # Connect to chrome dev tools
        self.driver = driver
        self.summary = summary
        
        self.shipping_price = 0
        self.price = 0
      
        self.selectors = {
            "menu_item": 'button[role="menuitem"]',
            "next": 'button[type="submit"]',
            "shipment": {
                "country": 'input[name="to.country"]',
                "post_code": 'input[name="to.postalCode"]',
                "weigth": 'input[name="parcels.0.weight"]',
                "lenght": 'input[name="parcels.0.length"]',
                "width": 'input[name="parcels.0.width"]',
                "height": 'input[name="parcels.0.height"]',
            },
            "service": {
                "button": ".service-list-wrapper article button",
                "price": ".service-list-wrapper article h2",
            },
            "address": {
                "first_name": 'input[name="to.firstName"]', 
                "last_name": 'input[name="to.lastName"]',
                "street": 'textarea[name="to.street1"]',
                "phone": 'input[name="to.phone"]',
                "email": 'input[name="to.email"]',
                "content_shipped": 'input[name="description"]',
                "content_value": 'input[name="value"]',
                "risk": 'input[value="NO_INSURANCE"]',
                "no-risk": 'input[value="NO_INSURANCE"]',
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
        self.driver.send_data (selector, value)
        sleep (1)
        
        # Validate if optiopn exists
        option = self.driver.get_text (self.selectors ["menu_item"])
        if option == "No results found":
            self.driver.set_attrib (selector, "value", "")
            return False
        
        self.driver.click (self.selectors ["menu_item"])
        return True
    
    def __shipping__ (self):
        """ Write data in shipping details section
        """
        
        # Selectors and step
        current_step = "shipment"
        current_selectors = self.selectors [current_step]
        self.driver.refresh_selenium ()
        
        # Select country and post code
        country_found = self.__select_item__ (current_selectors["country"], self.country)
        zip_code_found = self.__select_item__ (current_selectors["post_code"], self.zip_code)
        if not zip_code_found:
            zip_code_found = self.driver.send_data (current_selectors["post_code"], self.city)
        
        # Validate if country and post code were found
        if not country_found:
            error = f"country not found for {self.country}"
            self.summary.append (["error", current_step, error])
            raise Exception (error)
        
        if not zip_code_found:
            error = f"zip code and city not found for {self.zip_code, self.city}"
            self.summary.append (["error", current_step, error])
            raise Exception(error)
            
        # Write parcel data (if its required)
        current_weight = self.driver.get_attrib (current_selectors["weigth"], "value")
        if not current_weight:
            self.driver.send_data (current_selectors["weigth"], PARCEL_WEIGTH)
            self.driver.send_data (current_selectors["lenght"], PARCEL_LENGTH)
            self.driver.send_data (current_selectors["width"], PARCEL_WIDTH)
            self.driver.send_data (current_selectors["height"], PARCEL_HEIGHT)
        
        self.driver.click (self.selectors["next"])
        sleep (1)
            
    def __service__ (self):
        """ Select service and save price
        """
        
        # Selectors and step
        current_step = "service"
        current_selectors = self.selectors [current_step]
        self.driver.refresh_selenium ()
        
        self.shipping_price = self.driver.get_text (current_selectors["price"])
        button = self.driver.get_text (current_selectors["button"])
        
        if not self.shipping_price or not button:
            error = "services not found"
            self.summary.append (["error", "service", error])
            raise Exception(error)
        
        # Format price
        self.shipping_price = float (self.shipping_price.replace ("€", "").replace (",", "."))
        
        # Select service
        self.driver.click (current_selectors["button"])
        sleep (1)
        
    
    def __address__ (self):
        """ Write data in address section
        """
        
        # Selectors and step
        current_step = "address"
        current_selectors = self.selectors [current_step]
        self.driver.refresh_selenium ()
            
        # Format data
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "street": self.street,
        }
        
        # Main data
        for key, value in data.items ():
            
            # Delete old chars
            input_elem = self.driver.get_elem (current_selectors[key])
            input_text = self.driver.get_attrib (current_selectors[key], "value")
            if input_text:
                input_elem.send_keys(Keys.BACKSPACE * len(input_text))
                print ()
                      
            self.driver.send_data (current_selectors[key], value)
        
        # Content shipped
        content_shipped_found = self.__select_item__ (current_selectors["content_shipped"], CONTENT_SHIPPED)
        if not content_shipped_found:
            error = f"content shipped not found for {CONTENT_SHIPPED}"
            self.summary.append (["error", current_step, error])
            raise Exception(error)
        
        # Add content and price data
        data["content_value"] = str(self.price - self.shipping_price)
        
        
        # Risk option
        if RIST_SHIPMENT:
            self.driver.click_js (current_selectors["risk"])
        else:
            self.driver.click_js (current_selectors["no-risk"])
    
        # Submit form with js
        self.driver.click_js (self.selectors["next"])
        sleep (1)

    def create_draft (self, country:str, first_name:str, last_name:str, street:str, 
                     city:str, zip_code:str, phone:str, email:str, price:float): 
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
            price (float): price of the service

        Returns:
            bool: True if draft was created
        """
        
        self.country = country
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.phone = phone
        self.email = email
        self.price = price
                        
        self.driver.set_page ("https://pro.packlink.com/private/shipments/create/info")
        sleep (4)
        
        self.__shipping__ ()
        self.__service__ ()
        self.__address__ ()
        
        # Select service
        print ()
        