#------Lab Integration Alert---------
#[Lab Analyzer IP Address]
#.....LIS-IP=172.20.20.175
#....Host-IP=172.20.20.67

#[Computer IP Address]

#...172.20.20.175

#Listener Code with python(stage1)
# echo-server.py

import socket
import hl7

LIS = "172.20.20.175"  # Standard loopback interface address (localhost)
PORT = 5600  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((LIS, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(2048)
            response = data.decode("utf-8")
            
            #id = (str(data.splitlines()[0]).split('|')[9])
            print('received {} bytes from {}'.format((data), addr))
                  
            h = hl7.parse(data)
            #print(h.segment('PID')[3][0])
            #print(h.segment('PID')[5][0])
            print(h.segment('MSH')[3][0])
            print(h.segment('OBR')[3][0])

            print("AccessionNo="+h.segment('OBR')[6][0])
            print("WBC=",h.segments('OBX')[6][5][0])
            print("NEU%=",h.segments('OBX')[7][5][0])
            print("LYM%=",h.segments('OBX')[8][5][0])
            print("MON%=",h.segments('OBX')[9][5][0])

            print("EOS%=",h.segments('OBX')[10][5][0])

            print("BAS%=",h.segments('OBX')[11][5][0])

            print("NEU#=",h.segments('OBX')[12][5][0])

            print("LYM#=",h.segments('OBX')[13][5][0])

            print("MON#=",h.segments('OBX')[14][5][0])

            print("EOS#=",h.segments('OBX')[15][5][0])

            print("BAS#=",h.segments('OBX')[16][5][0])
            
          

            print("ALY#=",h.segments('OBX')[17][5][0])

            print("ALY%=",h.segments('OBX')[18][5][0])

            print("LIC#=",h.segments('OBX')[19][5][0])

            print("LIC%=",h.segments('OBX')[20][5][0])

            print("RBC=",h.segments('OBX')[21][5][0])

            print("HGB=",h.segments('OBX')[22][5][0])

            print("HCT=",h.segments('OBX')[23][5][0])

            print("MCV=",h.segments('OBX')[24][5][0])

            print("MCH=",h.segments('OBX')[25][5][0])

            print("MCHC=",h.segments('OBX')[26][5][0])

            print("RDW-CV=",h.segments('OBX')[27][5][0])

            print("RDW-SD=",h.segments('OBX')[28][5][0])

            print("PLT=",h.segments('OBX')[29][5][0])

            print("MPV=",h.segments('OBX')[30][5][0])

            print("PDW=",h.segments('OBX')[31][5][0])
            print("PCT=",h.segments('OBX')[32][5][0])
            
            if not data:
                break
            
            conn.sendall(data)



