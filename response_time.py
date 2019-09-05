import datetime
import requests

org_name = input("Github Organisation Name: ")
API_ENDPOINT = "https://web-dep.appspot.com/repos"
DATA = '{"org":"'+str(org_name)+'"}'
# curl --header "Content-Type: application/json" --request POST  --data '{"org": "mozilla"}' https://web-dep.appspot.com/repos 
 
try:
    res = requests.post(API_ENDPOINT, data=DATA, timeout=75)
    res.raise_for_status()
    respTime = str(round(res.elapsed.total_seconds(),2))
    currDate = datetime.datetime.now()
    currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
    print(f"{res.text} \nres_time: {respTime}sec | date_time: {currDate}\n")
except requests.exceptions.HTTPError as e1:
    print ("HTTP error: ", e1)
except requests.exceptions.ConnectionError as e2:
    print ("Error connecting: ", e2)
except requests.exceptions.Timeout as e3:
    print ("Timeout error:", e3)
except requests.exceptions.RequestException as e4:
    print ("Error: ", e4)
