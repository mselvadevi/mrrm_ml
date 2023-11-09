import os, numpy as np, json
import transformers
from transformers import AutoModel, BertTokenizerFast, BertForSequenceClassification, BertTokenizer
import spacy, torch, datetime
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"device is :{device}")
# device = 'cuda'
device="cuda:0"
import os, sys
import general_utilities
import time
#import git
os.environ['TZ'] = "Asia/Kolkata"

if os.name == 'nt':
    os_name = "windows"
else:
    os_name = "linux"
    
    
my_pages =[
    "Fax Server 2/29/2022 (Li24:27 AM PAGE 1/010 Fax Server\r\n\r\nBLESSING\r\nPO Box 7005 + Quincy, IL 62305 * 217.223.8400\r\nHealth System blessinghealthorg Q@OOOO\r\n\r\nDate: 2/25/2022\r\n\r\nTo: WORK COMP LUDWIG From: Blessing Health System\r\n\r\nLocation: Department: Patient Financial Services\r\n\r\nFax Number: 866-767-3290\r\n\r\nImmediate Action: Yes\r\n\r\nNumber of Pages (including this page): 10\r\n\r\nMessage:\r\n\r\nPlease review and process\r\n\r\nThanks\r\n\r\nChell Threet CRCS.Account Specialist\r\nBlessing Hospital\r\n\r\nPFS Work comp\r\n\r\n217-223-8400 EXT 4189\r\n\r\nFax 217-223-9945\r\n\r\nBlessing Hospital \u00ab Hini Coramunity Hospital \u00bb Ble\r\n\r\nsing Physician Services \u00bb Hannibal Clinic * Derman Services\r\n\r\nBlessing-Rieman College of Nursing & Health Sciences * Blessing Foundation + Blessing Corporate Services\r\n\r\nCCOC/S C/O",
    "Fax Server 2/29/2022 (1:24:27 AM PAGE 8/010 Fax Server\r\n\r\nBlessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Result - Current Visit\r\nPatient Name: Ludwig, Candia $ Admit Date; 02/10/2022 Attending: Pimlott, Bryan J\r\nMRN: 000136426 Account Number: 4002-274362 Referring: Pimlotl, Bryan J\r\nDate of Birth: 06/01/1960 Discharge Date: 02/40/2022\r\nAge: 6ty Location: Radiology\r\nGender. Female\r\nRadiology\r\nDate/Time: 02/10/2022 15:07 Ordering Physician: Pimiott, Bryan J Order#: OO7NHJZXL\r\nProcedure. Fluoro Needle Loc/Biopsy/Aspirat a Ancillary#: OOTNHJZXL\r\nReason, Shoulder dislocation right initial encounter\r\nFluoro Needle Loc/Bicpsy/Aspirat Final Updated\r\n\r\nFINAL\r\n\r\nStudy Description: FL GUIDANCE ONLY FOR NEEDLE PLACEMENT\r\n\r\nORDERING HEALTHCARE PROVIDER: Bryan Pimiott\r\nClinical Indications: Right shoulder dislocation.\r\n\r\nProcedure: The procedure, risks, benefits, and complications of the procedure wereexplained fo the patient. Also discussed the\r\ntisk of bleeding, nerve damage, infection. The patient agreed to the procedure and expressed verbal understanding. All questions\r\nwere answered. Written consent was obtained and placed in patient's chart. The patient was placed supine on the table. Ascout\r\nview of the right shoulder was obtained for the purposes of localization. The patient's right shoulder was prepped and draped in\r\nusual sterile fashion. Lidocaine 1% was utilized for local anesthesia. Using an anterior approach and under direct fluoroscopic\r\nguidance, a 22-gauge spinal needle was introduced into the right glenohumeral joint space. This is then followed by a mixture of\r\n10 mL of Omnipaque, 5 mL of saline, \u00a7 mL of 1% lidocaine and 0.1 mL of Omniscan into the joint space. Atotal of 12 mL was\r\ninjected into the joint space. Hard copy of needie placement was obtained. The needle was removed and hemostasis achieved\r\n\r\nwith manual compression. Asterile dressing was applied. There was lessthan 2 ML blood loss. The patient tolerated the\r\nprocedure well without immediate postprecedural complications. The patient tolerated the procedure weil and was sent to MRI in\r\nstable condition.\r\n\r\nFluoroscopy time was 54 seconds, Total images 2. The mGy skin dose was 17.9.\r\nimpression: Technically successful fluoroscopic-guided right glenohumeral arthrogram.\r\nProcedure was performed by Sonya Krause, PA-C\r\n\r\nElectronically signed by. Mohammadali Mojarrad MD\r\n\r\nSigned Date/Time: 2/14/2022 8:45 AMCST\r\nWorkstation: 109-0432 TY6\r\n\r\nAccession Nbr. OO1NHJZXL\r\n\r\nDate/Time: 02/10/2022 15:50 Ordering Physician: Pimlott, Bryan J Order: OO7NHJZXR\r\nProcedure: MRI Shoulder Right w Contrast a Ancillary#: OOTNHIJZXR\r\nReason: Shoulder dislocation right initial encounter\r\nMRI Shoulder Right w Contrast Final\r\nFINAL\r\n\r\nEXAM: MRI Shoulder Right w Contrast\r\nRadLex MR SHOULDER WITH IV CONTRAST\r\n\r\nHISTORY: Shoulder dislocation right initial encounter.\r\n\r\nThe information contained in this report is confidential. If you have received this docurment in enor, please notify the Medical Records department.\r\n\r\nPrinted: 2/24/2022 2:03:08 PM Page: 1 of 3 Report: BHResult\r\nBlessing's Automated Record\r\n\r\nCCOC/S C/O",
    "Blessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Selected Document\r\npe akin Meiaih? Kauai SOE a OO \u2014\u2014e\u2014e\u2014eEeEeEeEeEeEeEEEEEe\r\nPatientName: Ludwig, Candia S Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/0141960 Oischarge Date: 03/02/2022\r\nAge: 61y Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\nODS Operative Report/Discharge Orders\r\n\r\nOate Of Service: 63-02-2022\r\n\r\nProce\r\nPhysician Dictation:\r\n\r\nDate af Surgery:\r\n\r\n3/2/2022\r\n\r\nPreoperative Diagnosis:\r\n\r\n1. Right shoulder rotator cuff tear.\r\n\r\n2. Right shoulder biceps tendinopathy.\r\n\r\n3. Right shoulder subacromial impingement.\r\n\r\n4. Right shoulder degenerative labral tear.\r\nPostoperative Diagnasis:\r\n\r\n1. same\r\n\r\nProcedure Performed:\r\n\r\n1. Right shoulder arthroscopic rotator cuff repair.\r\n2. Right shoulder arthroscopic biceps tenadesis\r\n\r\n3. Right shoulder arthroscopic subacromial decompression.\r\n4, Right shoulder arthroscopic limited debridement.\r\nSurgeon: Josue Acevedo, MD.\r\n\r\nAssistant: Ciara Glenn, PA,\r\n\r\nAnesthesia: General.\r\n\r\nAntibiotics: 2 g cefazolin fv.\r\n\r\nFluids: Crystailoid.\r\n\r\n| The information contained in this report is confidential. If you have raceived this document in error, please notify the Medical Recaris department.\r\n\r\nPrinted: 04/ 28/2022 Page: 1 of 6 Report: BHSelectedDocurrent\r\nBlessing'\u2019s Automated Racord\r\n\r\nOVd\r\n\r\nTTOT/80/80",
    "Blessing Hospital\r\n\r\n{ith & Broadway Quincy, tilinois 62305 (217) 223-1200 Selected Document\r\nPatientName: Ludwig, Candia S$ Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/01/1960 Discharge Date: 03/02/2022\r\nAge: 6ly Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\n008 Operative ReportDiecharge Orders .\r\n\r\nOate Of Service: 03-02-2022\r\n\r\nEstimated Blood Loss: Minimal.\r\n\r\nPositioning: Lateral Oecubitus.\r\n\r\nImplants:\r\n\r\n1, Arthrex 4.75mm PEEK SwiveLock Anchar (x5 }.\r\nSpecimens: None.\r\n\r\nComplications: None.\r\n\r\nFindings: Intra-operative: Right full thickness large supraspinatus L-shaped tear with retraction to the articular cartilage. Full-\r\nthickness superior subscapularis tendon tear. Lang head of the biceps intra-articular tendinopathy and tear. Degenerative\r\nanterior and inferior labral tears. Moderate sized subacromial spur, type ll. Glenohumeral articular cartilage was fairly intact.\r\n\r\nIndications: This is a 61 years old female with history of right shoulder pain with associated limited range of motion and\r\ndiagnosis of a rotator cuff tear. This was canfirmed on preoperative imaging. Initially, injuries were treated with non-\r\noperatively and the patient failed this treatment plan. It was then discussed in the office the option to undergo the procedure\r\nas listed above. The risks, benefits, and alternatives ta this procedure were descrihed ta the patient. Surgical risks include but\r\nare not limited to ratator cuff tendon re-tear, adhesive capsulitis. weakness, bleeding, damage to nerves, vessels, muscles,\r\ntendons, infection, DVT. pulmonary embolism. postoperative stiffness, postoperative pain. and need for future surgeries. All\r\nquestions were answered to their satisfaction, they elected to proceed with surgery. and subsequently siqned an informed\r\ncansent form.\r\n\r\nDescription of Pracedure:\r\n\r\nThe patient was identified in preoperative halding area by verbal name confirmation as well as name tag identification. The\r\nOperative site was marked with indelible ink as per protocol. They were taken to the operating roam, placed supine on the\r\noperating table, and anesthesia was induced. They were then carefully placed in the lateral decubitus pasitian on a bean bag.\r\nAll bony prominences were well padded and an axillary roll was placed. The operative extremity was prepped and draped in\r\nthe usual sterile fashion. Traction on the operative extremity was maintained using 10 pounds hanging from the arm\r\npositioner. 1% lidocaine with epinephrine was subcutaneously injected into the planned incision sites. Antibiotics were\r\nadministered prior ta beginning the procedure. A final time-out was taken where the surgeons involved, anesthesia. and\r\nsurgical staff were in agreement on the correct patient. operative site. and procedure to be perfarmed.\r\n\r\nThe information contained in this report s confidential. If you have received this document in error, please notify the Medical Records department.\r\n\r\nPrinted: 04/ 28/2022 Page: 2 of 6 Report: BHSelectedDocurent\r\nBlessing\u2019s Automated Record\r\n\r\nOVd\r\n\r\nTTOT/80/80"
]

def batch_files_put_pull(ENVIRON="/DEV",hostname='prelsftp.preludesys.com',username='SFTP_AI-ML', password='M{\^SJ:FA$0*&L)',port=2332
                        ):
    start = datetime.datetime.now()
    with open("/LOGS/sftp_logs.txt","a") as fp:
        fp.write(f'\nFTP Process started {start} \n Connecting to SFTP server')
    from paramiko.client import SSHClient
    import paramiko
    import os
    client = SSHClient()
    # client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='prelsftp.preludesys.com',username='SFTP_AI-ML', password='M{\^SJ:FA$0*&L)',port=2332)
    # stdin, stdout, stderr = client.exec_command('ls -l')
    while  True:
        with client.open_sftp() as sftp:
            with open("/LOGS/sftp_logs.txt","a") as fp:
                fp.write(f'\nConnected to FTP server {datetime.datetime.now()}')
            print("sftp established")
            # ENVIRON = os.environ.get('ENVIRON')
            print('ENVIRON',ENVIRON)
            # ENVIRON = "/DEV"
            dir_ = 'TO_KPO'
            files = [ file for file in sftp.listdir(os.path.join(ENVIRON,dir_)) if file.endswith('.json')]
            with open("/LOGS/sftp_logs.txt","a") as fp:
                fp.write(f'\nList of Files tobe copied form SFTP {files}')
            print(f'List of Files tobe copied form SFTP {files}')
            for file in files:
                print(f'Processing File {file}')
                remote_abs_file = os.path.join(ENVIRON,dir_,file)
                if file.startswith('Train_'):
                    _dir = '/MODELS/KPO/TRG_SOURCE_DIR'
                elif file.startswith('Predict_'):
                    _dir = '/MODELS/KPO/SOURCE_INFERENCE'
                else:
                    with open("/LOGS/sftp_logs.txt","a") as fp:
                        fp.write(f'\n{remote_abs_file} neither train nor predict service file')                    
                    continue
                local_abs_file = os.path.join(_dir,file)
                sftp.get(remote_abs_file,local_abs_file)
                print(f'{remote_abs_file} has been downloaded to VM server')
                with open("/LOGS/sftp_logs.txt","a") as fp:
                    fp.write(f'\n{remote_abs_file} Copied from SFTP Server to {local_abs_file}')
                sftp.remove(remote_abs_file)
                print(f'{remote_abs_file} deleted from SFTP server')
            predicted_dir = '/MODELS/KPO/PREDICTED_INFERENCE'
            send_files = [ file for file in os.listdir(predicted_dir) if file.endswith('.json') ]
            print(f'List of Files to be copied to SFTP {send_files}')
            for file in send_files:
                print(f'Processing File {file}')
                local_abs_file = os.path.join(predicted_dir,file)
                dir_ = 'FROM_KPO'
                remote_abs_file = os.path.join(ENVIRON,dir_,file)
                sftp.put(local_abs_file,remote_abs_file)
                with open("/LOGS/sftp_logs.txt","a") as fp:
                    fp.write(f'\nPRedicted Results {remote_abs_file} Copied to SFTP Server ')                
                os.remove(local_abs_file)
            time.sleep(5*60)
    


def load_label_dict(abs_file_name):
    label_path = abs_file_name
    print(f"label_path:{abs_file_name}")
    if os.path.isfile( label_path)  :
      print(f"\t {label_path} exists")
      with open(label_path,"r") as fp:
        label_dict = json.load(fp)
    else:
        print(f"\t {label_path} does not exists")
        label_dict = None
    if label_dict:
      if 1==1:
        t ={}
        for key,value in label_dict.items():
          if isinstance(key,np.bool_):
            t[bool(key)] = value
          else:
            t[key] = value

        label_dict = t

    print(label_dict)
    return label_dict     

def intitialize_tokenizers_raw(tokenizer_name="bert-base-uncased",max_length=512,
                               tokenizer_instance = BertTokenizer,location = None,): 
    if os.path.exists(location):
        tokenizer = tokenizer_instance.from_pretrained(location)
        print(f"Loaded tokenizer from {location}")
    else:
        tokenizer = tokenizer_instance.from_pretrained(tokenizer_name, max_length = max_length ,
                                                  # model_max_length = max_length,
                                                  do_lower_case=True )
    return tokenizer    

def load_model(model_path,label_dict,cpu_status = device,model_check_point = 'bert-base-uncased',num_labels=20):
    label_dict_map = { int(value):key for key,value in label_dict.items()}
    model = BertForSequenceClassification.from_pretrained(model_check_point,
                                                          num_labels=num_labels,
                                                          output_attentions=False,
                                                          output_hidden_states=False,
                                                         )

    
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)), strict=False)
    model = model.to(device)
    return  model
model_store_dir =r""
save_model_name =r""
max_length = 512
robert_qa_model_name = "roberta-base-squad2"
repo_url = "https://huggingface.co/deepset/roberta-base-squad2"
if os_name == "linux":
    location = f'{os.sep}MODELS{os.sep}KPO'
    qa_config_file_path = f'{location}{os.sep}qa_config.json'
    robert_qa_model_path = f'{location}{os.sep}{robert_qa_model_name}'
    source_json_inference = f'{location}{os.sep}SOURCE_INFERENCE'
    predicted_json_inference = f'{location}{os.sep}PREDICTED_INFERENCE'
    
    if not os.path.exists(robert_qa_model_path):
        local_repo_target= robert_qa_model_path
        print(f'Repository {repo_url} is being cloned into {local_repo_target}')
        #repo = git.Repo.clone_from(repo_url, local_repo_target)
        print(f'Repository Cloned at location: {local_repo_target}')
    else:
        print(f'Repository : {robert_qa_model_path} exists')
else:
    win_home = r'C:\Users\murugesan_r\OneDrive - Prelude Systems Inc\PRELUDESYS\GITHUB\KPO'
    location = f'MODELS{os.sep}FINAL'
    qa_config_file_path = "qa_config.json"
    robert_qa_model_path = f'{location}{os.sep}{robert_qa_model_name}'
    source_json_inference = f'{win_home}{os.sep}{location}{os.sep}SOURCE_INFERENCE'
    predicted_json_inference = f'{win_home}{os.sep}{location}{os.sep}PREDICTED_INFERENCE'
    
    if not os.path.exists(robert_qa_model_path):
        local_repo_target= robert_qa_model_path
        print(f'Repository {repo_url} is being cloned into {local_repo_target}')
        local_repo_target= robert_qa_model_path
        #repo = git.Repo.clone_from(repo_url, local_repo_target)
        print(f'Repository Cloned at location: {local_repo_target}')
    else:
        print(f'Repository : {robert_qa_model_path} exists')
    
tokenizer_path = f'{location}{os.sep}Classfication_PAGE_CATEGORY_512_BERT_BOUNDRY_PRE_TRAIN_512_tokenizer'
model_path = f'{location}{os.sep}Classfication_PAGE_CATEGORY_512_BERT_BOUNDRY_PRE_TRAIN.model'
abs_label_path = f'{location}{os.sep}PAGE_CATEGORY_ImageText_label_dict.json'
model_checkpoint ="bert-base-uncased"
def category_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=20,device =device):
    label_dict  = load_label_dict(abs_label_path)
    tokenizer = intitialize_tokenizers_raw(tokenizer_name= model_checkpoint, 
                                               max_length=max_length,tokenizer_instance = BertTokenizer,
                                               location= tokenizer_path)
    model = load_model(model_path,label_dict,cpu_status = device,model_check_point = 'bert-base-uncased',num_labels=20)
    pipe = transformers.pipeline(task="text-classification",model=model,tokenizer=tokenizer,device=device,config=model.config)
    return pipe,label_dict
def segmenter_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=20,device =device):
    label_dict  = load_label_dict(abs_label_path)
    tokenizer = intitialize_tokenizers_raw(tokenizer_name= model_checkpoint, 
                                               max_length=max_length,tokenizer_instance = BertTokenizer,
                                               location= tokenizer_path)
    model = load_model(model_path,label_dict,cpu_status = device,model_check_point = 'bert-base-uncased',num_labels=2)
    pipe = transformers.pipeline(task="text-classification",model=model,tokenizer=tokenizer,device=device,config=model.config)
    return pipe,label_dict
pipe,label_dict_category = category_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=20,device =device)

tokenizer_path = f'{location}{os.sep}Classfication_PAGE_SEGMENTER_512_BERT_BOUNDRY_PRE_TRAIN_512_tokenizer'
model_path = f'{location}{os.sep}Classfication_PAGE_SEGMENTER_512_BERT_BOUNDRY_PRE_TRAIN.model'
abs_label_path = f'{location}{os.sep}PAGE_SEGMENTER_ImageText_label_dict.json'

segmenter_pipe,label_dict_segmenter = segmenter_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=2,device =device)


tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}

result_set = {}

def predict_category(pages,label_dict = label_dict_category):
    start = datetime.datetime.now()
    print("Categerizer")
    
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}
    id2label = {'LABEL_' + str(value) : key for key, value in label_dict.items() }
    # print(id2label)
    result = pipe(pages,**tokenizer_kwargs)
    label_result = [ id2label.get( _.get('label') ) for _ in result ]
    # print(result)
    # print(label_result)
    end = datetime.datetime.now()
    print(f'Categerizer Time taken :{end -start}')       
    result_set['category'] = label_result
    return label_result

def predict_segment(pages,label_dict=label_dict_segmenter):
    start = datetime.datetime.now()
    print("Segmenter")    
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}
    id2label = {'LABEL_' + str(value) : key for key, value in label_dict.items() }
    # print(id2label)
    result = segmenter_pipe(pages,**tokenizer_kwargs)
    label_result = [ id2label.get( _.get('label') ) for _ in result ]
    # print(result)
    # print(label_result)
    end = datetime.datetime.now()
    result_set['segmenter'] = label_result
    print(f'Segmenter Time taken :{end -start}')    
    return label_result


import spacy
import os, json
#spacy.require_gpu()
spacy.prefer_gpu()
nlp=spacy.load('en_core_web_trf',enable=["ner"])
print("Models loaded")
#ruler = nlp.add_pipe("entity_ruler",after='ner')
text_file_path= r"provider.jsonl"
# ruler=nlp.add_pipe("entity_ruler").from_disk(text_file_path)

from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
model_name = "roberta-base-squad2"
robert_qa_model_name = "roberta-base-squad2"
roberta_qa_model = AutoModelForQuestionAnswering.from_pretrained(robert_qa_model_path)
roberta_qa_tokenizer = AutoTokenizer.from_pretrained(robert_qa_model_path)
qa_extraction_pipe = pipeline('question-answering', model=robert_qa_model_path, tokenizer=robert_qa_model_path, device = device)
# predict_category(my_pages,label_dict)       
# predict_segment(my_pages,label_dict_segmenter)   
def entity_extract(pages,label_dict=None):
    start = datetime.datetime.now()
    print("SPACY ENITY")        
    if isinstance(pages,str):
        doc = nlp(pages)
        org = [ ent.text for ent in doc.ents if ent.label_ =='ORG' ]
        return [org]
    else:
        _ = []
        for page in pages:
            doc = nlp(page)   
            org = []
            for ent in doc.ents:
                if ent.label_ =='ORG':
                    org = [ent.text]
                    print(f'org:{org}')
                    break
            _.append(org)
    end = datetime.datetime.now()
    print(f'SPACY ENITY Time taken :{end - start}')        
    result_set['ORG'] = _
    return _




def extract_qa(pages,label_dict=None):
    start = datetime.datetime.now()
    print("QA")       
    service_date = ["what is the Date of Service?",
                   "what is the Visit Date?",
                    "what is SVC date?",
                    "what is Encounter Date?",
                   ]
    patient_name = [
        "what is patient name?",
                   "what is patient?",
                    "what is patient or patient name?"

                   ]
    hospital = ["what is hospital or facility or medical center?",
               "what is the facility?",
               "what is  the medical center?",
               "what is hospital or facility or medical center?"]
    
    service_date = ["Date of Service",
                    "Service",
                   "Visit Date",
                    "SVC date",
                    "Encounter Date",
                   ]
    patient_name = ["patient name",
                    "patientname",
                   "patient",


                   ]
    hospital = ["hospital",
               "facility",
               "medical center",
                "medicalcenter"
                ]
    data =None
    with open(qa_config_file_path,"r") as fp:
        print(f'loading config data from file:{qa_config_file_path}')
        data = json.load(fp)
    if data:
        service_date = data.get('service_date')
        patient_name = data.get('patient_name')
        hospital = data.get('hospital')
    service_date  = [ question.lower() for question in service_date]
    questions = {
    "patient_name":patient_name,
    "service_date" : service_date,
    "provider" :hospital
    }
    
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,'return_tensors':'pt'}
 
    if isinstance(pages,str):
        pages = pages.lower()
        t= {"patient_name":"","service_date":"","provider":"" }
        for key,question in questions.items():
            for quest in question:
                quest = quest.lower()
                if pages.find(quest) == -1: continue
                QA_input = {'question':"what is the " + quest,
                        'context': pages
                        }
                result  = qa_extraction_pipe(QA_input, **tokenizer_kwargs)
                if result:
                    if quest.find(result.get('answer') ) == -1:
                        t[key] = result.get('answer')
                        break
        end = datetime.datetime.now()
        print(f'QA ENITY Time taken :{end - start}')           
        return [t]
    else:
        _ = []
        for page in pages:
            page = page.lower()
            t= {"patient_name":"","service_date":"","provider":"" }
            for key,question in questions.items():
                # print("questions:",question)
                for quest in question:
                    quest = quest.lower()
                                     
                    if page.find(quest) == -1: continue
                    quest = "what is the " + quest
                    # print("quest:",quest)   
                    QA_input = {'question':quest,
                                
                            'context': page
                            }
                    result  = qa_extraction_pipe(QA_input, **tokenizer_kwargs)
                    # print(result)
                    if result:
                        if quest.find(result.get('answer') ) == -1:
                            t[key] = result.get('answer')
                            break            

            _.append(t)
        end = datetime.datetime.now()
        print(f'QA ENITY Time taken :{end - start}')   
        result_set['DATE'] = _
        return _    
# extract_qa(my_pages)   

import threading
import concurrent.futures
import threading
import concurrent.futures
import re
def process_pages(my_pages,batch_number=0,category=True,segmenter=True,spacy_=True,qa=True):
    print(f'batch_number:{batch_number}, {len(my_pages)}')
    page_no = [ i+1 for i in range(batch_number,batch_number+len(my_pages) )]
    print(f'Page nos :{len(my_pages)} ')
    global result_set
    start = datetime.datetime.now()
    print(f'{batch_number+1} th batch process_pages Started at :{start}')
    print(f'Number of Pages : {len(my_pages)}')
    from concurrent.futures import ThreadPoolExecutor
    _ = []
    with ThreadPoolExecutor() as executor:
        
        print("Started Threading")
        no_process = len(my_pages) * [-1]
        category_predicted = len(my_pages) * [-1]
        segment_predicted = len(my_pages) * [-1]
        org_predicted = len(my_pages) * [-1]
        provider_predicted = len(my_pages) * [-1]
        # print(f'Non thread predicted :strts')
        # x = predict_category(my_pages,label_dict_category)
        # print(f'Non thread predicted :{x}')
        if category:
            th_category = executor.submit(predict_category, my_pages,label_dict_category)

        if segmenter:
            th_segment = executor.submit(predict_segment, my_pages,label_dict_segmenter)
            
        if spacy_:
            th_spacy_provider= executor.submit(entity_extract, my_pages)
            
        if qa:
            th_qa_provider = executor.submit(extract_qa, my_pages)
            
        if category:
            category_predicted = th_category.result()
        if segmenter:
            segment_predicted = th_segment.result()
        if spacy_:
            org_predicted = th_spacy_provider.result()
        if qa:
            provider_predicted = th_qa_provider.result()
            pattern = re.compile("^[0-9]{1}[0-9]?[-/][0-9]{1}[0-9]?[-/][0-9][0-9][0-9][0-9]$")
            for _per_page in provider_predicted:
                if not pattern.fullmatch( _per_page.get('service_date') ):
                    _per_page['service_date'] = ''

        print(f'category_predicted: {category_predicted}')
        for i,j,k,m,p in zip(category_predicted,org_predicted,provider_predicted,segment_predicted,page_no):
            t = {'page_number' :p, 
                'category' : i,
                 'segment': m,
                  'ORG' : j,
                  'info' : k
                }
            _.append(t)        
    end = datetime.datetime.now()
    print(f'{batch_number+1} th batch process_pages Ended at:{end} and  Time taken is :{end -start}')
    return _
import datetime


def json_generator_fn(my_pages,step_size=10):
    _size =  len(my_pages)
    print(f'input len {_size} and step size is {step_size}')
    for i in range(0,_size,step_size):
        print("\tforloop:",i,i+step_size,type(my_pages),sep="#")
        yield my_pages[i:i+step_size]
        # yield my_pages[i:step_size]
my_p = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
def batch_json(my_pages,step_size=10,category=True,segmenter=True,spacy_=True,qa=True):

    result_set =[]
    # step_size = int(len(my_pages)/1000) if len(my_pages) > 1000 else round(int(len(my_pages)/10))
    if step_size<=0: step_size=len(my_pages)
    if step_size> len(my_pages): step_size=len(my_pages) 
    if step_size < 100 and len(my_pages) >=100: 
        step_size=100
        print(f'---------------- STEP SIZE is {step_size}-----------')
    step_size = len(my_pages) 
    input_generator = json_generator_fn(my_pages,step_size)
    
    for i in range(0,int(len(my_pages)),step_size):
        print(f'Batch number {i+1}')
        re_ = process_pages(next(input_generator),i,category,segmenter,spacy_,qa)
        # print("re_:",re_)
        result_set.extend(re_   )
    return result_set
# from MODELS 

def process_dir(source_dir=source_json_inference,target_dir=predicted_json_inference):
    while  True:
        orig_stdout = sys.stdout
        json_file_list = [ file for file in os.listdir(source_dir) if file.endswith(".json")]
        print(f' source_json_inference List of files:{json_file_list}')
        if not json_file_list:
            time.sleep(300)
            continue
        for file in json_file_list:
            dt_ = f'{datetime.datetime.now():%Y-%m-%d_H_%M_%S}'
            try:
                with open(f'/LOGS/process_dir/{ os.path.basename(file)}_{dt_}.logs',"a") as fp:
                    
                    sys.stdout = fp
                    print(f'Processing File : {file}')
                    json_file_content = general_utilities.load_json(source_dir,file)
                    my_pages = json_file_content.get('pages')
                    config = json_file_content.get('config')
                    if not config : 
                        config = { "category":True,"segmenter":True,"spacy_" :True,"qa" : True } 
                    # config['step_size']= 10
                    try:
                        # result_set = batch_json(my_pages=my_pages,**config)
                        start = datetime.datetime.now()
                        result_set = process_pages(my_pages=my_pages,**config)
                        if os.path.isfile(os.path.join(os.path.join(source_dir,file+"l"))):
                            print(f'Deleting file {os.path.join(source_dir,file+"l")}')
                            os.remove(os.path.join(source_dir,file+"l"))
                            print(f'Deleted file {os.path.join(source_dir,file+"l")}')
                            
                        with open(os.path.join(target_dir,file),"w" ) as fout:
                            print(f'storing results to {os.path.join(target_dir,file)}')
                            json.dump(result_set,fout,indent=2)
                            print(f'Success storeing results  to {os.path.join(target_dir,file)}')
                            print(type(result_set),result_set,sep=" # ")
                            
                            print(f'Results are stored at {os.path.join(target_dir,file) }')
                            os.rename(os.path.join(source_dir,file),os.path.join(source_dir,file+"l") )
                            print(f'Renameing file {os.path.join(source_dir,file)}  to {os.path.join(source_dir,file+"l")} ')
                        with open(os.path.join(location,"source_inference_logs.txt"), "a") as flogs:
                            flogs.write( f' {os.path.join(source_dir,file)} Started at {start} and Completed at {datetime.datetime.now()}\n' )
                    except Exception as e:
                        with open(os.path.join(location,"source_inference_logs.txt"), "a") as flogs:
                            flogs.write( f' {os.path.join(source_dir,file)} Exception at {datetime.datetime.now()} Excepton is {str(e)}\n' )

            except Exception as e:
                sys.stdout = orig_stdout
                with open(os.path.join(location,"source_inference_logs.txt"), "a") as flogs:
                    flogs.write( f' {os.path.join(source_dir,file)} Exception at outer try {datetime.datetime.now()} Excepton is {str(e)}\n' )            

            finally:
                sys.stdout = orig_stdout
        
    return

# print(process_pages(my_pages))
