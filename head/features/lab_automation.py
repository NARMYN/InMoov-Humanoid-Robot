import requests

url1 = "https://api.thingspeak.com/update?api_key=G39NYATOHG8YCBE9&field"
url2 = "https://api.thingspeak.com/update?api_key=19C0JCSMVQUHZI0Q&field"

lights = {"AL1": '1'}
fans = {"AF1": '4'}


def switch(cmd: str):
    if "lights" in cmd and "on" in cmd:
        for light in lights.keys():
            if light[0] == 'A':
                s = url1 + lights[light] + '=' + '0'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

            elif light[0] == 'B' or light[0] == 'C':
                s = url2 + lights[light] + '=' + '0'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

    elif "lights" in cmd and "off" in cmd:
        for light in lights.keys():
            if light[0] == 'A':
                s = url1 + lights[light] + '=' + '1'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

            elif light[0] == 'B' or light[0] == 'C':
                s = url2 + lights[light] + '=' + '1'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

    elif "fans" in cmd and "on" in cmd:
        for fan in fans.keys():
            if fan[0] == 'A':
                s = url1 + fans[fan] + '=' + '0'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

            elif fan[0] == 'B' or fan[0] == 'C':
                s = url2 + lights[fan] + '=' + '0'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

    elif "fans" in cmd and "off" in cmd:
        for fan in fans.keys():
            if fan[0] == 'A':
                s = url1 + fans[fan] + '=' + '1'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

            elif fan[0] == 'B' or fan[0] == 'C':
                s = url2 + lights[fan] + '=' + '1'
                a = requests.get(s)
                while a.text == '0':
                    a = requests.get(s)

    else:
        print("Invalid command")
