import os
import read_utils
import init,torch_metrics, os, sys
import torch
import mlflow
import pandas as pd
from pathlib import Path
from torch.utils.data import Dataset, TensorDataset
from transformers import  BertForSequenceClassification, BertTokenizer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def iterative_model_training(
    file_dir,input_feature,target,
                             model_store_dir,
                             save_model_name,
                             max_length,
                             model_checkpoint,
                             tokenizer_instance,
                                model_instance,
                            num_labels,
                             epochs,
    batch_size,
                             exlcude=['Duplicates'],
                        file_type = ".json",
    MODEL_TYPE = "PAGE_CATEGORY"):
    
    

      print('Directory:',file_dir)
      print("Directory content:",os.listdir( os.path.join(file_dir)) )
      file_list = [ file for file in os.listdir( os.path.join(file_dir)) if os.path.isfile(os.path.join(file_dir,file) )
        and file.endswith(file_type)
        # and file not in ['21-123-1922_cleaned.json']
        #  and file.startswith("part_file_")
        ]
      print("File lists:",file_list)
      for file in file_list:
        with mlflow.start_run(run_name=file) as run:
            # mlflow.pytorch.autolog()
            abs_file_name = os.path.join(file_dir,file)
            print("Processing:",file,abs_file_name)
            # return
            df = pd.read_json(abs_file_name)
            df[input_feature] = df[input_feature].map(lambda x: ' '.join(x)  if isinstance(x,list) else  x)
            print(df.columns,df[target].unique())
            df = df[~df[target].isin(exlcude) ]
            df = df.dropna(subset=[input_feature,target])
            df = df[~df[input_feature].str.len()<=0 ]
            features= input_feature
            Target_variable = target
            label = Target_variable
            target_variable = label
            df[Target_variable] = df[Target_variable].map(lambda x: str(x))
            print(df.info())
            print(df.head(2))
         
            label_dict = read_utils.df_label_dict_column(df,label=Target_variable,target_columns = features,model_store_dir=model_store_dir,MODEL_TYPE=MODEL_TYPE)
            print(f"Label dict#####{label_dict}")
            df = read_utils.clean_df(df,label_dict,label = Target_variable)
            df = init.split_data(df,label=label)
            print("Unique Labels:",df[Target_variable].unique())
            print("size:",len(df))
            print(df[Target_variable])
            df = df.sample(frac=1)
            df_train = df[df.data_type=='train']
            df_test = df[df.data_type=='val'] 
            from datetime import datetime
            date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S')
            train_file_name_abs = os.path.join(os.environ['HOME'],r"KPO/TRAIN",Path(file).stem + f'_train_{date_time_}.json')
            val_file_name_abs = os.path.join(os.environ['HOME'],r"KPO/TEST",Path(file).stem +f'_val_{date_time_}.json') 
            with open(train_file_name_abs,"w") as fp:
              df_train.to_json(fp,indent=2,orient='records')
            with open(val_file_name_abs,"w") as fp:
              df_test.to_json(fp,indent=2,orient='records')        
            model_checkpoint 
            location = f'{model_store_dir}/{save_model_name}_{max_length}_tokenizer'
            tokenizer = init.intitialize_tokenizers_raw(tokenizer_name= model_checkpoint, 
                                                   max_length=max_length,tokenizer_instance = tokenizer_instance,
                                                   location= location
                                                       
                                                       )
            print('here:',df[df.data_type=='train'][label].values)
            dataset_train,dataset_val    =  init.tokenize_data_with_tokenizer(tokenizer,df,features=features,label=target_variable,
                                                    max_length=max_length,
                                                   model_store_dir = model_store_dir ,
                                             save_model_name = save_model_name
                                 
                                                                             )
            epochs = epochs
            batch_size = batch_size
            print(type(dataset_train))
            dataloader_train, dataloader_validation   = init.bind_data_loader(dataset_train,dataset_val,batch_size = batch_size)
            bert_sequence_config = None
            model = init.initialize_model_raw(bert_sequence_config,model_instance = model_instance,
                                 MODEL_STORE=model_store_dir,MODEL_NAME_STRING = save_model_name,model_check_point = model_checkpoint,
                                 num_labels = num_labels)
            optimizer = init.initalize_optimizer(model,  lr=1e-5, eps=1e-8)
            scheduler = init.iniatlize_scheduler_custom_param(dataloader_train,optimizer,epochs=epochs)
          
            init.initiate_training_custom(model,dataloader_train,dataloader_validation,
                                              epochs,model_store_dir,save_model_name,
                                           optimizer,scheduler)
            _, predictions, true_vals = torch_metrics.evaluate_model(dataloader_validation,model,device)
            t = torch_metrics.accuracy_per_class(predictions, true_vals,label_dict)
            print("t:",t)
            for i in t:
                class_ = i.get('Class')
                accuracy_ = i.get('Accuracy')
                predicted_ = i.get('predicted')
                actuals_ = i.get('actuals')
                mlflow.log_metric(class_,accuracy_)
                mlflow.log_param(f'{class_}_nums',f'{predicted_}/{actuals_}')


            #   with open(os.path.join(model_store_dir,"_valid_logs.json"),"w") as fw:      
            #     json.dump(data,fw)
            # os.rename(abs_file_name,f'{abs_file_name+"l"}')
      return 

# print(device)
# python3 -m train. "KPO/SOURCE"  "KPO/MODELS" "xyz" 512  "bert-base-uncased" 10  2 50 "ImageText"  'category' 'Duplicates' "PAGE_CATEGORY" ".json"
if __name__ =='__main__':
    import mlflow
    traking_uri = "http://10.10.0.7:8886"
    traking_uri = "http://10.10.0.7:5000"
    try:
        mlflow.set_tracking_uri(traking_uri)
    except Exception as e:
        print(e)    
    project_type= "Classfication"
    MODEL_TYPE = sys.argv[12] #"PAGE_CATEGORY"
    file_type = sys.argv[13] # ".json"
    base_model = "BERT"
    base_model_fine_tune ="BOUNDRY_PRE_TRAIN"
    file_dir = os.path.join(os.environ['HOME'],sys.argv[1]) 
    model_store_dir = os.path.join(os.environ['HOME'],sys.argv[2]) 
    
    # save_model_name =  sys.argv[3]
    max_length = int(sys.argv[4]) # 512
    save_model_name = '_'.join([project_type,MODEL_TYPE,str(max_length),base_model,base_model_fine_tune])

    model_checkpoint ="bert-base-uncased"
    tokenizer_instance = BertTokenizer
    model_instance = BertForSequenceClassification
    model_checkpoint = sys.argv[5] # "bert-base-uncased"
    
    epochs =  int(sys.argv[6])
    batch_size = int(sys.argv[7])
    num_labels= int(sys.argv[8])
    input_feature = sys.argv[9]
    target = sys.argv[10]
    exlcude= [sys.argv[11]] #['Duplicates']

    args = {'file_dir':file_dir,'model_store_dir':model_store_dir,'save_model_name':save_model_name,
            'max_length':max_length,'model_checkpoint':model_checkpoint,'epochs':epochs,
            'batch_size':batch_size, 'num_labels':num_labels,'input_feature':input_feature,
            'target':target,'exlcude':exlcude,'MODEL_TYPE':MODEL_TYPE,'file_type':file_type

    }
    print(f'Command line Args are : {args}')
    # iterative_model_training(file_dir,input_feature,target,
                             # model_store_dir,
                             # save_model_name,
                             # max_length,
                             # model_checkpoint,
                             # tokenizer_instance,
                                   # model_instance,
                                   # num_labels,
                             # epochs = epochs,
                                   # batch_size = batch_size,
                             # exlcude = exlcude,
                                   # file_type = ".json",
                                   # MODEL_TYPE = MODEL_TYPE
                            # )
    target = "Isstart"
    MODEL_TYPE = "PAGE_SEGMENTER"
    save_model_name = '_'.join([project_type,MODEL_TYPE,str(max_length),base_model,base_model_fine_tune])
    num_labels=2
    iterative_model_training(file_dir,input_feature,target,
                             model_store_dir,
                             save_model_name,
                             max_length,
                             model_checkpoint,
                             tokenizer_instance,
                                   model_instance,
                                   num_labels,
                             epochs = epochs,
                                   batch_size = batch_size,
                             exlcude = exlcude,
                                   file_type = ".json",
                                   MODEL_TYPE = MODEL_TYPE
                            )                            
    print("compltetd")
    sys.exit(0) 