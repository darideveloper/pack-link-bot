import re
from time import sleep
from dotenv import load_dotenv
from scraping.web_scraping import WebScraping

load_dotenv ()

class KofiBot (): 
        
    def __init__ (self, driver:WebScraping):
        
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
                "ticket": '#ticket'
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
                r'\(\d{3}\)[\s-]?\d{3}[\s-]?\d{4}',
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
        
    def get_shipping_data (self, url:str, email:str) -> dict:
        """ Get shipping data from kofi

        Args:
            url (str): url of the kofi donation
            email (str): email of the user

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
        self.driver.refresh_selenium ()
        full_text = self.driver.get_text (self.selectors ["commission"]["ticket"])
        
        # Load shipping details
        self.driver.click (self.selectors ["commission"]["show_details"])
        self.driver.refresh_selenium ()        
        sleep (3)
        
        shipping_data = {"using_default": []}
        for name, selector in self.selectors ["commission"].items ():
            shipping_data [name] = self.driver.get_attrib (selector, "value")
        
        # Get email and phone
        shipping_data["email"] = self.__extract_regex__ (full_text, self.regex_patterns ["email"])
        if not shipping_data["phone"]:
            shipping_data["phone"] = self.__extract_regex__ (full_text, self.regex_patterns ["phone"])
        
        # Remove extra fields
        extra_fields = ["show_details", "ticket"]
        for row in extra_fields:
            shipping_data.pop (row)
        
        # Fix email
        if not shipping_data["email"]:
            shipping_data["email"] = email
        
        # Validate data
        default_data = {
            "email": "sample@gmail.com",
            "phone": "+12345678912"
        }
        for key in shipping_data:
            if not shipping_data [key]: 
                
                # Skip default values control
                if key == "using_default":
                    continue
                
                # Use default value
                default_value = default_data.get (key, "")
                if default_value:
                    shipping_data [key] = default_value
                    shipping_data ["using_default"].append (key)
                else:
                    raise Exception (f"missing {key}")
            
        return shipping_data        