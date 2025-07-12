#------Lab Integration Alert---------
#[Lab Analyzer IP Address]
#.....LIS-IP=192.168.1.237
#....Host-IP=172.20.20.67

#[Computer IP Address]

#...192.168.1.237

#Listener Code with python(stage1)
# echo-server.py

import socket
import hl7
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LIS = "172.20.20.108"  # Standard loopback interface address (localhost)
import requests,json
PORT = 5600  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((LIS, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        print("ok")
        while(1): 
            data = conn.recv(2048)
            print(data)
            response = data.decode("utf-8")
                
            #id = (str(data.splitlines()[0]).split('|')[9])
            print('received {} bytes from {}'.format((data), addr))
            #msg = parse_message(data)
            if 'MSH' in str(data): 
                parsed_message = hl7.parse(data)
                counter=len(parsed_message)
                print('Number of segments=',len(parsed_message))
                # Access the individual segments of the message
                print(parsed_message[0])
                print(parsed_message[1])
                i=1
                dt_val = datetime.today().isoformat()
                while i<counter:
                                
                    if  ("OBR"  in str(parsed_message[i]) ): # take only the OBR segment
                        print("kkkkk")
                        print(parsed_message[i])  #print the whole OBR segment
                        print("AccessionNo=",parsed_message[i][3]) # 7th element in OBR segment
                        print("length=",len(parsed_message[i][3]))
                        AccessionNo = str(parsed_message[i][3]).replace(" ", "")
                       
                        
                    
                    elif ('OBX' in str(parsed_message[i]) and "NM" in str(parsed_message[i])):
                        print("mmmmmm")
                        print(parsed_message[i])
                        var=str(parsed_message[i][3]) #WBC,LYM#,LYM%,NLR,PLR,RBC,HGB,MCV,MCH,MCHC,RDW-CV,RDW-SD,HCT,PLT,MPV,PDW,PCT,MID#,MID%,GRAN#,GRAN%,PLCC,PLCR
                        var=var.split('^')[1] # split and take the second item
                        if(var=="GRAN%"): var="GRANP"
                        if(var=="GRAN#"): var="GRANN"
                        if(var=="MID#"): var="MIDN"
                        if(var=="MID%"): var="MIDP"
                        if(var=="LYM%"): var="LYMP"
                        if(var=="LYMN"): var="LYMN"
                        if(var=="P-LCC"): var="PLCC"
                        if(var=="P-LCR"): var="PLCR"
                        if(var=="LYM#"): var="LYMN"
                        if(var=="BAS#"): var="BASN"
                        if(var=="BAS%"): var="BASP"
                        if(var=="*ALY#"): var="ALYN"
                        if(var=="*ALY%"): var="ALYP"
                        if(var=="*LIC#"): var="LICN"
                        if(var=="*LIC%"): var="LICP"
                        if(var=="EOS#"): var="EOSN"
                        if(var=="EOS%"): var="EOSP"
                        if(var=="MON%"): var="MONP"
                        if(var=="MON#"): var="MONN"
                        if(var=="NEU#"): var="NEUN"
                        if(var=="NEU%"): var="NEUP"
                      
                        
                       
                        var_value=parsed_message[i][5]
                        var_value=str(var_value).replace('[','')
                        var_value=str(var_value).replace(']','')
                        var_value=str(var_value).replace('"','')
                        
                        print(var,var_value)
                    #i+=1
                
            
                        post_data = { "machineName": "MINDRAY BC30",
                            "parameterName": var,
                            "result": var_value,
                            "sampleId": AccessionNo,
                            "dateTime": dt_val
                            }          
                        r = requests.post('https://172.20.20.125/openelis/addAnalyzerData',data=json.dumps(post_data),verify=False)
                    i+=1    
                            # str(parsed_message[i][3])+"=",parsed_message[i][5]