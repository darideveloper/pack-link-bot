import os
from time import sleep
from dotenv import load_dotenv
from sheets import KofiSheets
from kofi import KofiBot
from packlink import PackLinkBot
from scraping.web_scraping import WebScraping

load_dotenv ()
CHROME_FOLDER = os.getenv ("CHROME_FOLDER")

class Bot (WebScraping): 
    
    def __init__ (self):
        
        # Start chrome
        super().__init__ (chrome_folder=CHROME_FOLDER)
        
        self.summary = []        
        
        # Instances
        self.kofi_sheets = KofiSheets ()
        self.kofi_bot = KofiBot (self)
        self.packlink_bot = PackLinkBot (self, self.summary)
        
        
    def create_commissions_drafts (self):
        """ Create a draft for each commission
        """
        
        commissions = self.kofi_sheets.get_kofi_sheet_data ("commissions")
        
        for commission in commissions:
            
            # Get required fields from data
            country = commission ["country"]
            
            # Fix data
            if country == "United States":
                country = "USA"
        
            # Get and validate shipping data
            shipping_data = self.kofi_bot.get_shipping_data (commission["url"])
            if not shipping_data:
                continue
            
            self.packlink_bot.create_draft (
                country=country,
                first_name=shipping_data ["first_name"],
                last_name=shipping_data ["last_name"],
                street=shipping_data ["street"],
                city=shipping_data ["city"],
                zip_code=shipping_data ["zip_code"],
                phone=shipping_data ["phone"],
                email=shipping_data ["email"],
                price=commission ["amount"],
            )
            
            print ()

if __name__ == "__main__":
    # Test create drafts
    bot = Bot ()
    bot.create_commissions_drafts ()