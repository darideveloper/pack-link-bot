import os
from dotenv import load_dotenv
from spreadsheets.google_sheets import SheetsManager

load_dotenv ()
GOOGLE_SHEETS = os.getenv ("GOOGLE_SHEETS")
CREDS_PATH = os.path.join (os.path.dirname (__file__), "credentials.json")

class KofiSheets (SheetsManager): 
    """ Manage data from kofi google sheet """
    
    def __init__ (self):
        super().__init__ (GOOGLE_SHEETS, CREDS_PATH)
        
    def get_kofi_sheet_data (self, sheet_name:str) -> list:
        """ Query data from 'kofi donations' page
        
        Args:
            sheet_name (str): sheet name to query

        Returns:
            list: list of dicts with data from kofi donations, sales or commissions:
                commissions: 
                    date, time, user name, amount, email, currency, product name, 
                    country, full address, adiitional details, url, draft created
                donations:
                    TODO
                sales:
                    TODO
        """
        
        self.set_sheet (f"kofi {sheet_name}")
        data = self.get_data ()
        
        # Clean data and formmat
        donations = []
        for row in data:
            
            # Skip empty rows
            if not row["date"]:
                continue
            
            # Skip already done
            if row["draft created"] == "TRUE" or row["details"].strip() != "":
                continue
            
            # Save data
            donations.append (row)
            
        return donations
        
    def update (self, sheet_name:str, url:str, new_status:str="", details:str=""):
        """ Set done to true for a given url
        
        Args:
            sheet_name (str): sheet name to query
            url (str): url to set done
        """
        
        self.set_sheet (f"kofi {sheet_name}")
        data = self.get_data ()
        
        columns = {
            "commissions": {
                "status": 12,
                "details": 13
            },
            "donations": {
                "status": 9,
                "details": 10
            },
            "sales": {
                "status": 12,
                "details": 13
            },
        }
        
        # Clean data and formmat
        row_count = 1
        for row in data:
            
            row_count += 1
            
            if row["url"] == url:
                
                if new_status:
                    self.write_cell (new_status, column=columns[sheet_name]["status"], row=row_count)  

                if details:
                    self.write_cell (details, column=columns[sheet_name]["details"], row=row_count)
        
if __name__ == "__main__":
    # Test get data from kofi sheets
    kofi_sheets = KofiSheets ()
    kofi_sheets.update (
        "commissions", 
        "https://ko-fi.com/home/coffeeshop?txid=d10c91fc-f8d6-4359-a2ab-bbcdfb9ab17b&mode=r&ReturnUrl=/Manage/SupportReceived",
        details="Draft no created: error"
    )
    kofi_sheets.update (
        "commissions", 
        "https://ko-fi.com/home/coffeeshop?txid=d10c91fc-f8d6-4359-a2ab-bbcdfb9ab17b&mode=r&ReturnUrl=/Manage/SupportReceived",
        new_status="TRUE"
    )