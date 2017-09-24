import findbolig as fb
from apscheduler.schedulers.blocking import BlockingScheduler
import math

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def run():
    username = 'something'
    password = 'something'

    session = fb.login(username, password)
    res = fb.extract(session, True)

    csvfile = fb.save_csv(res)
    data = csvfile.read()

    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("NyboligListe")

    client.import_csv(spreadsheet.id,data)
    print("--------------------------------------------")
    print("YOUR DATA: ")
    print("--------------------------------------------")
    print(data)
    print("--------------------------------------------")
    print("Find it at: https://goo.gl/")

def main():
    sd = BlockingScheduler()

    print("Press Ctrl+C to quit")
    interval = input("At which interval(minutes) do you want to check findbolig.dk? (Enter a number!) ")
    if interval.isdigit():
        print("Setting up with interval of " + interval + " minutes")
        print("Starting")
        run()
        job = sd.add_job(run, 'interval', minutes=int(interval))
        sd.start()
    else:
        print("You didn't enter a number. Goodbye!")


# use one of these: the run function finds the data, the main function makes sure that main gets called every x minutes.

main()
#run()
