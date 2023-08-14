<div><a href='https://github.com/darideveloper/pack-link-bot/blob/master/LICENSE' target='_blank'>
                <img src='https://img.shields.io/github/license/darideveloper/pack-link-bot.svg?style=for-the-badge' alt='MIT License' height='30px'/>
            </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a><a href='https://www.twitch.tv/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Twitch&color=b9a3e3&logo=Twitch&logoColor=ffffff&label=' alt='Twitch' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/pack-link-bot/blob/master/logo.png?raw=true' alt='Pack Link Bot' height='80px'/>



# Pack Link Bot

Project for creating shipment drafts in [Pack LInk Pro](https://pro.packlink.com/private) using the data stored in Google Sheets, from the project [Kofi API](https://github.com/darideveloper/kofi-api)

Project type: **client**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#relatedprojects'>Related Projects</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a><a href='https://sheets.google.com/' target='_blank'> <img src='https://www.gstatic.com/images/branding/product/1x/sheets_2020q4_48dp.png' alt='Google Sheets' title='Google Sheets' height='50px'/> </a></div>

# Related projects

<div align='center'><a href='https://github.com/darideveloper/kofi-api' target='_blank'> <img src='https://github.com/darideveloper/kofi-api-sheets-email/blob/master/logo.png?raw=true' alt='Kofi Api' title='Kofi Api' height='50px'/> </a></div>

# Media

![address data content type](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/address-data-content-type.png?raw=true)

![address data recipient](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/address-data-recipent.png?raw=true)

![choose a service](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/choose-a-service.png?raw=true)

![custom items](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/custom-items.png?raw=true)

![custom sender details](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/custom-sender-details.png?raw=true)

![shipment details](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/shipment-details.png?raw=true)

# Details

For use this project, you should have a [Kofi API](https://github.com/darideveloper/kofi-api) service working, and saving data in a google sheets. 
You also need a **Kofi account** (the same as the Kofi API) **already logged in your google chrome**, and a **Pack Link Pro account** already logged too. 

## Workflow

The project will: 

1. Get main data from the google sheet. 
2. Extract the shipping data from kofi details page
3. Go to [Pack Link Pro Create page](https://pro.packlink.com/private/shipments/create/info)
4. In the **Shipment details** page, it will fill the: 
	* Country
	* Zip code
	* Weight (if required)
	* Length (if required)
	* Width (if required)
	* Height  (if required)
5. In the **Choose a service** page, it will select the first option
6. In the **Address data** page, it will: 
	* fill the address data with the client user info 
	* Select the content type
	* Set a value (calculated as: *product value from google sheet*, minus *shipment price*)
	* Select the "Shipment protection" or "I am willing to risk my shipments", based in your settings (more about settings details in the following sections)
7. In the **Customs** page (if is active), it will fill the following data from settings:
	* Invoice number
	* Category
	* Description
	* Items made in
	* Quantity
	* Value (the same as above)
	* Weight
8. Save the draft

# Install

## Programs

To run the project, the following software must be installed:: 

* [Google Chrome](https://www.google.com/intl/es/chrome) last version
* Python >= 3.10
* 
## Third party modules

Install all the python modules from pip: 

``` bash
$ pip install -r requirements.txt
```

# Settings

## Enviroment variables

In this file (`.env`), are the main options and settings of the project.

1. Create a **.env** file, and place the following content

```bash
CHROME_FOLDER = C:Users{your-user}AppDataLocalGoogleChromeUser Data
GOOGLE_SHEETS=https://docs.google.com/spreadsheets/d/{some random chars}/edit?pli=1#gid=0
PARCEL_WEIGTH = 1
PARCEL_LENGTH = 10
PARCEL_WIDTH = 10
PARCEL_HEIGHT = 10
CONTENT_SHIPPED = Electronics
RISK_SHIPMENT = True
CUSTOM_CATEGORY = videogames
CUSTOM_DETAILS = Sample text here
CUSTOM_MADE_IN = México
CUSTOM_QUANTITY = 1
CUSTOM_WEIGHT = 1
```
*Note: you can see as reference the **sample.env** file*

### CHROME_FOLDER

Path of your google chrome data
By default, in windows `C:Users{your-user}AppDataLocalGoogleChromeUser Data`

### GOOGLE_SHEETS

The link of the google sheet where data will be saved, with edit permissions
Details about structure and content, in the project [Kofi API](https://github.com/darideveloper/kofi-api)

### PARCEL_* 

PARCEL_WEIGTH, PARCEL_LENGTH, PARCEL_WIDTH and PARCEL_HEIGHT

These are the values to set in the section **Parcels** from the **Shipment details page**

![shipment parcels](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/readme/shipment-parcels.png?raw=true)

### CONTENT_SHIPPED

The content in the section **Content shipped** from the page **Address data**

![address data content type-content](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/readme/address-data-content-type-content.png?raw=true)

### RISK_SHIPMENT

`True` for select the **I am willing to risk my shipments** option, else (for add a protection) save as `False`

### CUSTOM_* 

CUSTOM_CATEGORY, CUSTOM_MADE_IN, CUSTOM_QUANTITY, CUSTOM_WEIGHT

Data to write in the **items** section from the page **Customs**

*Note: if there are categories with similar names, `CUSTOM_CATEGORY`  can be only a word of the category name (if you write this word manually, the first displayed option should be the correct one). 

![custom](https://github.com/darideveloper/pack-link-bot/blob/master/screenshots/readme/custom.png?raw=true)

## Counters 

In the file `counters.json`, there is the options `invoice_number`. This is a counter of the orders created and it will be saved in the **Customs** page. 
You can edit it. 

```json
{
    "invoice_number": 333
}
```

*Note: you can see as reference the **sample.counters.json** file*

# Run

For run the bot, just run with your python interpreter the `__main__.py` file  or the project folder

```bash
$ python .
```

```bash
$ python __main__.py
```

