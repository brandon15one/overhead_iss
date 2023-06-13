import requests
from datetime import datetime
import smtplib


MY_LAT = 00000000
MY_LONG = 000000
MY_EMAIL = "#############"
MY_PASS = "###############"


def is_iss_overhead():
    res = requests.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()
    datas = res.json()

    iss_latitude = float(datas["iss_position"]["latitude"])
    iss_longitude = float(datas["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: LOOK ABOVE IN THE NIGHT SKY!! \n\n the iss is above you in the sky"
        )
