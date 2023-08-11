import os
from time import sleep
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper
from sheets import KofiSheets
import re

load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")

class Bot (ChromDevWrapper): 
    
    def __init__ (self):
        super().__init__ (CHROME_PATH)
        
        self.selectors = {
            "packlinkpro": {
                "shipment": {
                    "country": 'input[name="to.country"]',
                    "next": ''
                }                
            },
            "kofi": {
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
        
    def create_commissions_drafts (self, commissions:list):
        """ Create a draft for each commission

        Args:
            commissions (list): list of dicts with commissions data
        """
        
        for commission in commissions:
            
            # Get required fields from data
            country = commission ["country"]
            
            # Fix data
            if country == "United States":
                country = "USA"
        
            # Get data from kofi
            
            # Load details page
            url = commission ["url"]
            self.set_page (url)
            
            # Load shipping details
            self.click (self.selectors ["kofi"]["commission"]["show_details"])
            sleep (3)
            shipping_data = {}
            for name, selector in self.selectors ["kofi"]["commission"].items ():
                shipping_data [name] = self.get_prop (selector, "value")
            
            # Get email and phone
            full_text = self.get_text ("#ticket")
            shipping_data["email"] = self.__extract_regex__ (full_text, self.regex_patterns ["email"])
            if not shipping_data["phone"]:
                shipping_data["phone"] = self.__extract_regex__ (full_text, self.regex_patterns ["phone"])
            
            # Validate data
            exclude_keys = ["show_details"]
            for key in shipping_data:
                if not shipping_data [key] and key not in exclude_keys:
                    print (f"missing {key} for {commission ['url']}")
                    continue
            
            print ()


if __name__ == "__main__":
    # Test create drafts
    bot = Bot ()
    kofi_sheets = KofiSheets ()
    commissions = kofi_sheets.get_kofi_sheet_data ("commissions")
    bot.create_commissions_drafts (commissions)
        
        