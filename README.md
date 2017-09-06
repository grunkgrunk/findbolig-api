# findbolig-api
A python web-scraper that automates the process of finding your placements on www.findbolig.nu. 

## Dependencies
You will need the python-modules: beautifulsoup4 and requests.

## How to use
First you need to download findbolig.py and put it in inside your working directory. Now you can import:

    import findbolig as fb
  
Now you can use the module to login to your findbolig account and extract the contents of www.findbolig.nu.

    session = fb.login(username, password)
    extracted = fb.extract(session, verbose=False)
    
The extracted function takes very long to complete. If you are afraid that the program does not work because nothing happens after the extract function is called, you can just pass true to the second parameter of the function. This will make the function print some info whenever it retrieves ranks from the site. The "extracted" variable now holds a list of dictionaries in the form:

    [{
        'Adresse': 'Lundtoftegade', 
        'Opskrivninger': '17 boliger', 
        'Ejendomsnavn': 'Lundtoftegade', 
        'Postnummer': '2400 København NV', 
        'Rank': 122
      }, ...]

The result is sorted by rank from lowest to highest.

If you want, you can save the results as a csv-file:
    
    fb.save_csv(extracted)

## The example
In this repo you can find a file called "example.py". This is a program that makes use of this module. It gets the contents of findbolig, then it saves a csv which is then imported to a spreadhsheet at Google Sheets. The program automatically runs at a specified time-interval. If you want to use this program, you will need to create a "client.json" file for this to work. Follow this tutorial to get up and running with Google Sheets and python: https://www.youtube.com/watch?v=vISRn5qFrkM.

## Why it's slow
You should know that it takes a very long time for the extract function to complete. This is because the site is very slow to respond when asked for the rankings. It is also slow because the ranks are retrieved one by one. 
