#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import os, numpy as np, json
import transformers
from transformers import AutoModel, BertTokenizerFast, BertForSequenceClassification, BertTokenizer
import spacy, torch


# In[2]:


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# In[12]:


my_pages =[
    "Fax Server 2/29/2022 (Li24:27 AM PAGE 1/010 Fax Server\r\n\r\nBLESSING\r\nPO Box 7005 + Quincy, IL 62305 * 217.223.8400\r\nHealth System blessinghealthorg Q@OOOO\r\n\r\nDate: 2/25/2022\r\n\r\nTo: WORK COMP LUDWIG From: Blessing Health System\r\n\r\nLocation: Department: Patient Financial Services\r\n\r\nFax Number: 866-767-3290\r\n\r\nImmediate Action: Yes\r\n\r\nNumber of Pages (including this page): 10\r\n\r\nMessage:\r\n\r\nPlease review and process\r\n\r\nThanks\r\n\r\nChell Threet CRCS.Account Specialist\r\nBlessing Hospital\r\n\r\nPFS Work comp\r\n\r\n217-223-8400 EXT 4189\r\n\r\nFax 217-223-9945\r\n\r\nBlessing Hospital \u00ab Hini Coramunity Hospital \u00bb Ble\r\n\r\nsing Physician Services \u00bb Hannibal Clinic * Derman Services\r\n\r\nBlessing-Rieman College of Nursing & Health Sciences * Blessing Foundation + Blessing Corporate Services\r\n\r\nCCOC/S C/O",
    "Fax Server 2/29/2022 (1:24:27 AM PAGE 8/010 Fax Server\r\n\r\nBlessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Result - Current Visit\r\nPatient Name: Ludwig, Candia $ Admit Date; 02/10/2022 Attending: Pimlott, Bryan J\r\nMRN: 000136426 Account Number: 4002-274362 Referring: Pimlotl, Bryan J\r\nDate of Birth: 06/01/1960 Discharge Date: 02/40/2022\r\nAge: 6ty Location: Radiology\r\nGender. Female\r\nRadiology\r\nDate/Time: 02/10/2022 15:07 Ordering Physician: Pimiott, Bryan J Order#: OO7NHJZXL\r\nProcedure. Fluoro Needle Loc/Biopsy/Aspirat a Ancillary#: OOTNHJZXL\r\nReason, Shoulder dislocation right initial encounter\r\nFluoro Needle Loc/Bicpsy/Aspirat Final Updated\r\n\r\nFINAL\r\n\r\nStudy Description: FL GUIDANCE ONLY FOR NEEDLE PLACEMENT\r\n\r\nORDERING HEALTHCARE PROVIDER: Bryan Pimiott\r\nClinical Indications: Right shoulder dislocation.\r\n\r\nProcedure: The procedure, risks, benefits, and complications of the procedure wereexplained fo the patient. Also discussed the\r\ntisk of bleeding, nerve damage, infection. The patient agreed to the procedure and expressed verbal understanding. All questions\r\nwere answered. Written consent was obtained and placed in patient's chart. The patient was placed supine on the table. Ascout\r\nview of the right shoulder was obtained for the purposes of localization. The patient's right shoulder was prepped and draped in\r\nusual sterile fashion. Lidocaine 1% was utilized for local anesthesia. Using an anterior approach and under direct fluoroscopic\r\nguidance, a 22-gauge spinal needle was introduced into the right glenohumeral joint space. This is then followed by a mixture of\r\n10 mL of Omnipaque, 5 mL of saline, \u00a7 mL of 1% lidocaine and 0.1 mL of Omniscan into the joint space. Atotal of 12 mL was\r\ninjected into the joint space. Hard copy of needie placement was obtained. The needle was removed and hemostasis achieved\r\n\r\nwith manual compression. Asterile dressing was applied. There was lessthan 2 ML blood loss. The patient tolerated the\r\nprocedure well without immediate postprecedural complications. The patient tolerated the procedure weil and was sent to MRI in\r\nstable condition.\r\n\r\nFluoroscopy time was 54 seconds, Total images 2. The mGy skin dose was 17.9.\r\nimpression: Technically successful fluoroscopic-guided right glenohumeral arthrogram.\r\nProcedure was performed by Sonya Krause, PA-C\r\n\r\nElectronically signed by. Mohammadali Mojarrad MD\r\n\r\nSigned Date/Time: 2/14/2022 8:45 AMCST\r\nWorkstation: 109-0432 TY6\r\n\r\nAccession Nbr. OO1NHJZXL\r\n\r\nDate/Time: 02/10/2022 15:50 Ordering Physician: Pimlott, Bryan J Order: OO7NHJZXR\r\nProcedure: MRI Shoulder Right w Contrast a Ancillary#: OOTNHIJZXR\r\nReason: Shoulder dislocation right initial encounter\r\nMRI Shoulder Right w Contrast Final\r\nFINAL\r\n\r\nEXAM: MRI Shoulder Right w Contrast\r\nRadLex MR SHOULDER WITH IV CONTRAST\r\n\r\nHISTORY: Shoulder dislocation right initial encounter.\r\n\r\nThe information contained in this report is confidential. If you have received this docurment in enor, please notify the Medical Records department.\r\n\r\nPrinted: 2/24/2022 2:03:08 PM Page: 1 of 3 Report: BHResult\r\nBlessing's Automated Record\r\n\r\nCCOC/S C/O",
    "Blessing Hospital\r\n\r\n11th & Broadway Quincy, Illinois 62305 (217) 223-1200 Selected Document\r\npe akin Meiaih? Kauai SOE a OO \u2014\u2014e\u2014e\u2014eEeEeEeEeEeEeEEEEEe\r\nPatientName: Ludwig, Candia S Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/0141960 Oischarge Date: 03/02/2022\r\nAge: 61y Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\nODS Operative Report/Discharge Orders\r\n\r\nOate Of Service: 63-02-2022\r\n\r\nProce\r\nPhysician Dictation:\r\n\r\nDate af Surgery:\r\n\r\n3/2/2022\r\n\r\nPreoperative Diagnosis:\r\n\r\n1. Right shoulder rotator cuff tear.\r\n\r\n2. Right shoulder biceps tendinopathy.\r\n\r\n3. Right shoulder subacromial impingement.\r\n\r\n4. Right shoulder degenerative labral tear.\r\nPostoperative Diagnasis:\r\n\r\n1. same\r\n\r\nProcedure Performed:\r\n\r\n1. Right shoulder arthroscopic rotator cuff repair.\r\n2. Right shoulder arthroscopic biceps tenadesis\r\n\r\n3. Right shoulder arthroscopic subacromial decompression.\r\n4, Right shoulder arthroscopic limited debridement.\r\nSurgeon: Josue Acevedo, MD.\r\n\r\nAssistant: Ciara Glenn, PA,\r\n\r\nAnesthesia: General.\r\n\r\nAntibiotics: 2 g cefazolin fv.\r\n\r\nFluids: Crystailoid.\r\n\r\n| The information contained in this report is confidential. If you have raceived this document in error, please notify the Medical Recaris department.\r\n\r\nPrinted: 04/ 28/2022 Page: 1 of 6 Report: BHSelectedDocurrent\r\nBlessing'\u2019s Automated Racord\r\n\r\nOVd\r\n\r\nTTOT/80/80",
    "Blessing Hospital\r\n\r\n{ith & Broadway Quincy, tilinois 62305 (217) 223-1200 Selected Document\r\nPatientName: Ludwig, Candia S$ Admit Date: 03/02/2022 Attending: Acevedo. Josue\r\nMRN: 000136426 Account Number: 4002-286841 Referring: Acevedo, Josue\r\nOate of Birth: 06/01/1960 Discharge Date: 03/02/2022\r\nAge: 6ly Location: Surgery Center BH PACU\r\n\r\nGender: Female\r\n\r\n008 Operative ReportDiecharge Orders .\r\n\r\nOate Of Service: 03-02-2022\r\n\r\nEstimated Blood Loss: Minimal.\r\n\r\nPositioning: Lateral Oecubitus.\r\n\r\nImplants:\r\n\r\n1, Arthrex 4.75mm PEEK SwiveLock Anchar (x5 }.\r\nSpecimens: None.\r\n\r\nComplications: None.\r\n\r\nFindings: Intra-operative: Right full thickness large supraspinatus L-shaped tear with retraction to the articular cartilage. Full-\r\nthickness superior subscapularis tendon tear. Lang head of the biceps intra-articular tendinopathy and tear. Degenerative\r\nanterior and inferior labral tears. Moderate sized subacromial spur, type ll. Glenohumeral articular cartilage was fairly intact.\r\n\r\nIndications: This is a 61 years old female with history of right shoulder pain with associated limited range of motion and\r\ndiagnosis of a rotator cuff tear. This was canfirmed on preoperative imaging. Initially, injuries were treated with non-\r\noperatively and the patient failed this treatment plan. It was then discussed in the office the option to undergo the procedure\r\nas listed above. The risks, benefits, and alternatives ta this procedure were descrihed ta the patient. Surgical risks include but\r\nare not limited to ratator cuff tendon re-tear, adhesive capsulitis. weakness, bleeding, damage to nerves, vessels, muscles,\r\ntendons, infection, DVT. pulmonary embolism. postoperative stiffness, postoperative pain. and need for future surgeries. All\r\nquestions were answered to their satisfaction, they elected to proceed with surgery. and subsequently siqned an informed\r\ncansent form.\r\n\r\nDescription of Pracedure:\r\n\r\nThe patient was identified in preoperative halding area by verbal name confirmation as well as name tag identification. The\r\nOperative site was marked with indelible ink as per protocol. They were taken to the operating roam, placed supine on the\r\noperating table, and anesthesia was induced. They were then carefully placed in the lateral decubitus pasitian on a bean bag.\r\nAll bony prominences were well padded and an axillary roll was placed. The operative extremity was prepped and draped in\r\nthe usual sterile fashion. Traction on the operative extremity was maintained using 10 pounds hanging from the arm\r\npositioner. 1% lidocaine with epinephrine was subcutaneously injected into the planned incision sites. Antibiotics were\r\nadministered prior ta beginning the procedure. A final time-out was taken where the surgeons involved, anesthesia. and\r\nsurgical staff were in agreement on the correct patient. operative site. and procedure to be perfarmed.\r\n\r\nThe information contained in this report s confidential. If you have received this document in error, please notify the Medical Records department.\r\n\r\nPrinted: 04/ 28/2022 Page: 2 of 6 Report: BHSelectedDocurent\r\nBlessing\u2019s Automated Record\r\n\r\nOVd\r\n\r\nTTOT/80/80"
]


# In[17]:


#14
#pages 1
my_pages =[
    "Peer Review Services Division\r\n\r\nPeer Review Report\r\nReferral Date: 01/28/2015 Review Type: Workers Comp\r\nClaimant\u2019s Name: Kim Lavallais Group/Policy/ Claim Number: 301421949300001IF\r\nMES Case Number: 31815009679 Service: Prospective/Pre-\r\nCertification\r\nClient: Sedgwick Referred By: Mary Wigley\r\n\r\nDATA REVIEWED AND CONTACT INFORMATION:\r\nData reviewed consisted of the Sedgwick CMS referral form and the submitted clinical documentation.\r\n\r\ne Sedgwick IL Referral Form dated 01/28/2015\r\ne Encounter Summary from Sarkis M. Bedikian, DO dated 01/27/2015\r\ne Letter from Loyola University Medical Center to Exam Works dated 10/16/2014\r\n\r\nThe attending provider was called on 01/28/2015 at 5:30 p.m. PST and I spoke with Tanisha. My call back information\r\nwas provided along with the reason for the call to include additional exam findings for the injection requested. The due\r\ndate and time was provided.\r\n\r\nSUMMARY OF RECORDS:\r\n\r\nThis is a female claimant with reported muscle weakness, arthralgias and joint pain in the right knee. She reports falls in\r\nthe past year. Her current medications include Tylenol #3, hydrocodone, ibuprofen, and tramadol. She also has had a\r\nKenalog injection. She is currently not working. The examination reveals a right knee with tenderness, an antalgic gait,\r\nrange of motion with crepitus, pain at extremes, and strength is 4/5. X-rays are said to reveal degenerative joint disease.\r\nAn MRI is said to reveal evidence of chondromalacia of the undersurface of the patella. The assessment includes\r\nosteoarthritis (OA) of the knee and a sprain of the medial collateral ligament of the knee. The recommendation is for a\r\nhyaluronic acid injection.\r\n\r\nREVIEW QUESTION (S):\r\n1. Is the request for Monovisc injection to the right knee medically necessary?\r\n\r\nA Monovise injection to the right knee is medically necessary.\r\n\r\nPer ODG, \u201cPatients experience significantly symptomatic osteoarthritis but have not responded adequately to\r\nrecommended conservative nonpharmacologic (e.g., exercise) and pharmacologic treatments or are intolerant of these\r\ntherapies (e.g., gastrointestinal problems related to anti-inflammatory medications), after at least 3 months;\r\n\u00abDocumented symptomatic severe osteoarthritis of the knee, which may include the following: Bony enlargement; Bony\r\ntenderness; Crepitus (noisy, grating sound) on active motion; Less than 30 minutes of morning stiffness, No palpable\r\nwarmth of synovium; Over 50 years of age.\r\n\r\n\u00abPain interferes with functional activities (e.g., ambulation, prolonged standing) and not attributed to other forms of joint\r\ndisease;\r\n\r\n+ Failure to adequately respond to aspiration and injection of intra-articular steroids\u201d\r\n\r\nThe guideline criteria have been met as the claimant complains of continued knee pain and weakness with falls. The\r\nexam reveals tenderness, an antalgic gait, range of motion with crepitus, pain at extremes, and strength is 4/5. There is\r\ndetailed evidence submitted of weeks-month(s) of a recent, reasonable and comprehensive non-operative treatment\r\nprotocol trial and failure, such as medications, activity modification, and cortisone injections. As such, due to the\r\nevidence of OA the request is indicated. Therefore, a Monovisce injection to the right knee is medically necessary.",
    "Conflict of Interest Attestation:\r\n\r\nI certify that I do not accept compensation for review activities that is dependent in any way on the specific outcome of\r\nthe case. To the best of my knowledge I was not involved with the specific episode of care prior to referral of the case for\r\nreview. I do not have a material professional, familial, or financial conflict of interest (financial conflict of interest is\r\ndefined as ownership interest of greater than 5%) regarding any of the following: the referring entity; the insurance\r\nissuer or group health plan that is the subject of the review; the covered person whose treatment is the subject of the\r\nreview and the covered person\u2019s authorized representative, if applicable; any officer, director or management employee\r\nof the insurance issuer that is the subject of the review; any group health plan administrator, plan fiduciary, or plan\r\nemployee; the health care provider, the health care provider\u2019s medical group or independent practice association\r\nrecommending the health care service or treatment that is the subject of the review, the facility at which the\r\nrecommended health care service or treatment would be provided; or the developer or manufacturer of the principle\r\ndrug, device, procedure or other therapy being recommended for the covered person whose treatment is the subject of\r\nthe review.\r\n\r\nI attest that I have a scope of licensure or certification and professional experience that typically manages the medical\r\ncondition, procedure, treatment, or issue under review.\r\n\r\nLy NT, MD\r\n\r\nDavid H. Trotter, M.D.\r\n\r\nBoard Certified in Orthopaedic Surgery\r\nCA License #G87941\r\n\r\nIL License #36062856\r\n\r\nTX License #L3854\r\n\r\nKY License #45796\r\n\r\nFL License #ME114976\r\n\r\n01/29/2015\r\n\r\nGUIDELINE:\r\n\r\nODG Criteria for Hyaluronic acid injections:\r\n\r\n+ Patients experience significantly symptomatic osteoarthritis but have not responded adequately to recommended\r\nconservative nonpharmacologic (e.g., exercise) and pharmacologic treatments or are intolerant of these therapies (e.g.,\r\ngastrointestinal problems related to anti-inflammatory medications), after at least 3 months;\r\n\r\n\u00abDocumented symptomatic severe osteoarthritis of the knee, which may include the following: Bony enlargement; Bony\r\ntenderness; Crepitus (noisy, grating sound) on active motion; Less than 30 minutes of morning stiffness, No palpable\r\nwarmth of synovium; Over 50 years of age.\r\n\r\n\u00abPain interferes with functional activities (e.g., ambulation, prolonged standing) and not attributed to other forms of joint\r\ndisease;\r\n\r\n+ Failure to adequately respond to aspiration and injection of intra-articular steroids;\r\n\r\n* Generally performed without fluoroscopic or ultrasound guidance;\r\n\r\n\u00ab Are not currently candidates for total knee replacement or who have failed previous knee surgery for their arthritis,\r\nunless younger patients wanting to delay total knee replacement. (Wen, 2000)\r\n\r\n\u00ab Repeat series of injections: If documented significant improvement in symptoms for 6 months or more, and symptoms\r\nrecur, may be reasonable to do another series. No maximum established by high quality scientific evidence, see Repeat\r\nseries of injections above.\r\n\r\n\u00ab Hyaluronic acid injections are not recommended for any other indications such as chondromalacia patellae, facet joint\r\narthropathy, osteochondritis dissecans, or patellofemoral arthritis, patellofemoral syndrome (patellar knee pain), plantar\r\nnerve entrapment syndrome, or for use in joints other than the knee (e.g., ankle, carpo-metacarpal joint, elbow, hip,\r\nmetatarso-phalangeal joint, shoulder, and temporomandibular joint) because the effectiveness of hyaluronic acid\r\ninjections for these indications has not been established.",
    "** INBOUND NOTIFICATION : FAX RECEIVED SUCCESSFULLY **\r\n\r\nTIME_RECEIVED REMOTE CSID DURATION PAGES STATUS\r\nApril 20, 2015 10:05:26 AM EDT SEDGWICK 204 5 Received\r\n0472072015 9:02:05 AM -0500 SEDGWICK PAGE I OF 5\r\n\r\nSedgwick Claims Management Services, Inc.\r\n\r\nTo: sir\r\n\r\nFax Number: 8592804853\r\n\r\nFrom: Isom, Angela\r\n\r\nFax Number:\r\n\r\nDate: April 20, 2015\r\n\r\nSubject: 301421949300001/KIM LAVALLAIS\r\nMemo:\r\n\r\nThe information transmitted is intended only for the person or entity to which it is addressed and may contain\r\nconfidential and/or privileged material. Any review, retransmission, dissemination or other use of, or taking of any\r\naction in reliance upon this information by persons or entities other than the intended recipient is prohibited. If you\r\nreceived this in error, please contact the sender and delete the material from any computer.\r\n\r\nThe information transmitted is intended only for the person or entity to which it is addressed and may contain\r\nconfidential and/or privileged material. Any review, retransmission, dissemination or other use of, or taking of any\r\naction in reliance upon this information by persons or entities other than the intended recipient is prohibited. If you\r\nreceived this in error, please contact the sender and delete the material from any computer.\r\n\r\n\u201cCONFIDENTIALITY NOTE***\r\n\r\nThe information contained in this facsimile message may be legally privileged\r\nand confidential information intended only for the use of the individual or\r\n\r\nentity named above. If the reader of this message is not the intended recipient,\r\nyou are hereby notified that any dissemination, distribution, or copying of this\r\ntelecopy is strictly prohibited. If you have received this telecopy in error,\r\n\r\nplease notify us immediately by calling the number listed above and return the\r\noriginal message to us at the address above by the United States Postal Service.",
    "O4/40/420109 9:02:00 AM \u2014O000 SEDGWICK PAGE 4 OF 9\r\n\r\n** INBOUND NOTIFICATION : FAX RECEIVED SUCCESSFULLY **\r\n\r\nTIME RECEIVED REMOTE CSID PAGES STATUS\r\nApril 13, 2015 1:25:49 pM EDT 630 789 1606 4 Received\r\nD7979D8B-B8EB - 41CA-9775-2230D39FF58E- 490908 - IF\r\nApr 1416 11:19a Paul D Belich MD 630 789 1606 p1\r\n\r\nz = LOYOLA 2160 South First Avenue\r\n\r\n~ 7 Bldg 105 Ste 1700\r\n\r\n2 UNIVERSITY Paul Belich MD Mapwoot TT, 60133\r\n\r\ni) MEDICAL CENTER\r\nfelephone: (708) 216-5995\r\nOutpatient Appts: (708) 216-8563\r\nFax: (708) 216-5858\r\n\r\nLoyola University Chicago\r\nDepartment of Orthopaedic Surgery and Rehabilitation\r\n\r\nApril 9, 2015\r\n\r\nExam Works\r\n2450 Rim Rock Road Suite 210\r\n\r\nMadison, WI 53713\r\n\r\nRE: LAVALLAIS, KIM\r\nMED REC#: 2725043\r\n\r\nTo Whom It May Concern:\r\n\r\nOn April 9, 2015, I was asked to see Ms. Kim Lavallais for the purpose of a repeat Independent Medical\r\nEvaluation. The history of her work accident has been described in the previous Independent Medical\r\nEvaluation. On May 15, 2014, apparently there was a food fight in the lunchroom and she slipped on an\r\norange that was on the floor and twisted her right knee. She states that her right knee popped and as she\r\nstumbled, she hit her right shoulder on a table. She did not fall to the ground. At the time, she\r\nreferenced an MRI to her knee which she states showed meniscus tears. Since that evaluation, she has\r\nbeen seen by an orthopaedic doctor who apparently has given her injections into her knee with no telief\r\nwhatsoever. She states that she still has pain in the right knee. She indicates to me that a total knee\r\narthroplasty has been recommended. I asked her if she had another set of x-rays since the first x-rays\r\nand specifically, I asked her if she had x-rays standing of her knees and she relayed to me that she did\r\nnot have standing x-rays. Apparently the orthopaedic surgeon is recommending a total knes\r\narthroplasty.\r\n\r\nPRIOR HOSPITALIZATIONS AND SURGERIES: None.\r\n\r\nALLERGIES: None.\r\n\r\nCURRENT MEDICATIONS: \u2018lramadol.\r\nREVIEW OF SYSTEMS: All systems reviewed in the patient intake form.\r\n\r\nFAMILY MEDICAL HISTORY: Positive for arthritis.\r\n\r\nLAVALLAIS, KIM lof4 4/9/2015",
    "O4/40/4019 9:02:00 AM \u2014O000 SEDGWICK PAGE 3 OF 93\r\nApr 1415 11:19a Paul D Belich MD 630 789 1606 p.2\r\n\r\nSOCIAL HISTORY: She is an occasional smoker, less than a pack a day; occasional drinker.\r\n\r\nREVIEW OF RECORDS: | did review my previous Independent Medical Evaluation which was done\r\non October 16, 2014. At the time, the MRI of the right knee done on June 6, 2014, was read as showing\r\nthinning of the articular cartilage of the patella. I reviewed the films myself and agreed that there were\r\nsome articular surface changes of the patella, but otherwise no other evidence of degenerative arthritis in\r\n\r\nthe medial and lateral compartments and no meniscal tears.\r\n\r\nI reviewed notes by Dr. Kyle Geissler and this was apparently from Austin Family Health. There was a\r\nnote from June 11, 2014, where he indicated that the patient may work four hours a day and return to\r\nwork full duty on June 30, 2014. She apparently was followed up on July 1, 2014, where she was now\r\nkept off work and sent to therapy. On September 5, 2014, she was also in therapy and not working. On\r\nOctober 16, 2014, an orthopaedic consultation was recommended and on December 18, 2014, she was\r\nhaving increased shoulder pain with flexion of 90 and abduction of 100 degrees.\r\n\r\nI reviewed treatment notes from Dr. Sarcus Vedikian with the first notation on December 29, 2014. He\r\nfound that she had tenderness in the medial and lateral patellar facets and the medial fernoral and medial\r\ntibial articular surfaces. There was medial joint line tenderness and tendemess at the MCL. There was\r\npatellofemoral crepitation. He diagnosed her with patellofemoral chondromalacia, osteoarthritis of the\r\nright knee and MCL sprain of the right knee. He gave her a steroid injection into the right knee. On\r\nJanuary 27, 2015, she returned saying that the right knee pain was 5 to 10/10 and the physical\r\nexamination was identical. She had no relief from the injection. He recommended a hyaluronic acid\r\ninjection and on February 10, 2015, she reviewed the first injection. She returned on March 10, 2015,\r\nwith no change in her symptoms and a right total knee arthroplasty was recommended.\r\n\r\nPHYSICAL EXAMINATION: The patient had a nonreciprocal slightly right antalgic gait. She\r\nappeared to have her knee buckle during the weightbearing portion of gait. There was no increased\r\nvarus or valgus to the knee during stance. When I asked her to point to the area of the knee where she\r\nhurt, she pointed all over. She stated that the knee hurts everywhere. Specifically to palpation, she had\r\nmedial joint line tenderness, lateral joint line tenderness and patellofemoral tenderness. There was\r\nsomewhat reactive type withdrawal behavior during palpation. She had no effusion in the knee. Her\r\nrange of motion was 100 degrees of flexion, and full extension. Initially when asked to flex her knee,\r\nshe could only flex it to about 60 degrees, but with some assistance, got to 100 degrees. The collateral\r\nligaments were stable on full extension and 30 degrees of flexion. The Lachman and drawer at 90 were\r\nnegative. She had no patellofemoral crepitation that I could note today. Circumferential measurements\r\n\r\nof the distal thigh were 12-3/4 bilaterally. Motor and sensation were intact to her right leg.\r\nDISCUSSION:\r\n\r\n1. The patient's diagnosis is post sprain, right knee and patellofemoral chondromalacia of the right\r\nknee. I believe the sprain and the symptoms of patellofemoral choendromalacia are related to the\r\nMay 15, 2014, work injury. She has pain at the patellofemoral joint, but as noted above, she also\r\nhas pain everywhere else in the joint which really cannot be directly related to her diagnosis of\r\npatellofemoral chondromalacia.\r\n\r\n4. I believe that the work injury is still a contributing factor to her current diagnosis.\r\n\r\nLAVALLAIS, KIM 2 of 4 4/9/2015",
    "O4/ 2420/2015\r\nApr 1415 11:19a\r\n\r\n3.\r\n\r\n3:02:00 AM \u20140900 SEDGWICK PAGE 4 OF 93\r\nPaul D Belich MD 630 789 1606 p.3\r\n\r\nI have stated that the work injury is a contributing factor. I believe the pop that she heard in her\r\nknee was probably from the patellofemoral joint, as she was stumbling and this became the source\r\nof her pain initially.\r\n\r\nI believe that the work incident did aggravate a pre-existing condition and ] would have expected\r\nthis to be a temporary aggravation with appropriate treatment She has had some spotty physical\r\ntherapy 2nd I am not sure if she really cooperated. well with this therapy, but certainly it did not\r\nappear tc give her any relief. 1 would expect it to get relief from a patellofemoral condition from\r\nphysical therapy.\r\n\r\nShe has had therapy, medication and injections as treatment since her prior Independent Medical\r\nEvaluation in my office. I believe those treatments have been reasonable and necessary. The\r\npatient, however, is not responding to what | would consider to be very appropriate treatment for\r\nher diagnosis.\r\n\r\nI asked this patient if she had x-rays standing of her knee and in my review of the records, I did\r\nnot see any standing x-rays reported. I see no evidence of any standing x-rays of this patient's\r\nknees during her visits to the orthopaedic surgeon. I saw no x-rays described there, so if any were\r\ntaken, they were not noted in my review of the records. I think the standard of care for treating\r\nthis patient would be to obtain a set of standing weightbearing x-rays of the knees as well as\r\npatellar or skyline views of the knees to assess the joint surfaces of her right knee. In addition, if\r\nthe joint spaces are not markedly decreased, | am wondering why ina 52-year-old female, why an\r\narthroscopy of the knee is not being done first to evaluate the joint and to check for any other\r\narticular pathology. If the joint spaces are maintained, after standing x-rays, it would seem to me\r\nthat an arthroscopic evaluation might be more appropriate than proceeding to a total knee\r\narthroplasty which J consider to be a much more significant procedure and certainly one that is not\r\nsupported by the MRI findings and is not at all supported by the fact that she has had no standing\r\nx-rays of her knees. Based on what I am seeing in diagnostic tests and on my examination, | have\r\nconcerns about a patient with such reactive behavior with pain everywhere, but with no arthritic\r\nfindings in much of the areas of her knee joint as to why she would be a candidate for a knee\r\nreplacement. Specifically patients who have significant patellofemoral arthritis of the knee with\r\nbone-on-bone patellofemoral joints localize their pain specifically to the patellofemoral joints and\r\nthey do not have generalized pain with reactive behavior as such as I have seen twice in\r\nevaluating this patient. ] have concerns as to whether this patient will do well after a total knee\r\narthroplasty considering the way she presents herself in my office today and at the time of her\r\nprevious Independent Medical Evaluation. 1 would recommend a well supervised course of\r\ntherapy three times a week for 6 to 8 weeks,a patellar brace and non-steroidal medication before\r\nconsidering any type of surgery on this patient.\r\n\r\nI have said in the past that I think she needs a Functional Capacity Evaluation and I think she is\r\ngoing to have to have one before any attempt is going to be to return her to work. I will say that\r\nshe does not appear to be motivated at ali to return to work, at least by what I have seen on exam\r\nin the two visits with her. I could really not even attempt to say what her restrictions would be, but\r\nI think a Functional Capacity Evaluation might help us with this. \\\r\n\r\nIt does not appear that she has reached maximum medical improvement with regards to this\r\nmatter. I, at this point, cannot give an estimation as to maximum medical improvement. I think\r\nthis patient needs to have standing x-rays of her knee and I think those should be evaluated first\r\n\r\nbefore consideration needs to be made towards any further surgical treatment.\r\n\r\nLAVALLAIS, KIM 3 of 4 4/9/2015",
    "O4/40/4019 9:02:00 AM \u2014O000 SEDGWICK PAGE 93 OF 93\r\nApr 1415 11:20a Paul D Belich MD 630 789 1606 p.4\r\n\r\nIf there are any further questions, please feel free to contact me.\r\n\r\nSincerely,\r\n\r\na, LD bbux ay\r\n\r\nPaul Belich MD\r\nPB/bg\r\n\r\nLAVALLAIS, KIM 4 of 4 4/9/2015",
    "Lexington, KY 40512-4666\r\n\r\nExamWorks, Inc.\r\n\r\n2450 Rimrock Road, Suite 303\r\n\r\nMadison, Wi 53713\r\nPhone: (608) 442-8474\r\nFax: (855) 865-1247\r\nwww.examworks.com\r\n\r\nVint MENU AOD\r\n. ee\r\nInvoice\r\nBill To Invoice Number 280-80355\r\nAngela Isom Invoice Date 8/7/2014\r\nSedgwick CMS Examinee\r\nPO Box 14446\r\n\r\nKim Lavallais >\r\nCtaim Number 301421949300001\r\n\r\nCase Number 134284\r\n\r\nExpert Dr. Paul Belich\r\nSpecialty Orthopaedic Surgery\r\nTerms Due Upon Receipt\r\n. CPT cg Unit Extended\r\nDate Units Code Description Amount Amount\r\n\r\n8/7/2014 1.00\r\n\r\nNo Show Independent Medical Evaluation | $1,200.00 $1,200.00\r\n\r\n- Provider: Paul Belich, M.D. -\r\nOrthopaedic Surgery, Examinee: Kim\r\nLavallais Claim#: 301421949300001\r\n\r\n8/7/2014 1.00\r\n\r\nMileage payment to claimant for IME $6.33 $6.33\r\n\r\nInvoice Total\r\n\r\n$1,206.33\r\n\r\n~** NO BILL REVIEW - NO REDUCTION ALLOWED *****\r\n\u201c4 NO BILL REVIEW - NO REDUCTION ALLOWED *****\r\n**** NO BILL REVIEW - NO REDUCTION ALLOWED *****\r\n\r\n(en {O\r\n\r\n194\r\n\r\nPlease Remit Payment To:\r\n2450 Rimrock Road, Suite 303\r\nMadison, WI 53713\r\nPhone: (888) 588-9292\r\nFax: (855) 865-1247\r\nFederal Tax 1D: 26-1114252",
    "Peer Review Services Division\r\n\r\nPeer Review Report\r\nReferral Date: 09/25/14 Review Type: Workers Comp\r\nClaimant\u2019s Name: Kim Lavallais Group/Policy/ Claim Number: 301421949300001IF\r\nMES Case Number: 31814095539 Service: Prospective Concurrent\r\nClient: Sedgwick Referred By: Wendy Wesley\r\n\r\nDATA REVIEWED AND CONTACT INFORMATION:\r\nData reviewed consisted of the Sedgwick CMS referral form and the submitted clinical documentation.\r\n\r\nI called the attending provider (AP) on 9/24/14 at 3:15 p.m. and a detailed voice mail and call back number was left. On\r\n9/25/14 at 9:39 a.m. I called again and on a recording left a message with my call back number.\r\n\r\nSUMMARY OF RECORDS:\r\n\r\nKim Lavallais is a 51-year-old female diagnosed with a sprain in the knee/leg, joint pain in the leg, and osteoarthrosis in\r\nthe leg. On 6/11/14, she saw Dr. Geissler where she complained of the pain in her right knee and right shoulder. She\r\ndescribed it as 4/10, comes and goes, aching, and throbbing. She had been using a crutch intermittently and reported\r\nmoderate improvement in symptoms of pain and swelling. She also reported improvement in her right arm stiffness and\r\npain. Her MRI showed degenerative arthritis of the right knee and mucoid degeneration in the medial and lateral menisci.\r\nShe was recommended to go to physical therapy.\r\n\r\nREVIEW QUESTION (S):\r\n1. Is additional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee medically necessary?\r\n\r\nAdditional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee is not medically necessary; however,\r\nadditional Physical Therapy #6 visits are medically necessary.\r\n\r\nODG supports an initial course of physical therapy with objective functional deficits and functional goals\r\n\r\nAn additional six visits are indicated to augment the claimant\u2019s functional capacity given limited conservative treatment\r\noptions. Therefore, additional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee is not medically\r\nnecessary; however, additional Physical Therapy #6 visits are medically necessary.\r\n\r\nConflict of Interest Attestation:\r\n\r\nI certify that I do not accept compensation for review activities that is dependent in any way on the specific outcome of\r\nthe case. To the best of my knowledge I was not involved with the specific episode of care prior to referral of the case for\r\nreview. I do not have a material professional, familial, or financial conflict of interest (financial conflict of interest is\r\ndefined as ownership interest of greater than 5%) regarding any of the following: the referring entity; the insurance\r\nissuer or group health plan that is the subject of the review; the covered person whose treatment is the subject of the\r\nreview and the covered person\u2019s authorized representative, if applicable; any officer, director or management employee\r\nof the insurance issuer that is the subject of the review; any group health plan administrator, plan fiduciary, or plan\r\nemployee; the health care provider, the health care provider\u2019s medical group or independent practice association\r\nrecommending the health care service or treatment that is the subject of the review, the facility at which the\r\nrecommended health care service or treatment would be provided; or the developer or manufacturer of the principle\r\n\r\ndrug, device, procedure or other therapy being recommended for the covered person whose treatment is the subject of\r\nthe review.\r\n\r\nI attest that I have a scope of licensure or certification and professional experience that typically manages the medical\r\ncondition, procedure, treatment, or issue under review.",
    "Moshe M. Lewis, M.D.\r\nBoard Certified in Physical Medicine & Rehabilitation\r\nAdded Expertise in Pain Medicine\r\nCA License #490204\r\nCO License #DR48550\r\nFL License #ME108489\r\nGA License #065700\r\nIL License #036126082\r\nCT License #49939\r\n09/25/2014\r\n\r\nREFERENCES:\r\nODG \u2014 Knee Chapter\r\n\r\nPatients should be formally assessed after a \"six-visit clinical trial\" to see if the patient is moving in a positive direction,\r\nno direction, or a negative direction (prior to continuing with the physical therapy)\r\n\r\nADDENDUM\r\nReason for Addendum: AP contact established\r\n\r\nOn 9/26/14 at 2:02 p.m. I spoke with Dr. Geissler who stated the claimant required additional physical therapy for knee\r\nand functional range. She has difficulty walking.\r\n\r\nWher fe fears\r\n\r\nMoshe M. Lewis, M.D.\r\nBoard Certified in Physical Medicine & Rehabilitation\r\nAdded Expertise in Pain Medicine\r\nCA License #490204\r\nCO License #DR48550\r\nFL License #ME108489\r\nGA License #065700\r\nIL License #036126082\r\nCT License #49939\r\n09/26/2014",
    "Peer Review Services Division\r\n\r\nPeer Review Report\r\nReferral Date: 09/25/14 Review Type: Workers Comp\r\nClaimant\u2019s Name: Kim Lavallais Group/Policy/ Claim Number: 301421949300001IF\r\nMES Case Number: 31814095539 Service: Prospective Concurrent\r\nClient: Sedgwick Referred By: Wendy Wesley\r\n\r\nDATA REVIEWED AND CONTACT INFORMATION:\r\nData reviewed consisted of the Sedgwick CMS referral form and the submitted clinical documentation.\r\n\r\nI called the attending provider (AP) on 9/24/14 at 3:15 p.m. and a detailed voice mail and call back number was left. On\r\n9/25/14 at 9:39 a.m. I called again and on a recording left a message with my call back number.\r\n\r\nSUMMARY OF RECORDS:\r\n\r\nKim Lavallais is a 51-year-old female diagnosed with a sprain in the knee/leg, joint pain in the leg, and osteoarthrosis in\r\nthe leg. On 6/11/14, she saw Dr. Geissler where she complained of the pain in her right knee and right shoulder. She\r\ndescribed it as 4/10, comes and goes, aching, and throbbing. She had been using a crutch intermittently and reported\r\nmoderate improvement in symptoms of pain and swelling. She also reported improvement in her right arm stiffness and\r\npain. Her MRI showed degenerative arthritis of the right knee and mucoid degeneration in the medial and lateral menisci.\r\nShe was recommended to go to physical therapy.\r\n\r\nREVIEW QUESTION (S):\r\n1. Is additional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee medically necessary?\r\n\r\nAdditional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee is not medically necessary; however,\r\nadditional Physical Therapy #6 visits are medically necessary.\r\n\r\nODG supports an initial course of physical therapy with objective functional deficits and functional goals\r\n\r\nAn additional six visits are indicated to augment the claimant\u2019s functional capacity given limited conservative treatment\r\noptions. Therefore, additional Physical Therapy 2-3X/wk for 12 more visits for the Right Knee is not medically\r\nnecessary; however, additional Physical Therapy #6 visits are medically necessary.\r\n\r\nConflict of Interest Attestation:\r\n\r\nI certify that I do not accept compensation for review activities that is dependent in any way on the specific outcome of\r\nthe case. To the best of my knowledge I was not involved with the specific episode of care prior to referral of the case for\r\nreview. I do not have a material professional, familial, or financial conflict of interest (financial conflict of interest is\r\ndefined as ownership interest of greater than 5%) regarding any of the following: the referring entity; the insurance\r\nissuer or group health plan that is the subject of the review; the covered person whose treatment is the subject of the\r\nreview and the covered person\u2019s authorized representative, if applicable; any officer, director or management employee\r\nof the insurance issuer that is the subject of the review; any group health plan administrator, plan fiduciary, or plan\r\nemployee; the health care provider, the health care provider\u2019s medical group or independent practice association\r\nrecommending the health care service or treatment that is the subject of the review, the facility at which the\r\nrecommended health care service or treatment would be provided; or the developer or manufacturer of the principle\r\n\r\ndrug, device, procedure or other therapy being recommended for the covered person whose treatment is the subject of\r\nthe review.\r\n\r\nI attest that I have a scope of licensure or certification and professional experience that typically manages the medical\r\ncondition, procedure, treatment, or issue under review.",
    
    
]


# In[5]:


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

    
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    return  model
model_store_dir =r""
save_model_name =r""
max_length = 512
location = f'{model_store_dir}/{save_model_name}_{max_length}_tokenizer'
location = f'MODELS{os.sep}FINAL'
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
pipe,label_dict = category_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=20,device =device)

tokenizer_path = f'{location}{os.sep}Classfication_PAGE_SEGMENTER_512_BERT_BOUNDRY_PRE_TRAIN_512_tokenizer'
model_path = f'{location}{os.sep}Classfication_PAGE_SEGMENTER_512_BERT_BOUNDRY_PRE_TRAIN.model'
abs_label_path = f'{location}{os.sep}PAGE_SEGMENTER_ImageText_label_dict.json'

segmenter_pipe,label_dict_segmenter = segmenter_pipe(abs_label_path,model_checkpoint,max_length,tokenizer_path,tokenizer_instance = BertTokenizer,num_labels=2,device =device)


tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}


def predict_category(pages,label_dict):
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}
    id2label = {'LABEL_' + str(value) : key for key, value in label_dict.items() }
    print(id2label)
    result = pipe(my_pages,**tokenizer_kwargs)
    label_result = [ id2label.get( _.get('label') ) for _ in result ]
    print(result)
    print(label_result)
    return label_result

def predict_segment(pages,label_dict):
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,}
    id2label = {'LABEL_' + str(value) : key for key, value in label_dict.items() }
    print(id2label)
    result = segmenter_pipe(my_pages,**tokenizer_kwargs)
    label_result = [ id2label.get( _.get('label') ) for _ in result ]
    print(result)
    print(label_result)
    return label_result


# predict_category(my_pages,label_dict)       
# predict_segment(my_pages,label_dict_segmenter)   


# In[18]:


def process_pages(my_pages):
    category = predict_category(my_pages,label_dict)
    spacy_provider = entity_extract(my_pages)
    qa_provider = extract_qa(my_pages)
    segment = predict_segment(my_pages,label_dict_segmenter)  
    _ = []
    for i,j,k,m in zip(category,spacy_provider,qa_provider,segment):
        t = { 'category' : i,
             'segment': m,
              'ORG' : j,
              'info' : k
            }
        _.append(t)
    return _
process_pages(my_pages) 


# In[15]:


def process_pages(my_pages):
    category = predict_category(my_pages,label_dict)
    spacy_provider = entity_extract(my_pages)
    qa_provider = extract_qa(my_pages)
    _ = []
    for i,j,k in zip(category,spacy_provider,qa_provider):
        t = { 'category' : i,
              'ORG' : j,
              'info' : k
            }
        _.append(t)
    return _
process_pages(my_pages)   


# In[7]:


import spacy
import os, json
nlp=spacy.load('en_core_web_trf')
print("Models loaded")
#ruler = nlp.add_pipe("entity_ruler",after='ner')
text_file_path= r"provider.jsonl"
# ruler=nlp.add_pipe("entity_ruler").from_disk(text_file_path)

from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
model_name = "roberta-base-squad2"
qa_extraction_pipe = pipeline('question-answering', model='roberta-base-squad2', tokenizer=model_name)




# In[8]:


def entity_extract(pages):
    if isinstance(pages,str):
        doc = nlp(pages.lower())
        org = [ ent.text for ent in doc.ents if ent.label_ =='ORG' ]
        return [org]
    else:
        _ = []
        for page in pages:
            doc = nlp(page.lower())
            org = [ ent.text for ent in doc.ents if ent.label_ =='ORG' ]
            _.append(org)
        return _

# entity_extract(my_pages)


# In[ ]:


qa_config_file_path = "qa_config.json"


def extract_qa(pages):
    service_date = ["what is the Date of Service?",
                   "what is the Visit Date?",
                    "what is SVC date?",
                    "what is Encounter Date?",
                   ]
    patient_name = ["what is patient name?",
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
        return _    
extract_qa(my_pages)   


# In[ ]:


if __name__ == "__main__":
    server.run(host='0.0.0.0',port=6000, debug=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# import pandas as pd, os, re

# import numpy as np
# import pandas as pd
# import torch, random
# import torch.nn as nn

# from sklearn.metrics import classification_report
# import transformers
from transformers import AutoModel, BertTokenizerFast, BertForSequenceClassification, BertTokenizer, BertConfig
# from torch.utils.data import Dataset, TensorDataset
# from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import AdamW, get_linear_schedule_with_warmup
# from sklearn.metrics import f1_score
# import random
# from tqdm import tqdm
# from transformers import pipeline
import json, os

from transformers import AutoTokenizer , AutoModelForSequenceClassification



# In[ ]:


import mlflow
from datetime import datetime


# In[ ]:


config_dict = { "max_position_embeddings" :1024 , "vocab_size" :100000, 
              "hidden_dropout_prob" : 0.1, "attention_probs_dropout_prob": 0.2,
              }


# In[ ]:


140/35


# In[ ]:


import train
if __name__ == "__main__":
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    print("Current tracking uri: {}".format(mlflow.get_tracking_uri))
    sequence_length = 1024 # sys.argv[1] if sys.argv[1] else 1024
    vocab_size = 100000 #sys.argv[2] if sys.argv[2] else 100000
    hidden_dropout_prob = 0.1 # sys.argv[3] if sys.argv[3] else 0.1
    attention_probs_dropout_prob = 0.2 # sys.argv[4] if sys.argv[4] else 0.2
    config_dict = { "max_position_embeddings" :sequence_length , "vocab_size" :vocab_size, 
              "hidden_dropout_prob" : hidden_dropout_prob , "attention_probs_dropout_prob": attention_probs_dropout_prob,
              }

    file_dir = f'.{os.sep}DATA-SETS'
    file_name = r"cleaned_compiled_json_13-04-23_14_22_18.json"
    abs_file_name = os.path.join(os.getcwd(),file_dir,file_name)
    # print(f'Bert Custom Config:{bert_config}\n Training Data File Name:{abs_file_name}')
    
    date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S') 
    experiment_id = mlflow.create_experiment("page_categorizer" + date_time_ .upper())
    with  mlflow.start_run(
                        run_name='_'.join(["BERT",str(config_dict.get('max_position_embeddings'))] ),
                        experiment_id=experiment_id,
                        tags={"version": "v1", "priority": "P1"},
                        description="parent",
                            ) as parent_run:
        date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S') 
        mlflow.log_param("Paranet Run Start Time", date_time_)
        mlflow.log_param("File", abs_file_name)
        target_col_types =  ['ImageText', 'ImageText_Non_Blank','ImageText_Non_Blank_header_5','ImageText_Non_Blank_restrict_line_tokens_3','ImageText_Non_Blank_restrict_line_tokens_3_with_verb']
        for target_column in [target_col_types[0]]:
            with mlflow.start_run(
                                run_name=target_column,
                                experiment_id=experiment_id,
                                description=target_column,
                                nested=True,
                                    ) as child_run:
                mlflow.log_param("Target columns", target_column)
                mlflow.log_params(config_dict)
                    
                date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S')
                mlflow.log_param("Time", date_time_)
                
                target_variable = "category"
                model_checkpoint ="bert-base-uncased"
                tokenizer_name= "bert-base-uncased"
                model_max_length = 64
                max_length = 64
                batch_size = 32
                lr=1e-5
                
                eps = 1e-8
                epochs = 5
                json_data = read_utils.read_json(abs_file_name)
                df = read_utils.clean_json(json_data)
                label_dict = read_utils.df_label_dict_column(df,label=target_variable,)
                df = read_utils.clean_df(df,label_dict,label = target_variable)
                df = read_utils.split_data(df,label = target_variable)
                df = df.sample(frac=.10)
                
                # train.build_model(config_dict,abs_file_name,target_variable = target_variable,features = target_column,
                # model_checkpoint =model_checkpoint, 
                # model_instance = BertForSequenceClassification, tokenizer_name= tokenizer_name,
                # model_max_length = model_max_length, max_length = max_length, batch_size = batch_size,
                # lr = lr, eps = eps,optimizer_instance = AdamW , epochs = 2,
                #                )    
    

    
    
    
    
    


# In[ ]:


import read_utils


# In[ ]:


target_variable = "category"
model_checkpoint ="bert-base-uncased"
tokenizer_name= "bert-base-uncased"
model_max_length = 64
max_length = 64
batch_size = 32
lr=1e-5

eps = 1e-8
epochs = 5


# In[ ]:


file_dir = f'.{os.sep}DATA-SETS'
file_name = r"cleaned_compiled_json_13-04-23_14_22_18.json"
abs_file_name = os.path.join(os.getcwd(),file_dir,file_name)


# In[ ]:


json_data = read_utils.read_json(abs_file_name)
df = read_utils.clean_json(json_data)
label_dict = read_utils.df_label_dict_column(df,label=target_variable,)
df = read_utils.clean_df(df,label_dict,label = target_variable)
df = read_utils.split_data(df,label = target_variable)
df = df.sample(frac=.10)


# In[ ]:


df.columns


# In[ ]:


df['text'] = df['ImageText']
df['label'] = df['category']


# In[ ]:


df_train =  df.sample(frac=.10)
df_val =  df.sample(frac=.5)


# In[ ]:


df_val


# In[ ]:


from datasets import Dataset


# In[ ]:


train_dataset = Dataset.from_pandas(df_train)
test_dataset  = Dataset.from_pandas(df_val)


# In[ ]:


import mlflow

with mlflow.start_run(run_name="artifact_test") as run:
    artifact_uri = run.info.artifact_uri
    # mlflow.log_dict({"mlflow-version": "0.28", "n_cores": "10"}, "config.json")
    # config_json = mlflow.artifacts.load_dict(artifact_uri + "/config.json")
    print(artifact_uri)


# In[ ]:


mlflow.end_run()


# In[ ]:


mlflow.pytorch.autolog()


# In[ ]:


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("device:",device)


# In[ ]:


pip install  datasets


# In[ ]:


import os

import numpy as np
import pandas as pd
from datasets import load_dataset, load_metric
# from huggingface_hub import notebook_login
from matplotlib import pyplot as plt
from transformers import (
   AutoModelForSequenceClassification,
   BertForSequenceClassification,
   AutoTokenizer,
   Trainer,
   TrainingArguments,
)


# In[ ]:


tokenizer_name="bert-base-uncased"
model = BertForSequenceClassification.from_pretrained(tokenizer_name)
tokenizer = BertTokenizer.from_pretrained(tokenizer_name)


# In[ ]:


# train_dataset, test_dataset = load_dataset("imdb", split=["train", "test"])


# In[ ]:


training_args = TrainingArguments(
    num_train_epochs=2,
    output_dir="./output",
   logging_steps=500,

    push_to_hub=False,
)
training_args


# In[ ]:


train_dataset


# In[ ]:


feature = 'text'
def tokenize_function(examples):
    return tokenizer(examples[feature], padding="max_length", truncation=True)


train_dataset = train_dataset.map(tokenize_function,  batched=True)
test_dataset = test_dataset.map(tokenize_function,  batched=True)


# In[ ]:


train_dataset, test_dataset


# In[ ]:


metric = load_metric("accuracy")
labels= ['Medical' 'Non-Medical/Others']

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


# In[ ]:


import torch_metrics,mlflow, 


# In[ ]:


from transformers.integrations import MLflowCallback


# In[ ]:


trainer = Trainer(
   model=model,
   args=training_args,
   train_dataset=train_dataset,
   eval_dataset=test_dataset,
   compute_metrics = torch_metrics.f1_score_func,
    callbacks=[MLflowCallback]
   
)


# In[ ]:


mlflow.end_run()
mlflow.start_run(run_name="artifact_test_new")


# In[ ]:


os.environ["MLFLOW_EXPERIMENT_NAME"] = "trainer-mlflow-demo"
os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"


# In[ ]:


mlflow.end_run()
with mlflow.start_run(run_name="artifact_test_new") as new_run:
    mlflow.pytorch.autolog()
    mlflow.log_param('epoch',1)
    trainer.train()


# In[ ]:





# In[ ]:





# In[ ]:


train_dataset, test_dataset = load_dataset("imdb", split=["train", "test"])


# In[ ]:


import train
file_dir = f'.{os.sep}DATA-SETS'
file_name = r"cleaned_compiled_json_13-04-23_14_22_18.json"
abs_file_name = os.path.join(os.getcwd(),file_dir,file_name)
abs_file_name
# os.sep
os.path.isfile(abs_file_name)
# train.build_model(bert_config,abs_file_name,target_variable = "category",features='ImageText',
#                   model_checkpoint ="bert-base-uncased", 
#                   model_instance = BertForSequenceClassification, tokenizer_name= "bert-base-uncased",
#                   model_max_length = 1024, max_length=1024,batch_size = 5,
#                   lr=1e-5, eps=1e-8,optimizer_instance = AdamW , epochs=5,
#                )


# In[ ]:





# In[ ]:


# bert_sequence_config =  BertConfig()

# def intitialize_tokenizers(tokenizer_name="bert-base-uncased",max_length=512):    
#     tokenizer = BertTokenizer.from_pretrained(tokenizer_name, max_length = max_length ,
#                                               model_max_length = max_length,
#                                               do_lower_case=True )
#     return tokenizer
# tokenizer = intitialize_tokenizers(tokenizer_name="bert-base-uncased",)
# print(tokenizer)

# def initialize_model_raw(bert_sequence_config,model_object):
#     model = model_object(   bert_sequence_config )
#     return model
# model = initialize_model_raw(bert_sequence_config,BertForSequenceClassification)
# model.summary()


# In[ ]:





# In[ ]:




