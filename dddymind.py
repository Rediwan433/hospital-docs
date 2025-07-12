#!/usr/bin/python

import hl7
import socket
from datetime import datetime
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Original HL7 example data (commented out)
# data = 'MSH|^~\\&|20250603210849ORU^R01|9|P|2.3.1UNICODE\rPID|1^^^^MR\rPV1|1\rOBR|103062025-002|00001^Automated Count^99MRC|20250603205957|HMAdministrator\rOBX|1|IS|08001^Take Mode^99MRCOF\rOBX|2|IS|08002^Blood Mode^99MRCWF\rOBX|3|IS|01002^Ref Group^99MRCGeneralF\rOBX|4|NM|6690-2^WBC^LN2.4|10*3/uL|4.0-10.0|L~N|F\rOBX|5|NM|731-0^LYM#^LN1.1|10*3/uL|0.8-4.0|N|F\rOBX|6|NM|736-9^LYM%^LN44.7|%|20.0-40.0|H~N|F\rOBX|7|NM|789-8^RBC^LN5.61|10*6/uL|3.50-5.50|H~N|F\rOBX|8|NM|718-7^HGB^LN23.3|g/dL|11.0-16.0|H~N|F\rOBX|9|NM|787-2^MCV^LN122.5|fL|80.0-100.0|H~N|F\rOBX|10|NM|785-6^MCH^LN41.5|pg|27.0-34.0|H~N|F\rOBX|11|NM|786-4^MCHC^LN33.9|g/dL|32.0-36.0|N|F\rOBX|12|NM|788-0^RDW-CV^LN14.6|%|11.0-16.0|N|F\rOBX|13|NM|21000-5^RDW-SD^LN62.0|fL|35.0-56.0|H~N|F\rOBX|14|NM|4544-3^HCT^LN68.8|%|37.0-54.0|H~N|F\rOBX|15|NM|777-3^PLT^LN140|10*3/uL|100-300|N|F\rOBX|16|NM|32623-1^MPV^LN9.2|fL|6.5-12.0|N|F\rOBX|17|NM|32207-3^PDW^LN17.9|15.0-17.0|H~N|F\rOBX|18|NM|10002^PCT^99MRC1.28|mL/L|1.08-2.82|N|F\rOBX|19|NM|10027^MID#^99MRC0.1|10*3/uL|0.1-1.5|N|F\rOBX|20|NM|10029^MID%^99MRC5.6|%|3.0-15.0|N|F\rOBX|21|NM|10028^GRAN#^99MRC1.2|10*3/uL|2.0-7.0|L~N|F\rOBX|22|NM|10030^GRAN%^99MRC49.7|%|50.0-70.0|L~N|F\rOBX|23|NM|10013^PLCC^99MRC34|10*9/L|30-90|N|F\rOBX|24|NM|10014^PLCR^99MRC24.2|%|11.0-45.0|N|F\rOBX|25|IS|12003^Leucopenia^99MRCTF\rOBX|26|IS|12013^RBC Abnormal distribution^99MRCTF\rOBX|27|IS|15198-5^Macrocytes^LNT||||F\r\x1c\r'

# Server configuration
host = "172.20.20.175"
port = 5600

s = socket.socket()
s.bind((host, port))
s.listen(1)

print(f"Listening on {host}:{port}")
conn, addr = s.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(2048)
    if not data:
        break

    print(data)

    # Only proceed if HL7 MSH header is detected
    if 'MSH' in str(data):
        parsed_message = hl7.parse(data)
        counter = len(parsed_message)
        print('Number of segments =', counter)

        # Display MSH and PID segments
        print(parsed_message[0])
        print(parsed_message[1])

        i = 1
        dt_val = datetime.today().isoformat()

        while i < counter:
            # Extract OBR (Order Request)
            if "OBR" in str(parsed_message[i]):
                print("kkkkk")
                print(parsed_message[i])
                print("Med_Rec_No =", parsed_message[i][3])
                Med_Rec_No = str(parsed_message[i][3]).replace(" ", "")

            # Extract OBX (Observation/Results) if it's numeric
            elif "OBX" in str(parsed_message[i]) and "NM" in str(parsed_message[i]):
                print("mmmmmm")
                print(parsed_message[i])

                var = str(parsed_message[i][3])
                var = var.split('^')[1]

                # Normalizing variable names
                if var == "GRAN%":
                    var = "GRANP"
                if var == "GRAN#":
                    var = "GRANN"
                if var == "MID#":
                    var = "MIDN"
                if var == "MID%":
                    var = "MIDP"
                if var == "LYM%":
                    var = "LYMP"
                if var == "LYMN":
                    var = "LYMN"

                var_value = str(parsed_message[i][5]).replace('[', '').replace(']', '').replace('"', '')
                print(var, var_value)

                post_data = {
                    "machineName": "DYMIND DF50",
                    "parameterName": var,
                    "result": var_value,
                    "sampleId": Med_Rec_No,
                    "dateTime": dt_val
                }

                r = requests.post(
                    'https://172.20.20.125/openelis/addAnalyzerData',
                    data=json.dumps(post_data),
                    verify=False
                )

            i += 1
