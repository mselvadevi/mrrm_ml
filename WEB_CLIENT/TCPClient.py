import socket
import sys, os
import json
import pickle

def submit_request(dict_request_data,host = "127.0.0.1", port = 6000):
    print(f'---------TCPcleint side request received---------')
    received = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        print(f'---------TCPcleint side request processing---------')
        try:
            HOST = socket.gethostbyname("kposerver")
        except Exception as e:
            HOST = host
        try: 
            PORT = os.environ.get('SEND_PORT')
        except Exception as e:
            HOST = port            

        if not HOST: HOST = host
        if not PORT: PORT =  port
        print(f"Target host {HOST} and PORT is {PORT}")
        sock.connect((HOST, int(PORT)))
        
        
        byte_request = pickle.dumps(dict_request_data)
        # print(f'submit_request : dict_request_data:{dict_request_data}, type:{type(dict_request_data)}')
        #sending byte tsream to server
        print(f'Request is being submitted')
        sock.sendall(bytes(json.dumps(dict_request_data)+ "\n", "utf-8") ) 
        print(f'Request submitted')
        
        # Server response
        raw_received = []
        while True:
            print(f'\tReceiving response')
            #print(f'Received  1024:{t}')
            t = sock.recv(131072)
            print(f'\t\t Received  1024:{len(t)}')
            if t.strip() : raw_received.append(t)
            else: break
        received = json.loads(b''.join(raw_received))

 
        # print("Sent:     {}".format(dict_request_data))
        # print("Received: {}".format(received))
    print("sending Results to flask gunicorn") 
    return  received      


HOST, PORT = "127.0.0.1", 5000
# data = " ".join(sys.argv[1:])
my_pages = 25 * [
    "Fax Server 2/29/2022 (Li24:27 AM PAGE 1/010 Fax Server\r\n\r\nBLESSING\r\nPO Box 7005 + Quincy, IL 62305 * 217.223.8400\r\nHealth System blessinghealthorg Q@OOOO\r\n\r\nDate: 2/25/2022\r\n\r\nTo: WORK COMP LUDWIG From: Blessing Health System\r\n\r\nLocation: Department: Patient Financial Services\r\n\r\nFax Number: 866-767-3290\r\n\r\nImmediate Action: Yes\r\n\r\nNumber of Pages (including this page): 10\r\n\r\nMessage:\r\n\r\nPlease review and process\r\n\r\nThanks\r\n\r\nChell Threet CRCS.Account Specialist\r\nBlessing Hospital\r\n\r\nPFS Work comp\r\n\r\n217-223-8400 EXT 4189\r\n\r\nFax 217-223-9945\r\n\r\nBlessing Hospital \u00ab Hini Coramunity Hospital \u00bb Ble\r\n\r\nsing Physician Services \u00bb Hannibal Clinic * Derman Services\r\n\r\nBlessing-Rieman College of Nursing & Health Sciences * Blessing Foundation + Blessing Corporate Services\r\n\r\nCCOC/S C/O",
    "Fax Server 2/29/2022 (1:24:27 AM PAGE 8/010 Fax Server\r\n\r\nBlessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Result - Current Visit\r\nPatient Name: Ludwig, Candia $ Admit Date; 02/10/2022 Attending: Pimlott, Bryan J\r\nMRN: 000136426 Account Number: 4002-274362 Referring: Pimlotl, Bryan J\r\nDate of Birth: 06/01/1960 Discharge Date: 02/40/2022\r\nAge: 6ty Location: Radiology\r\nGender. Female\r\nRadiology\r\nDate/Time: 02/10/2022 15:07 Ordering Physician: Pimiott, Bryan J Order#: OO7NHJZXL\r\nProcedure. Fluoro Needle Loc/Biopsy/Aspirat a Ancillary#: OOTNHJZXL\r\nReason, Shoulder dislocation right initial encounter\r\nFluoro Needle Loc/Bicpsy/Aspirat Final Updated\r\n\r\nFINAL\r\n\r\nStudy Description: FL GUIDANCE ONLY FOR NEEDLE PLACEMENT\r\n\r\nORDERING HEALTHCARE PROVIDER: Bryan Pimiott\r\nClinical Indications: Right shoulder dislocation.\r\n\r\nProcedure: The procedure, risks, benefits, and complications of the procedure wereexplained fo the patient. Also discussed the\r\ntisk of bleeding, nerve damage, infection. The patient agreed to the procedure and expressed verbal understanding. All questions\r\nwere answered. Written consent was obtained and placed in patient's chart. The patient was placed supine on the table. Ascout\r\nview of the right shoulder was obtained for the purposes of localization. The patient's right shoulder was prepped and draped in\r\nusual sterile fashion. Lidocaine 1% was utilized for local anesthesia. Using an anterior approach and under direct fluoroscopic\r\nguidance, a 22-gauge spinal needle was introduced into the right glenohumeral joint space. This is then followed by a mixture of\r\n10 mL of Omnipaque, 5 mL of saline, \u00a7 mL of 1% lidocaine and 0.1 mL of Omniscan into the joint space. Atotal of 12 mL was\r\ninjected into the joint space. Hard copy of needie placement was obtained. The needle was removed and hemostasis achieved\r\n\r\nwith manual compression. Asterile dressing was applied. There was lessthan 2 ML blood loss. The patient tolerated the\r\nprocedure well without immediate postprecedural complications. The patient tolerated the procedure weil and was sent to MRI in\r\nstable condition.\r\n\r\nFluoroscopy time was 54 seconds, Total images 2. The mGy skin dose was 17.9.\r\nimpression: Technically successful fluoroscopic-guided right glenohumeral arthrogram.\r\nProcedure was performed by Sonya Krause, PA-C\r\n\r\nElectronically signed by. Mohammadali Mojarrad MD\r\n\r\nSigned Date/Time: 2/14/2022 8:45 AMCST\r\nWorkstation: 109-0432 TY6\r\n\r\nAccession Nbr. OO1NHJZXL\r\n\r\nDate/Time: 02/10/2022 15:50 Ordering Physician: Pimlott, Bryan J Order: OO7NHJZXR\r\nProcedure: MRI Shoulder Right w Contrast a Ancillary#: OOTNHIJZXR\r\nReason: Shoulder dislocation right initial encounter\r\nMRI Shoulder Right w Contrast Final\r\nFINAL\r\n\r\nEXAM: MRI Shoulder Right w Contrast\r\nRadLex MR SHOULDER WITH IV CONTRAST\r\n\r\nHISTORY: Shoulder dislocation right initial encounter.\r\n\r\nThe information contained in this report is confidential. If you have received this docurment in enor, please notify the Medical Records department.\r\n\r\nPrinted: 2/24/2022 2:03:08 PM Page: 1 of 3 Report: BHResult\r\nBlessing's Automated Record\r\n\r\nCCOC/S C/O",
    "Blessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Selected Document\r\npe akin Meiaih? Kauai SOE a OO \u2014\u2014e\u2014e\u2014eEeEeEeEeEeEeEEEEEe\r\nPatientName: Ludwig, Candia S Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/0141960 Oischarge Date: 03/02/2022\r\nAge: 61y Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\nODS Operative Report/Discharge Orders\r\n\r\nOate Of Service: 63-02-2022\r\n\r\nProce\r\nPhysician Dictation:\r\n\r\nDate af Surgery:\r\n\r\n3/2/2022\r\n\r\nPreoperative Diagnosis:\r\n\r\n1. Right shoulder rotator cuff tear.\r\n\r\n2. Right shoulder biceps tendinopathy.\r\n\r\n3. Right shoulder subacromial impingement.\r\n\r\n4. Right shoulder degenerative labral tear.\r\nPostoperative Diagnasis:\r\n\r\n1. same\r\n\r\nProcedure Performed:\r\n\r\n1. Right shoulder arthroscopic rotator cuff repair.\r\n2. Right shoulder arthroscopic biceps tenadesis\r\n\r\n3. Right shoulder arthroscopic subacromial decompression.\r\n4, Right shoulder arthroscopic limited debridement.\r\nSurgeon: Josue Acevedo, MD.\r\n\r\nAssistant: Ciara Glenn, PA,\r\n\r\nAnesthesia: General.\r\n\r\nAntibiotics: 2 g cefazolin fv.\r\n\r\nFluids: Crystailoid.\r\n\r\n| The information contained in this report is confidential. If you have raceived this document in error, please notify the Medical Recaris department.\r\n\r\nPrinted: 04/ 28/2022 Page: 1 of 6 Report: BHSelectedDocurrent\r\nBlessing'\u2019s Automated Racord\r\n\r\nOVd\r\n\r\nTTOT/80/80",
    "Blessing Hospital\r\n\r\n{ith & Broadway Quincy, tilinois 62305 (217) 223-1200 Selected Document\r\nPatientName: Ludwig, Candia S$ Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/01/1960 Discharge Date: 03/02/2022\r\nAge: 6ly Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\n008 Operative ReportDiecharge Orders .\r\n\r\nOate Of Service: 03-02-2022\r\n\r\nEstimated Blood Loss: Minimal.\r\n\r\nPositioning: Lateral Oecubitus.\r\n\r\nImplants:\r\n\r\n1, Arthrex 4.75mm PEEK SwiveLock Anchar (x5 }.\r\nSpecimens: None.\r\n\r\nComplications: None.\r\n\r\nFindings: Intra-operative: Right full thickness large supraspinatus L-shaped tear with retraction to the articular cartilage. Full-\r\nthickness superior subscapularis tendon tear. Lang head of the biceps intra-articular tendinopathy and tear. Degenerative\r\nanterior and inferior labral tears. Moderate sized subacromial spur, type ll. Glenohumeral articular cartilage was fairly intact.\r\n\r\nIndications: This is a 61 years old female with history of right shoulder pain with associated limited range of motion and\r\ndiagnosis of a rotator cuff tear. This was canfirmed on preoperative imaging. Initially, injuries were treated with non-\r\noperatively and the patient failed this treatment plan. It was then discussed in the office the option to undergo the procedure\r\nas listed above. The risks, benefits, and alternatives ta this procedure were descrihed ta the patient. Surgical risks include but\r\nare not limited to ratator cuff tendon re-tear, adhesive capsulitis. weakness, bleeding, damage to nerves, vessels, muscles,\r\ntendons, infection, DVT. pulmonary embolism. postoperative stiffness, postoperative pain. and need for future surgeries. All\r\nquestions were answered to their satisfaction, they elected to proceed with surgery. and subsequently siqned an informed\r\ncansent form.\r\n\r\nDescription of Pracedure:\r\n\r\nThe patient was identified in preoperative halding area by verbal name confirmation as well as name tag identification. The\r\nOperative site was marked with indelible ink as per protocol. They were taken to the operating roam, placed supine on the\r\noperating table, and anesthesia was induced. They were then carefully placed in the lateral decubitus pasitian on a bean bag.\r\nAll bony prominences were well padded and an axillary roll was placed. The operative extremity was prepped and draped in\r\nthe usual sterile fashion. Traction on the operative extremity was maintained using 10 pounds hanging from the arm\r\npositioner. 1% lidocaine with epinephrine was subcutaneously injected into the planned incision sites. Antibiotics were\r\nadministered prior ta beginning the procedure. A final time-out was taken where the surgeons involved, anesthesia. and\r\nsurgical staff were in agreement on the correct patient. operative site. and procedure to be perfarmed.\r\n\r\nThe information contained in this report s confidential. If you have received this document in error, please notify the Medical Records department.\r\n\r\nPrinted: 04/ 28/2022 Page: 2 of 6 Report: BHSelectedDocurent\r\nBlessing\u2019s Automated Record\r\n\r\nOVd\r\n\r\nTTOT/80/80"
]
d = { 'id': "1",
 'client':"name",
 'pages' : my_pages,
 'config':{ 'category' : True, 'segmenter' : True,'spacy_' : False,'qa':False}
 }

# submit_request(dict_request_data = d,HOST="127.0.0.1", PORT=9002)
# d_str = json.dumps(d)
# print(d_str)
# # Create a socket (SOCK_STREAM means a TCP socket)
# print("connecting to locatl host")
if __name__ == "__main__":
    submit_request(dict_request_data = d,HOST="127.0.0.1", PORT=5000)

