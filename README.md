# findbolig-api
A python web-scraper that automates the process of finding your placements on www.findbolig.nu. 

## Dependencies

You will need the python-modules: beautifulsoup4, requests and grequests.

## How to use

First you need to download findbolig-api.py and put it in inside your working directory. Now you can import:

    import findbolig-api as fb
  
Now you can use the module to login and extract the contents of www.findbolig.nu.

    session = fb.login(username, password)
    extracted = fb.extract(session)
    
The "extracted" variable now holds a list of dictionaries in the form:

    [{
        'Adresse': 'Lundtoftegade', 
        'Opskrivninger': '17 boliger', 
        'Ejendomsnavn': 'Lundtoftegade', 
        'Postnummer': '2400 København NV', 
        'Rank': 122
      }, ...]

If you want, you can save the results as a csv-file:
    
    fb.save_csv(extracted)

## Important
You should know that it takes a very long time for the extract function to complete. I have tried to help the problem by using grequests so I could get the data asynchronously, but it still takes a long time. I don't really know how to make it faster at this point.
