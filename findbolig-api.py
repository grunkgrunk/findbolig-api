import requests, grequests
from bs4 import BeautifulSoup
import re
import csv
import time
import json
import math

def login(username, password):
    session = requests.session()

    login_url = 'https://www.findbolig.nu/logind.aspx'
    response = session.get(login_url)

    data = dict()
    content = response.text
    input_fields = re.findall("<input(.*)>", content, flags=re.IGNORECASE)
    for field in input_fields:
    	name = re.findall('.*name="([^"]*)".*', field)
    	value = re.findall('.*value="([^"]*)".*', field)
    	if name:
    		if value:
    			data[name[0]] = value[0]
    		else:
    			data[name[0]] = ""
    data["ctl00$placeholdercontent_1$txt_UserName"] = username
    data["ctl00$placeholdercontent_1$txt_Password"] = password
    data["__EVENTTARGET"] = "ctl00$placeholdercontent_1$but_Login"
    data["__EVENTARGUMENT"] = ""

    response = session.post(login_url, data=data)
    if "Log af" in response.text:
    	# Extract users full name.
    	name = re.search('<span id="fm1_lbl_userName">(.*)&nbsp;</span>', response.text)
    	return session
    else:
        return False



def extract(session):
    waiting_list = 'https://www.findbolig.nu/Findbolig-nu/Min-side/ventelisteboliger/opskrivninger?'
    page = session.get(
        waiting_list,
        headers = dict(referer = waiting_list)
    )

    soup = BeautifulSoup(page.content, 'html.parser')
    strsoup = str(soup)

    # different regexes to find properties of interest.
    p = re.compile('\d+ boliger')
    boliger = p.findall(strsoup)

    p = re.compile('\d+ København \w+')
    postal = p.findall(strsoup)

    names_soup = soup.find_all("td", {"align":"left", "style":"width:170px;"})
    p = re.compile('0">.*</f')

    names = []
    for name in names_soup:
        res = p.findall(str(name))[0]
        # the interesting part is in this range 3:-3.
        # could use a group instead.
        names.append(res[3:-3])


    adress_soup = soup.find_all("td", {"align":"left", "style":"width:185px;"})
    p = re.compile('0">.*<br/>')
    # this edge case might happen some time in the future aswell for one
    # of the other properties
    p2 = re.compile(">.*\.\.\.<br/")
    adresses = []
    for adr in adress_soup:
        res = p.findall(str(adr))
        if len(res) != 0:
            adresses.append(res[0][3:-5])
        else:
            res = p2.findall(str(adr))
            adresses.append(res[0][1:-4])


    p = re.compile("bid=(\d+)")
    url_soup = soup.find_all("td",  {"align":"left", "style":"width:180px;"})

    # a bid is sort of a url that is unique
    # to each apartment. It is needed to find
    # the ranking of that specific apartment.
    bids = []
    for u in url_soup:
        res = p.findall(str(u))
        bids.append(res[0])

    # this is the url we use to get the rankings of
    # the apartments
    placement = "https://www.findbolig.nu/Services/WaitlistService.asmx/GetWaitlistRank"

    # we dump all requests in this list so we can make
    # an asynchronous request with grequests.
    rs = []

    for i,bid in enumerate(bids):
        data = {
			'buildingId': bid
		}
        headers = {
			'Content-Type': 'application/json; charset=UTF-8'
		}
        rs.append(grequests.post(
                placement,
                data=json.dumps(data),
                headers=headers,
                session=session
            )
        )


    responses = grequests.map(rs)
    ranks = []
    for r in responses:
        dic = r.json()
        # if we got a rank we append the rank,
        # otherwise we append "???"
        rank = "???"
        if dic["d"] and dic["d"]["WaitPlacement"]:
            rank = dic["d"]["WaitPlacement"]
        ranks.append(rank)

    # build list that contains all content
    extracted = []
    for i in range(len(names)):
        o = {}
        o["Ejendomsnavn"] = names[i]
        o["Adresse"] = adresses[i]
        o["Postnummer"] = postal[i]
        o["Opskrivninger"] = boliger[i]
        o["Rank"] = ranks[i]
        extracted.append(o)

    # sort the results
    def sortfn(x):
        if x["Rank"] == "???":
            return math.inf
        return int(x["Rank"])

    extracted.sort(key=sortfn)
    return extracted


def save_csv(extracted):
    # this function just makes a csv from
    # the extracted data. The file and the content of the file
    # will have a timestamp
    timestr = time.strftime("%H:%M-%d-%m-%Y")
    filename = "output-" + timestr + ".csv"

    with open(filename, 'w') as csvfile:
        fieldnames = ["Rank", "Ejendomsnavn", "Adresse", "Postnummer", "Opskrivninger", timestr]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for d in extracted:
            writer.writerow(d)



    return open(filename, 'r')

def test():
    username = 'someusername'
    password = 'somepassword'

    session = login(username, password)
    extracted = extract(session)

    print(extracted)
    save_csv(extracted)

if __name__ == "__main__":
    test()
