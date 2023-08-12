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
            
            # Format data
            row["draft created"] = row["draft created"] == "TRUE"
            
            # Save data
            donations.append (row)
            
        return donations
        
if __name__ == "__main__":
    # Test get data from kofi sheets
    kofi_sheets = KofiSheets ()
    donations = kofi_sheets.get_kofi_sheet_data ("donations")
    sales = kofi_sheets.get_kofi_sheet_data ("sales")
    commissions = kofi_sheets.get_kofi_sheet_data ("commissions")
    print ()
