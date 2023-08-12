import os
from time import sleep
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper
import re

load_dotenv ()

class KofiBot (): 
        
    def __init__ (self, driver:ChromDevWrapper):
        
         # Connect to chrome dev tools
        self.driver = driver
         
        self.selectors = {
            "commission": {
                "show_details": 'a[onclick^="updateShippingDetailsApp"]',
                "first_name": 'input[placeholder="First name"]',
                "last_name": 'input[placeholder="Last name"]',
                "street": 'input[placeholder="Street address"]',
                "city": 'input[placeholder="City"]',
                "zip_code": 'input[placeholder="Postal code"]',  
                "phone": 'input[placeholder="Telephone"]',
            }
        }
        
        self.regex_patterns = {
            "email": [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            "phone": [
                r'\+?\d{2}\s\d{3}\s\d{3}\s\d{3}',
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\+?\d{1,3}[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}',
                r'\+?\d{1,3}[.\s]?\(?\d{3}\)?[.\s]?\d{3}[.\s]?\d{4}',
                r'\+?\d{1,3}-\d{3}-\d{3}-\d{4}',
                r'\+?\d{1,3}\.\d{3}\.\d{3}\.\d{4}',
                r'\+?\d{8,15}',
                r'\d{3}-\d{3}-\d{4}',
            ]
        }
                
    def __extract_regex__ (self, text:str, patterns:str) -> str:
        """ Get email using regex

        Args:
            text (str): html text from ko-fi
            pattern (str): regex pattern
            
        Returns:
            str: email found
        """
        
        for pattern in patterns:
        
            items_found = re.findall(pattern, text)
            if items_found:
                return items_found[0]
        
        return ""       
        
    def get_shipping_data (self, url:str) -> dict:
        """ Get shipping data from kofi

        Args:
            comission (dict): kofi details link

        Returns:
            dict: shipping data based in payment type
                comission: 
                    first_name
                    last_name
                    street
                    city
                    zip_code
                    phone
        """
        
        # Load details page
        self.driver.set_page (url)
        
        # Load shipping details
        self.driver.click (self.selectors ["commission"]["show_details"])
        sleep (3)
        shipping_data = {}
        for name, selector in self.selectors ["commission"].items ():
            shipping_data [name] = self.driver.get_prop (selector, "value")
        
        # Get email and phone
        full_text = self.driver.get_text ("#ticket")
        shipping_data["email"] = self.__extract_regex__ (full_text, self.regex_patterns ["email"])
        if not shipping_data["phone"]:
            shipping_data["phone"] = self.__extract_regex__ (full_text, self.regex_patterns ["phone"])
        
        # Remove extra fields
        extra_fields = ["show_details"]
        for row in extra_fields:
            shipping_data.pop (row)
        
        # Validate data
        for key in shipping_data:
            if not shipping_data [key]:
                print (f"missing {key} for {url}")
                return {}
            
        return shipping_data        