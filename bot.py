import os
from dotenv import load_dotenv
from chrome_dev.chrome_dev import ChromDevWrapper

load_dotenv ()
CHROME_PATH = os.getenv ("CHROME_PATH")

class Bot (ChromDevWrapper): 
    
    def __init__ (self):
        super().__init__ (CHROME_PATH)
        
    