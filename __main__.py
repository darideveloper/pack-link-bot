import os
import csv
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
        super().__init__ (chrome_folder=CHROME_FOLDER, start_killing=True)
                
        # Instances
        self.kofi_sheets = KofiSheets ()
        self.kofi_bot = KofiBot (self)
        self.packlink_bot = PackLinkBot (self)
        
        # Logs
        self.logs_path = os.path.join (os.path.dirname (__file__), "logs.csv")
        
        
    def create_drafts (self):
        """ Create a draft for each order
        """
        
        print ("Convert orders to drafts...")
        
        order_types = [
            "commissions",
            "sales",
        ]
        
        for order_type in order_types:
        
            orders_data = self.kofi_sheets.get_kofi_sheet_data (order_type)
            orders_num = len (orders_data)
            print (f"\nFound {orders_num} {order_type}.")
            
            for order in orders_data:
                
                error = ""
                status = []
                
                print (f"\nCreating draft for {order['url']}...")
                
                # Get required fields from data
                country = order ["country"]
                
                # Fix data
                if country == "United States":
                    country = "USA"
                if country == "United Kingdom":
                    country = "Kingdom"
            
                # Get and validate shipping data
                try:
                    shipping_data = self.kofi_bot.get_shipping_data (order["url"], order["email"])
                except Exception as e:
                    print (f">> Error getting shipping data: {e}")
                    status = ["error", "getting shipping data", str(e), order["url"]]
                    error = e
                else:
                
                    try:
                        self.packlink_bot.create_draft (
                            country=country,
                            first_name=shipping_data ["first_name"],
                            last_name=shipping_data ["last_name"],
                            street=shipping_data ["street"],
                            city=shipping_data ["city"],
                            zip_code=shipping_data ["zip_code"],
                            phone=shipping_data ["phone"],
                            email=shipping_data ["email"],
                            price=order ["amount"],
                            url=order ["url"],
                            using_default = shipping_data ["using_default"],
                        )
                    except Exception as e:
                        print (f">> Error crating draft: {e}")
                        status = ["error", self.packlink_bot.current_step, str(e), order["url"]]
                        error = e
                
                # Update data in sheets
                if error:
                    
                    if "default" in str(error).lower():
                        error = str(error)
                    else:
                        error = f"Draft NO created: {error}"
                    
                    self.kofi_sheets.update (order_type, order["url"], details=error)
                else:
                    self.kofi_sheets.update (order_type, order["url"], new_status="TRUE")
                    
                    # Set done status
                    print (">> Done")
                    status = ["done", "", "", order["url"]]
                
                
                # Save status in logs
                with open (self.logs_path, "a", newline='') as file:
                    csv_writer = csv.writer (file)
                    csv_writer.writerow (status)
                
            
if __name__ == "__main__":
    # Test create drafts
    bot = Bot ()
    bot.create_drafts ()