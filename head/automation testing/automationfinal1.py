import requests
url1 = "https://api.thingspeak.com/update?api_key=G39NYATOHG8YCBE9&field"
url2 = "https://api.thingspeak.com/update?api_key=19C0JCSMVQUHZI0Q&field"
Dict = {"AL1":'1',"AL2":'2',"AL3":'3',"AF1":'4',
            "BL1":'1',"BL2":'2',"BF1":'3',"CL1":'4',
            "CL2":'5',"CL3":'6',"AC1":'7'}

while(True):    
    n = input("Enter switch name: ")
    m = input('Enter 0 to ON & 1 to OFF')    
    #print(n[2])
    #print(n[0])
    print(Dict[n])
    
    if n[0]=='A':
        s=url1+Dict[n]+'='+m
        print(s)
        a=requests.get(s)    
        while a.text=='0':
            a = requests.get(s)
    
    elif n[0]=='B' or n[0] == 'C'  :
        s=url2+Dict[n]+'='+m
        print(s)
        a=requests.get(s)    
        while a.text=='0':
            a = requests.get(s)
    else:
        print("Please Enter Correct Switch Name")                   

    