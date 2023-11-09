#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import pandas as pd, os, re

import numpy as np
import torch, random
import torch.nn as nn
import transformers
from transformers import AutoModel, BertTokenizerFast, BertForSequenceClassification, BertTokenizer

import random

from transformers import pipeline
import json, os
from transformers import BertConfig
from transformers import AutoTokenizer,  AutoModelForSequenceClassification



# In[ ]:


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# In[ ]:


MODEL_STORE = r"./MODELS/"


# In[ ]:


os.listdir(MODEL_STORE)


# In[ ]:


lable_dict_file = r"PAGE_CLASSIFIER_label_dict.json"
model_file = r"Classfication_PAGE_CLASSIFIER_512_5_BERT_BOUNDRY_FINE_TUNE_512_5_17-04-23_07_53_13.model"
label_dict = None
# model_path = load_model_dir
# save_model_name = load_model_name

model_check_point = 'bert-base-uncased'
task="text-classification"


# In[ ]:


def load_label_dict(file ):
    with open(file, "r" )  as fp:
        label_dict = json.load(fp)
        label_dict_map = { "LABEL_" + str(j)  : i for i,j in label_dict.items() }
        print(label_dict,label_dict_map)
    return label_dict, label_dict_map 
label_dict,label_dict_map = load_label_dict(os.path.join(MODEL_STORE, lable_dict_file) )


# In[ ]:


def load_pipe(label_dict,model_path, model_file_name, model_check_point = 'bert-base-uncased'):
    tokenizer = BertTokenizer.from_pretrained(model_check_point, 
                                              do_lower_case=True)
    model = BertForSequenceClassification.from_pretrained(model_check_point,
                                                          num_labels=len(label_dict),
                                                          output_attentions=False,
                                                          output_hidden_states=False, from_tf=False)
    
    # model = BertForSequenceClassification.from_pretrained(os.path.join(model_path, model_file_name))
    model.load_state_dict(torch.load(os.path.join(model_path, model_file_name), map_location=torch.device(device)), )
    pipe = pipeline(task, model = model, tokenizer = tokenizer,device = device)
    return pipe
pipe = load_pipe(label_dict,model_path = MODEL_STORE, model_file_name = model_file, model_check_point = 'bert-base-uncased')


# In[ ]:


def load_model(model_path,label_dict,cpu_status = device,model_check_point = 'bert-base-uncased'):
    label_dict = load_label_dict(model_store_dir = model_store_dir )
    tokenizer = BertTokenizer.from_pretrained(model_check_point, 
                                              do_lower_case=True)
    model = BertForSequenceClassification.from_pretrained(model_check_point,
                                                          num_labels=len(label_dict),
                                                          output_attentions=False,
                                                          output_hidden_states=False)

    
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    model.to(device)
    pipe = pipeline(task, model = model, tokenizer = tokenizer,device = 'cpu')
    # model.load_state_dict(torch.load(model_path))
    return tokenizer, model,

from transformers import pipeline
def model_inference(model_path,save_model_name, labels_json_file, model_check_point, task,device):
    abs_model_file = os.path.join(model_path,save_model_name)
    abs_label_file = os.path.join(model_path,labels_json_file)
    # tokenizer, model = load_model(abs_model_file,cpu_status = device)
    print("device:",device)
    label_dict = load_label_dict(abs_label_file)
    tokenizer, model = load_model(abs_model_file,label_dict = label_dict,cpu_status = device,model_check_point=model_check_point)
    
    model.to(device)
    pipe = pipeline(task, model = model, tokenizer = tokenizer,device = 'cpu')
    return pipe,label_dict 
label_dict = None
# model_path = load_model_dir
# save_model_name = load_model_name

model_check_point = 'bert-base-uncased'
task="text-classification"
# pipe = model_inference(model_path,save_model_name,labels_json_file, model_check_point = model_check_point,task = task)               


# In[ ]:


# print(f'label_class:{label_dict}')
# print(f'org{my_text_page_category} with pages {my_text_page_no}')
# res_1 = pipe(my_text_page_text,padding=True, truncation=True)
# # res_2 = ImageText_Non_Blank_restrict_line_tokens_3_pipe(my_text_page_text,padding=True, truncation=True)
# print(f'res1:{res_1}')
# # print(f'res2:{res_2}')


# In[ ]:


def map_predictions(my_text):
    print(f' map_predictions: ,{type(my_text)}')
    my_text_page_no = [j for k in my_text for i,j in k.items() if i == "pagenumber" ]
    my_text_page_text = [j[0] for k in my_text for i,j in k.items() if i == "ImageText" ]
    
    # print(f'{my_text_page_no},\n ,\n {my_text_page_text}')
    
    res = pipe(my_text_page_text,padding=True, truncation=True)
    mapped_ =[]
    for i_ in res:
        mapped_.append( label_dict_map.get ( i_.get('label')  ) )
    print(mapped_)
    return mapped_
map_predictions(my_text)   


# In[ ]:


from flask import Flask, request,jsonify
server = Flask(__name__)


# In[ ]:


@server.route("/kpo/hello", methods=['GET','POST'])
def hello():
    return "<h1 style='color:blue'>Hello There welcome!</h1>"


# In[39]:


@server.route('/kpo/parse', methods=['POST'])
def parse_json_transcript():
    try:
        content_type = request.headers.get('Content-Type')
        try:
            content = request.json 
            print(f'content:{content} and type is:{type(content)}')
            content_json = json.dumps(content)
            print(f'content_json:{content_json} and {type(content_json) }')
            print(f'content{content} and {type(content) }')
            print(f'types:{json.dumps(content) } and {type(json.dumps(content)) }')
            
            _reponse = map_predictions(content) #process_request(content)

            print("_reponse:",_reponse)
            return _reponse
        except Exception as e:
            print("####### Exception occured#####:",e)
            error = e
            return jsonify({
                  "message":"success",
                  "status": 400,
                  "data": "Input is not in JSON/ transcripts key not found in input",
                  "error": str(error)
                })            

    
    except KeyError  as e:
        return jsonify({'message':"Could not process request", 'status': 500, 'exception' : e})
    
    except Exception as e:
        print (e)
        return jsonify({'message':"Could not process request", 'status': 400, 'exception' : e})


# In[ ]:




# In[ ]:


my_text = [
{
"pagenumber": 2,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510060008842

Suggested E/M=99203
1995 Guidelines

*Main Problem (list only one) )yj
O pressure 1 weakness
C1 oth

History=COMP (CC=Present;

HPI=Extended; PFMSH=Complete; ROS=Complete)

Exam=DET (4 Syst: 1 Syst/BA Expanded) / Complexity of MDM=MOD (DX=MOD; RISK=MOD; Data=N/A)

Atexian Brothers Corporate Health Services
41060 S. Elmhurst Road, Mt. Prospect, iL 60056

Recent Abnormal (for you) Symptoms

EI fever O chills ©) sweats Oltired [1 weight loss
(1 headache [1] weakness] poor balance or coordination

Where is it?

Makes worse:

Makes better:
Timing is...

List related symptoms....0 0.0.0.0 ce a ee

Severity

Quality: Radiation? Ono ( yes, where? _..
OsharpO dull acheO burnO other
What caused this or was happeningywhen this started? (describe ath

lated? LN
i )

O12 34 5 6 8 9 10} >"
OQOOBO0O000QWo000
+ Ono pan or symptoms frsiXef your fa=10 |

(OO umb, O1 tingling © urinary or bowel changes

[Head qr pain in > o car “Ch month © i tooth CF tivoat”
yes j urred vision_ ‘a doubte ‘Vision o eye pain
, Seer Di itchi s__[] redness
muscle pain> ¥ oral [) many areas |
joint pain > D several (many joints
Cchest pain or pressure Cllight headed EJ fainting |
DD fluttering in chest (1 swelling of legs or feet
Resp [@Y [Dison ‘of treaty Cleough Ch wheeze
Gl Ty " 7 dian ea “Cina nausea oo vomiting —

oO painful or “frequent urination Oo waking up to urinate
a irregular periods a itching O pain Oo discharge

io sepressedeatng, blue. ‘a anxious o difficulty sleeping
. a) unusual muising

‘a sneezing frequent infections

a itchy eyes

Where did injury occurZ-&t public building Wes.No

CO streathighway Industrial [1 ree sit (1 We are only care provider?
1 residential institution Cl fam (1 home (2 Back w/o prior injury?

C1 minefquary CD Treatment followed?

Cl other, ie, CO Tolerated treatment?

Current work status: oO regular ‘ty o maid duty 2 off work

boxes below)

. inl Wee
Family History ‘None O ir nat . -
CFO | her "Pregnant?" (Yes, No C] Unsure] tam-dd=yy)__
M O Sib it -
a ween eee . Last
OFOMOSibOOther Last Mam! (Ee
CF OM O Sib O Other Motses “pS me Last ae
a ~sdo - -
[Tobacco Tyhrever quit in (yr) CQ cigars (ram-od--yy) Pap (mma)
packs per day O<1/2 <1 O17 0174/2 (1>20 chewor snuff; ah amet ° ce tonnnoneet 8
Alsohot |G never [drinks per dayX) <1 1 1-2 112-3 C1 >3 - - a ae
7 Guen pending ROTO Sign in Sign out PiVoT
Street/Unprescribed Drugs? [N.no (1 yes} Pracice velocity Complete Complete Scanned"""],

}]

# my_text_page_no = [j for k in my_text for i,j in k.items() if i == "pagenumber" ]
# my_text_page_category = [ j for k in my_text for i,j in k.items() if i == "category" ]
# my_text_page_text = [j[0] for k in my_text for i,j in k.items() if i == "ImageText" ]
# print(f'{my_text_page_no},\n {my_text_page_category},\n {my_text_page_text}')


# In[ ]:


my_text = [
{
"pagenumber": 2,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510060008842

Suggested E/M=99203
1995 Guidelines

*Main Problem (list only one) )yj
O pressure 1 weakness
C1 oth

History=COMP (CC=Present;

HPI=Extended; PFMSH=Complete; ROS=Complete)

Exam=DET (4 Syst: 1 Syst/BA Expanded) / Complexity of MDM=MOD (DX=MOD; RISK=MOD; Data=N/A)

Atexian Brothers Corporate Health Services
41060 S. Elmhurst Road, Mt. Prospect, iL 60056

Recent Abnormal (for you) Symptoms

EI fever O chills ©) sweats Oltired [1 weight loss
(1 headache [1] weakness] poor balance or coordination

Where is it?

Makes worse:

Makes better:
Timing is...

List related symptoms....0 0.0.0.0 ce a ee

Severity

Quality: Radiation? Ono ( yes, where? _..
OsharpO dull acheO burnO other
What caused this or was happeningywhen this started? (describe ath

lated? LN
i )

O12 34 5 6 8 9 10} >"
OQOOBO0O000QWo000
+ Ono pan or symptoms frsiXef your fa=10 |

(OO umb, O1 tingling © urinary or bowel changes

[Head qr pain in > o car “Ch month © i tooth CF tivoat”
yes j urred vision_ ‘a doubte ‘Vision o eye pain
, Seer Di itchi s__[] redness
muscle pain> ¥ oral [) many areas |
joint pain > D several (many joints
Cchest pain or pressure Cllight headed EJ fainting |
DD fluttering in chest (1 swelling of legs or feet
Resp [@Y [Dison ‘of treaty Cleough Ch wheeze
Gl Ty " 7 dian ea “Cina nausea oo vomiting —

oO painful or “frequent urination Oo waking up to urinate
a irregular periods a itching O pain Oo discharge

io sepressedeatng, blue. ‘a anxious o difficulty sleeping
. a) unusual muising

‘a sneezing frequent infections

a itchy eyes

Where did injury occurZ-&t public building Wes.No

CO streathighway Industrial [1 ree sit (1 We are only care provider?
1 residential institution Cl fam (1 home (2 Back w/o prior injury?

C1 minefquary CD Treatment followed?

Cl other, ie, CO Tolerated treatment?

Current work status: oO regular ‘ty o maid duty 2 off work

boxes below)

. inl Wee
Family History ‘None O ir nat . -
CFO | her "Pregnant?" (Yes, No C] Unsure] tam-dd=yy)__
M O Sib it -
a ween eee . Last
OFOMOSibOOther Last Mam! (Ee
CF OM O Sib O Other Motses “pS me Last ae
a ~sdo - -
[Tobacco Tyhrever quit in (yr) CQ cigars (ram-od--yy) Pap (mma)
packs per day O<1/2 <1 O17 0174/2 (1>20 chewor snuff; ah amet ° ce tonnnoneet 8
Alsohot |G never [drinks per dayX) <1 1 1-2 112-3 C1 >3 - - a ae
7 Guen pending ROTO Sign in Sign out PiVoT
Street/Unprescribed Drugs? [N.no (1 yes} Pracice velocity Complete Complete Scanned"""],

},

{
"pagenumber": 3,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510060008842

LL be

Back
GU

J shes, ecchymosis, or lesions of skin of back

C1 Sensation : QCipTRs | AG Cy Strength
R L (mark where abnormal): (mark ifabnormal) + Hip fix (T12-L3)
DO Med forearm (T1) : i IR L
OO Medarm (T2) : R Patella Ltt ts 15
D O Torso (T1-7 H : 4
oo Thoacalaba (78-12) ‘L142 ya * Ptdersins (4)
OGantthigh (lia) | i} IR] |b
CO Med tep/foot(L4)  -R, Aenites LQ gy
D OLatigimd&drs ft (L5) :} | ei! IR
O OLatplantarft(S1) : : 15 15

MS‘ (1D Gait & Posture (antalgic gait, limp, hunched, tilting)
© [IB Spasm or tenderness of parasping! muscles
CO Loss of lumbosacral lordosis
/¥&i 0 Kyphosis or Scoliosis

OD Pelvisasymmetry . 4
O ) Heel/Toeambulation,
CP Straight leg raise tgSt for sciatic nerve“involvement

0
a=) 0 EHL weakness, i.e., great toe extension (L5)
C Patrick-Faberetest for pathology of sacroiliac joint
OC) Wadell'ssigns (specify if positive) C1) Axial loading
OO DistractedSLR C1 Superficial hyper-tendemness
© Simulated rotation D Ove:
DAD Back ROM (specify if posid

Flexion: fingertips to midtthigh Lo
ordst fromiloor 1 knee Vegi

action (not reproducible)

Name: COLLINS, WILLIAM

SSN: 9326-58-59
Birthdate: 06/19/1958
Visit Date: 09/23/2015 09:30 am

Acct: L07828159

Age: 57 yrs. 3 mon.

QUA (micro):

Patient seen during Glob
C1 day 0; 0-100 global
D day 0; 90d globat

Ci complication
CO related procedure

O day 0; sched. proc. (©) unrelated problem

al Period for a Procedure

C1 routine flu to global
Cl previous proced
different provider

O mid-shin
in. £30°
Lateral Flexion Lateral Rotation

R L R L
130° #30° 430° 130°

Ms" H&N LUE RUE LLE RLE
hpecintrain FO OO OO agag
i oO ob 00 oo oO

im) oO OO 00 00

og oO QO OO oO 00

Card" O 0 Hes
ENT

nurmurs, rubs, gal ks)

OO Ear pinnae & external nose (redness, lesion, mass) .

* Diagnoses
C2 new,wlu planned

‘jew,no wiu planned

est worsening
D est ,worsening

CO est stablefmproved
est, stablefimproved
CO est, stablefimproved

OO minor feg. cota, since,
‘insect bite)

O minor

Select 1 highest box!

fife threat; chr prb (sev exac),

acute inj 22 bdy area (mult trma)
acute neuro 4 (TIA, sz, weak)
or fracture (mani pution)

Rx med; chr prb (mid exac),
Injtoce,tvwrk. envijob.funcidisab,
acute illness(systmic symptoms:
inj acute: 1bdy area (complicatd,
head inj brief LOC,
dressing/debridment:1 bdy area
or fracture (no manipulation)

(F OTC med; minor surg,

acute problem {uncomplic.),
or 1 chronic stable probiem

Order and/or Review

{71 Independent reading of
1 Discuss test wi performing
(0 Decide to get off records

CJ Review & Summarize old

minor prob, rest, gargles...

Data Reviewed

2 Lab Test: va,strep,cho,cmp...
( Rad Test: x-ray, CT, MRI, US
(1 Med Test: EKG, PFT, Ox sat!

Image, tracing, or specimen
physician
or to get 3rd parson hx

records; get 3rd person hx;
or _discuss_w/other provider

0 O TMs& ext canals (red, tender, swelling)
OO Sinuses (maxillary or frontal) tender to percussion
OO Nares (mucosa, septum, turbinates)

O © Mouth (lips, teeth, gums)
O CO Pharynx (mucosa, salv gland, palate, tongue, tons, pharynx) _

Glabd OO Masses or Tender to palpation (Murphy sign)

OC CD Bowel sounds (absent, few, loud)

ro 1234567 8 8 |ifcounseling &/or coord. of care >50% of visit,
DoooooooO sop ilist total face-to-face time & document content.
atutetfataratetate O>10 Oets O20 0225 0230

Or40 O>4s O>60 0 280

iS

I certify that I have reviewed all of the data on all pages of this
form, and I deem the exam clinically appropriate for this visit,

*

en re

OO Liver & Spleen (enlarged, tender)

provider signature ¢499_99232018_093100

1000002661 0
21844

Fu) ="""],

},

{
"pagenumber": 4,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510060008842

|| Alexian Brothers Corporate Health Services .
i . . 1060 S. Elmhurst Road, Mt. Prospect, IL 60056 Name: COLLINS, WILLIAM a
; Diagnosis aa SSN; 326-58-59 Acct: L07828159
DD BOL Dermatitis, atopic DB DED Neuratgia A . 5
OOOO Fibromystgia CIGD Neunttsadtcatits, tambsr Birthdate: 06/19/1958 | Age: 57 yrs. 3 mon.
O DOD Muscte spasm 0 OOD Pitontdat cyst Visit Date: 09/23/2015 09:30 am
0 OOD Myagia C3 G1 O Pyelonephritis, acute
DOO mysts = == OOD Statin = Const CMR: oer: (i pr: starContinue
O OOD Abrasion (] neck [7 chest 1) back [1] buttock [1 abdomen (7) thigh a
OOD Bum earn? O3 6 a0 <x 0 10-19% ROJRe_____ Ss Specialist/Facclity: 7
; © (scalp 1 face (1) trmk (7 neck [[) shoulder (1 thigh - - oom
oOO000 Coltulitist OD sealp =O face (7) trunk (7 neck (7) shoulder (2) thigh Date (mm-dd-yy)

OOO comusn O scalp [[] face/neck [) chest [] shoulder [1] back
OO scaputer 1] abd wat §= 1) buttock Chip =) thigh Aner,
01 21 1D Disc Herniation, C-spine ([} without myelopathy — [[] with myelopathy | ———

1 C1 (101 Dise Herniation, T-spine (7) without myelopathy [1] with myelopathy
01) 11 111 Disc Herniation, L-spine [1] without myelopathy [7] with myelopathy
- L

COD resg § Csalp CO fice C1] tnnk C) neck Fy shoulder 0 hich “{ C&A spe Seg)
OOOO Freure © O closed O open C-spine (no cord injury)
© DL) hyoid bone O mandible cl ¢2 #¢3 C4 0
Di thyroid cartitage £] clavicle goood fA
OO trachea CO Tepine oooaa \

{ o larynx C$ C6 C7 multiple

' DOOD taceration @ C1 uncompttcated C] complicated (0b; infected: delayed ts)
i o Cl neck (©) back = [[] chest wall (7) abd wall, tat [7] buttock
OOOO Pan Blemne (1 Tspine — () Lespine OC timb

fa COO Sprainisteain GOcrspine AQ Tspine CI] Levine C1 shoulder
/
i _
; 2 Work Status: applies to work, home & recreation
: Fit for duty without . -
' al restrictions as of: today or Date (rim-dd-yy)
(4 Fit for duty with d eAIcies =] =f)
the following today or - -
O080 oo00 cooo «ooo ne istone os of y ae a
Li ttyy LELi ty LEP IL) LLL Ly | Mi Avoid kneeling, squattinggimpiad, rinqinp, clicibingtadders
EO EQ EO D Avoid prolonged CC sitting O standing
vo vO vo vo D Avoid strong gripping with .
9 00000 0 00006 0 OO000 0 OOOO | C Limit repetitive motion with } Clrighthand 11 left hand
100000 100000 100000 100000 Ib houlders with
200000 200000 200000 200000 | noffting S$ over snoulders wi CO right
3 00000 300000 300000300000 | greater Ibs below the waist nonvarm
400000400000 400000400000 than . Oi left arm
5 00000 s 00000 500000 s coo00 tbs waist to shoulders
600000 600000 6 00000 6 QO000 | CNopulling or pushing over ibs. mel he
7000007 00000 7 00000 7 OO000 | © Proper iting techniques as instructed an ee
8 O0D000 8 00000 8 00000 8 00000 | gright 2 ceit handed duty only C1 Wear splint
§ 0000080 900000 300000 9 OOOO | g sitdownwork only .
Instructions (Boils © Buns (1 Cetuitis L Cisiccation/Subluxation| Off work: C1] today only - - time out (hh-mm)
D Folicutitis (J Hidradenitis ([] Hyperhidrosis 17 Insect Bites/Stings or until Date (mm-dd-yy} am (1 PM
CO) KeratosisPilaris (1 Osteoarthritis [1 Shoulder, Frozen (1 Sprains/Strains R days if not better; [1 per consultant
1 Tendinitis‘Tenosynovitls theck sooner if worse. ‘ released 1000002661
OC wWoundGare LJ other Scheduled retum visit O7) T- @ -( ) aM 0
OF - otf -Lf : cpm +
Comp {1 Nophona# 11 Recheck is" Date (mm-ad-yy) _Timethh-mm) "3
Call CO Not reached, Why?... va 20. pr Call this office with any questions. c109_o9232018, 0831
“WG message to... b> " 4255
LD Spoke to... 923 S
a name Provider Signature . . a a
abd = abdomen; fb » foreign body, lut = Lateral: tx = treatment patent pending & © 2007 Practica Velocity |"""],

},

{
"pagenumber": 5,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""Printed: 9/23/2015

201510060008842

Alexian Brothers Medical Group Mt. Prospect
4060 S. Elmhurst Rd.
Mount Prospect, IL 60056-4240
224-265-9000

Discharge Summary

Company Metro Water Reclam/Chicago Phone 847-584-5424
Contact Bob Gottstein Fax 312-894-1162
Email robert.gottstein@mwrd.org
Patient Name William J. Collins
Patient ID L07-82-8159 Arrived Clinic 09:30 AM
Time In 09:40 AM
Left Clinic 10:39 AM
Injury Date 9/21/2015 Examining Provider Salvador Cabanit MD
Exam Date 9/23/2015 Initial Injury exam: Return to work with restrictions 9-23-15, Continue

medications. Return to Clinic or Hospital if pain worsen.

Work Status Summary Effective 9/23/2015, William J Collins is released to work on a modified basis:

Work Restrictions
Lift/Carry Limited to 10 Ibs

Limit Push/Pull to 10 lbs
Limit Repetitive Motion
No Climbing Ladders

Patient Injury Description pt states he injured his back at work while lifting a piece of metal.
Diagnosis 1, Upper Thoracic Strain 2. Cervical Strain

*Services Summary Initial Injury

*This is a general overview of the visit, it is not a complete list of billable services

Scheduled Appointments
Date Time Provider Specialty

9/29/2015 07:00 AM Salvador Cabanit, MD Occupational Medicine

Patient Instructions: y) eo

i L received and understand the information in this Discharge summa ob

Patient Signature Provider Signature"""],

},

{
"pagenumber": 6,
"category": "Medical",
"Type ":"Image",

"ImageText": [""") ALE

IAN

BROTHERS

Medical Group

2015100600

08842

Ve CORM = 01s

OWS

Q-I3BAS

ARRIVAL TIME

Treatment Rendered At

TIME OUT

O Alexian Brothers Medical Center- ER © Addison
O St. Alexius Medicaf Center - ER cyan. Prospect

DATE

O Bensenville

C1 Palatine

O Elk Grove
© Schaumburg

letra Woader

Collins William PEM

EM

PLOYER

Reckum

QO Non Work Related

Work Related

Diagnosi:

RETURN TO WORK:

OlNow Other (date) B Unable to work at this time.
C1 No Restrictions as of: With Restrictions as follows/as ok G o- 3 —t >)
LIFT/CARRY PUSH/PULL BEND/SQUAT STAND/AWALK OL OR
Q No LifvCary G No Push/Pull Gi No Knecling/Squatting © No Stand/Walk HAND/ARM
O Limited LifvCarry O No Twisting D No Bending {1 No Climbing Stairs © No Use
A # Maximum a Limited Push/Pull NG) Limited Repetitive No Climbing Ladders D Limit Useto_
t 7 ‘Sg herim ERY ‘Motion -Alternate~ ne weed —Hours/Day
~ Standing/Sitling as O Limit Strong Grip’
Tolerated Grasp/Pinch
© Sitting Only No Reaching/
Lifting Above
Shoulder

Misc: G Keep Wound Clean/Dry Avoid Contact with Imitating Chemicals
Q Use Splint O At Work O AtHome

Safety Precautions: Ci No Climbing or Work at Heights 0 No Driving or Operating Machinery

- ~ . DURATION OF RECOMMENE
Until Followup On: BR - JO-IO"S eR OF- gQ-(S

01 1240 N. BUSSE ROAD (RT.83) 1060 S. ELMHURST ROAD
BENSENVILLE . PROSPECT
(224) 265-9000

(847) 228-6407
6:30 am—6:00 pm M-F 7:00 am — 7:00 pm M-F

© 126 BIESTERFIELD ROAD
ELK GROVE VILLAGE
(847) 981-5910
7:30 am ~ 5:00 pm M-F

© 50 S NORTHWEST HIGHWAY
PALATINE
(847) 202-6060
8:00 am - 8:30 pm M-F
9:00 am — 6:00 pm Sat & Sun

DO 1139 W. LAKE STREET
ADDISON
(630) 930-5600
8:00 am - 8:30 pm M-F
9:00 am - 6:00 pm Sat & Sun

©1515 W. LAKE STREET
HANOVER PARK
(847) 472-1500
8:00 am - 8:30 pm M-F
9:00 am ~ 6:00 pm Sat & Sun
© Return Only as Needed
(© Company Contacted-
Name of Person Contacted

C1 Referred to:

Physician Signature:

036i WGOLF ROAD
SCHAUMBURG
(847) 952-7447
7:30 am - 7:00 pm M-F

Comments: a9) @nrn0 “A
<a) prea ag be
Other Instructions: ARR COPS 5 ;"""],

},

{
"pagenumber": 7,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510130002441

ww zw

PRAIRIESHORE PAIN CENTER, P.C.
185 Milwaukee Ave, Suite 230
Lincolnshire, IL 60069
Phone (847) 883-0077 Fax (847) 883-0078

COLLINS, WILLIAM (DOB: 6/19/1958-ID: 4166) - Sep 28, 2015 Mon 09:28 AM

cc

HP!

ROS

left neck and upper back pain/ muscle spasm

Patient presents for evaluation of above complaint. Pain score is current 3/10, average 5/10,
range 3-7/10. Patient reports worst pain located between shoulder blades into neck. The pain
radiates down left shoulder and arm. Patient describes pain as a intermittent dull, spasming,
stabbing/sharp and shooting pain. The pain is worst in the morning, during the day, evenings
and in the middle of the night. Patient has new pain complaint since last visit. On 9/21/15, pt
was at work lifting a metal flight(metal |-beam) and carried it about 25 feet. Immediately after
lifting this metal piece, he had pain in shoulder blades, left neck and down his left arm. He
reported if to his supervisor and was sent to company clinic 9/23/15 and given lifting
restrictions. He hasn't gotten better since that time. Pt denies any NEW issues with balance
problems, bladder/bowel incontinence, chills, difficulty walking, fevers, nausea/vomiting,
numbness/tingling, or weakness. Pt denies medication side effects: confusion constipation
dizziness drowsiness dry mouth nausea vomiting weight gain. Patient denies adverse effects
from current medications. Patient reports that patient is stable on the current medication
regimen. Pt reports that medication regimen helps to improve functioning and quality of life.
Patient reports compliance with medication regimen.

Original presentation:

This patient originally presented as a middle-aged man who was involved in a snowmobile
accident in 2004. The snowmobile overturned onte his right leg, resulting in a broken tibia and
fibula. Over time, he developed chronic pain over the right shin, radiating into the ankle and
foot. Constant pain is dull achy throbbing and stabbing. Intermittent pain is sharp burning and
shooting. Pain score ranges 4-8/10, Patient can not specify pain triggers. Medications help
contro! pain. Patient denies associated numbness, weakness, or muscle spasms in affected
limb. Patient denies prior history of similar pain. Onset was sudden. Patient denies
associated symptoms including weakness, numbness, pins & needles sensations, and muscle
spasms though he does have numbness in his left leg due to lumbar spine surgery. Patient
denies changes in sweating, temperature, skin color, hair/nail growth, muscle tone, and joint
flexibility. Patient denies associated bowel/bladder incontience or saddle anesthesia.

He has seen an ortho spine surgeon in the past. EMG results reveal acute moderately severe
bilateral L5-S1 radiculopathy.

Opioid risk factor- ORT = 0 (low risk 0-3)

Patient denies chills, difficulty sleeping, easy bruising/bleeding, rashes, excessive thirst,
fatigue, fevers, insomnia, low sex drive, night sweats, tremors, unexplained weight gain,
unexplained weight loss, weakness, recent visual changes, dental problems, hearing problems,
nosebleeds, recurrent sore throats, sinus problems, chest pain, blood clots, fainting, irregular
heartbeat/racing heart, lightheadedness, feet swelling, cough, wheezing, pulmonary embolism,
shortness of breath with exertion, shortness of breath at rest, acid reflux, coffee-ground vomit,
constipation, dark & tarry stool, diarrhea, nausea/vomiting, blood in urine, flank pain, painful
urination, decreased urine flow/frequency/volume, joint stiffness, joint swelling, carpal tunnel
syndrome, dizziness, headaches, loss of balance, numbness<tingling, seizures, tremors,

Printed By: Karen May, SECRETARY 10/8/2015 11:29:40 AM

Amazing Charts _ Page of 4

The information on this page is confidential.
Any release of this information requires the written authorization of the patient listed above."""],

},

{
"pagenumber": 8,
"category": "Medical",
"Type ":"Image",

"ImageText": ["""201510130002441

wow nae

COLLINS, WILLIAM (DOB: 6/19/1958 ID: 1166) '. Sep 28, 2015 Mon 09:28 AM
depressed mood, anxiety, stress, suicidal thoughts, suicidal planning, thoughts of harming
others.

Patient denies all above symptoms.

PMH h/o headache/migraine, lumbar degenerative disc disease, sinusitis, seasonal allergies

PSH inguinal hernia repair, removal of tongue cyst, lumbar discectomy, repair of broken leg,
removal of hardware in leg

SH Patient works full-time as an engineer.
Patient denies any history of tobaccoiillicit/prescription drug abuse.
Patient drinks etoh 2x/month,. Patient is married with two adult chilildren, lives with wife.
Tobacco: Never smoker
[Tobacco: Never smoker]

FH Patient denies any family history of CAD, DM, or CA.

==== Structured Family History ========

Patient reports their family members have no significant health history; Patient denies any
family history of CAD, DM, or CA.

Parent: No significant health history.

Allergies vioxx, dogs, trees, ragweed pollen allergen extract (Updated by NICOLE on 10/03/2014 09:33
AM)

Meds 1) lidocaine 5% topical ointment, apply 1-2 grams to effected area up to QID prn
2) Lidoderm 5% topical film, Take 3 patch(s) to affected areas Q12h X 1 Month (30d) As
Needed

3) Lifting restricted at 20#. No heavy pushing/pulling for one week.

4) Marinol 2.5 mg oral capsule, Take 1 pill by mouth QID X 30 days

5) Opana ER 20 mg oral tablet, extended release, Take 1 pill by mouth BID X 30 days
6) oxyCODONE 5 mg eral tablet, Take 1 pill by mouth TID X 20.days As Needed

7) Relpax 40 mg oral tablet, Take 1 pill by mouth QD X 1 Month (30d) As Needed

8) Sudafed 12-Hour 120 mg oral tablet, extended release, PRN

Vitals Wt: 175 lb Ht/Ln: 73 in BMI: 23.1 BP: 140/70 Pulse: 74 Sat: 95

PE Pleasant & cooperative Caucasian man with slim body habitus who appears his stated age.
Skin appears tanned, & dry with well-healed scar noted on right leg. HEENT NCAT EOMI
anicteric sclera, pink & moist oral mucosa, dentition wnl. Neck supple without masses or
tracheal deviation. Pulmonary: unlabored & quiet breathing. Peripheral vascular system: no
ankle/foot edema or varicose veins present. Musculoskeletal: normal muscle tone & bulk
except for tight bands and triggers noted left trapezius and rhomboid muscles. Increased pain
with cervical ROM. Hyperesthesia & paresthesia over the right shin/scar. Neuro heel-to-toe
gait WNL, no tremors/ataxia/antalgic gait, sensory grossly intact to light touch except as noted.
Mental status alert x oriented x 3, pleasant affect. Patient exhibits no signs of opioid
intoxication: no speech slurring, pupils are not miotic, no stumbling gait, no apparent
drowsiness. Patient does not display signs of opioid withdrawal: No tremors/ irritability/
piloerection/ or mydriasis.

AIP # Spasm of back muscles (728.85): (thoracic)

Previous Diagnoses:
# DEGENERATION OF LUMBAR OR LUMBOSACRAL INTERVERTEBRAL DISC (722.52):
# POSTLAMINECTOMY SYNDROME OF LUMBAR REGION (722.83):

Printed By: Karen May, SECRETARY 10/8/2015 11:29:40 AM
Amazing Charts : Page 2 of 4

The information on this page is confidential.
Any release of this information requires the written authorization of the patient listed above."""],

},

]
# my_text_page_no = [j for k in my_text for i,j in k.items() if i == "pagenumber" ]
# my_text_page_category = [ j for k in my_text for i,j in k.items() if i == "category" ]
# my_text_page_text = [j[0] for k in my_text for i,j in k.items() if i == "ImageText" ]
# # print(f'{my_text_page_no},\n {my_text_page_category},\n {my_text_page_text}')
# print(f'"WELCOME:"{json.dumps(my_text)}')


# In[ ]:





if __name__ == "__main__":
    server.run(host='0.0.0.0',port=9005, debug=True)