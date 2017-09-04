# findbolig-api
A python web-scraper that automates the process of finding your placements on www.findbolig.nu. 

## How to use

First you need to download findbolig-api.py and put it in inside your working directory. Now you can import:

    import findbolig-api as fb
  
Now you can use the module to login and extract the contents of www.findbolig.nu.

    session = fb.login(username, password)
    extracted = fb.extract(session)
    
The extracted variable is a list of dictionaries in the form:

If you want, you can save the results as a csv-file:
    
    fb.save_csv(extracted)
