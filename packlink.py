import os
import json
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
RISK_SHIPMENT = os.getenv ("RISK_SHIPMENT") == "True"
CUSTOM_CATEGORY = os.getenv ("CUSTOM_CATEGORY")
CUSTOM_DETAILS = os.getenv ("CUSTOM_DETAILS")
CUSTOM_MADE_IN = os.getenv ("CUSTOM_MADE_IN")
CUSTOM_QUANTITY = os.getenv ("CUSTOM_QUANTITY")
CUSTOM_WEIGHT = os.getenv ("CUSTOM_WEIGHT")

class PackLinkBot (): 
    
    def __init__ (self, driver:WebScraping):
        """ Create a draft for each commission

        Args:
            driver (ChromDevWrapper): chrome dev tools wrapper
        """
        
        
        # Connect to chrome dev tools
        self.driver = driver
        
        self.shipping_price = 0
        self.price = 0
        self.current_step = "start"
      
        self.selectors = {
            "new_button": '.css-1pae1zp button[type="button"]',
            "menu_item": 'button[role="menuitem"]',
            "next": 'button[type="submit"]',
            "save": 'button[data-id="checkout-save-button"]',
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
            },
            "custom": {
                'invoice': 'input[name="invoiceNumber"]',
                'category': 'input[name="inventoryOfContents[0].category"]',
                'description': 'textarea[name="inventoryOfContents[0].description"]', 
                'made': 'input[name="inventoryOfContents[0].countryOfOrigin"]',
                'quantity': 'input[name="inventoryOfContents[0].numberOfItems"]',
                'value': 'input[name="inventoryOfContents[0].value"]',
                'weight': 'input[name="inventoryOfContents[0].weight"]',
                'terms': 'input[name="customsTerms"]',
                'vat': 'label[for="receiver.vatStatus"]',
                'vat_personal': 'button[role="menuitem"]:last-child'
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
            
            # Delete text
            elem = self.driver.get_elem (selector)
            elem.send_keys(Keys.BACKSPACE * len(value))
            
            return False
        
        self.driver.click (self.selectors ["menu_item"])
        return True
    
    def __get_selectors__ (self, step:str) -> dict:
        """ Get css selectors for current step, update step and
            refresh selenium
        """
        
        self.current_step = step
        selectors = self.selectors [step]
        self.driver.refresh_selenium ()
        return selectors        
    
    def __write_group__ (self, selectors:dict, data:dict):
        """ Write text in a group of inputs

        Args:
            selectors (dict): css selectors of the inputs
            data (dict): data to write
        """
        
        # Main data
        for key, value in data.items ():
            
            # Delete old chars
            input_elem = self.driver.get_elem (selectors[key])
            input_text = self.driver.get_attrib (selectors[key], "value")
            if input_text:
                input_elem.send_keys(Keys.BACKSPACE * len(input_text))
                      
            self.driver.send_data (selectors[key], value)
    
    def __shipping__ (self):
        """ Write data in shipping details section
        """
        
        selectors = self.__get_selectors__ ("shipment")
        
        # Select country and post code
        country_found = self.__select_item__ (selectors["country"], self.country)
        zip_code_found = self.__select_item__ (selectors["post_code"], self.zip_code)
        if not zip_code_found:
            zip_code_found = self.driver.send_data (selectors["post_code"], self.city)
        
        # Validate if country and post code were found
        if not country_found:
            raise Exception (f"country not found for {self.country}")
        
        if not zip_code_found:
            raise Exception(f"zip code and city not found for {self.zip_code, self.city}")
            
        # Write parcel data (if its required)
        current_weight = self.driver.get_attrib (selectors["weigth"], "value")
        if not current_weight:
            self.driver.send_data (selectors["weigth"], PARCEL_WEIGTH)
            self.driver.send_data (selectors["lenght"], PARCEL_LENGTH)
            self.driver.send_data (selectors["width"], PARCEL_WIDTH)
            self.driver.send_data (selectors["height"], PARCEL_HEIGHT)
        
        self.driver.click (self.selectors["next"])
        sleep (1)
            
    def __service__ (self):
        """ Select service and save price
        """
        
        # Selectors and step
        selectors = self.__get_selectors__ ("service")
        
        self.shipping_price = self.driver.get_text (selectors["price"])
        button = self.driver.get_text (selectors["button"])
        
        if not self.shipping_price or not button:
            raise Exception("services not found")
        
        # Format price
        self.shipping_price = float (self.shipping_price.replace ("€", "").replace (",", "."))
        
        # Select service
        self.driver.click (selectors["button"])
        sleep (1)
        
    def __address__ (self):
        """ Write data in address section
        """
        
        # Selectors and step
        selectors = self.__get_selectors__ ("address")
            
        # Write main data
        self.__write_group__ (selectors, {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "street": self.street,
            "content_value": str(self.price - self.shipping_price),
        })
        
        # Content shipped
        content_shipped_found = self.__select_item__ (selectors["content_shipped"], CONTENT_SHIPPED)
        if not content_shipped_found:
            raise Exception(f"content shipped not found for {CONTENT_SHIPPED}")
        
        # Risk option
        if RISK_SHIPMENT:
            self.driver.click_js (selectors["risk"])
        else:
            self.driver.click_js (selectors["no-risk"])
    
        # Submit form with js
        self.driver.refresh_selenium ()
        self.driver.click (self.selectors["next"])
        sleep (1)
        
    def __custom__ (self):
        """ Write data in custom section
        """
        
        # Selectors and step
        selectors = self.__get_selectors__ ("custom")
        
        # Get invoice number from json
        json_path = os.path.join (os.path.dirname (__file__), "counters.json")
        with open (json_path, "r") as file:
            counters = json.load (file)
            invoice_number = counters ["invoice_number"]
        
        # Validate if custom data is required
        custom_category_text = self.driver.get_attrib (selectors["category"], "value")
        if not custom_category_text:
            return False
        
        # Select category
        category_found = self.__select_item__ (selectors["category"], CUSTOM_CATEGORY)
        
        # Select made in
        mode_in_found = self.__select_item__ (selectors["made"], CUSTOM_MADE_IN)
        
        # Select vat
        self.driver.click_js (selectors["vat"])
        self.driver.refresh_selenium ()
        self.driver.click_js (selectors["vat_personal"])
        
        # Raise errors
        if not category_found:
            raise Exception(f"category not found for {CUSTOM_CATEGORY}")
        
        if not mode_in_found:
            raise Exception(f"made in not found for {CUSTOM_MADE_IN}")
            
        # Write main data
        self.__write_group__ (selectors, {
            'invoice': invoice_number,
            'description': CUSTOM_DETAILS,
            'quantity': CUSTOM_QUANTITY,
            'value': str(self.price - self.shipping_price),
            'weight': CUSTOM_WEIGHT,
        })
        
        # Accept terms
        self.driver.click_js (selectors["terms"])
            
        # Update invoice number
        counters ["invoice_number"] += 1
        with open (json_path, "w") as file:
            json.dump (counters, file, indent=4)
            
        return True
        

    def create_draft (self, country:str, first_name:str, last_name:str, street:str, 
                     city:str, zip_code:str, phone:str, email:str, price:float, url:str,
                     using_default:list): 
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
            url (str): url of the commission
            using_default (list): list of fields that were filled with default values

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
        self.url = url
        self.using_default = using_default
                        
        self.driver.set_page ("https://pro.packlink.com/private/shipments/ready-to-purchase")
        self.driver.refresh_selenium ()
        self.driver.click_js (self.selectors["new_button"])
        sleep (4)
        self.driver.refresh_selenium ()
        
        self.__shipping__ ()
        self.__service__ ()
        self.__address__ ()
        custom_required = self.__custom__ ()
        
        # Save draft
        self.driver.refresh_selenium ()
        self.driver.click (self.selectors["save"])
        sleep (6)
        
        if self.using_default:
            error = f"Draft created using default values for {', '.join(self.using_default)}"
            
            if not custom_required:
                error += " and custom data not required"
            
            raise Exception (error)