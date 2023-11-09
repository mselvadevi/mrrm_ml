import read_utils, sys, os, data_process_util, torch_metrics
from transformers import AutoModel, BertTokenizerFast, BertForSequenceClassification, BertTokenizer, BertConfig, pipeline
from transformers import AdamW, get_linear_schedule_with_warmup
import pandas as pd, numpy as np, json
from tqdm import tqdm
import torch
import mlflow
import mlflow.pytorch
from mlflow import MlflowClient
import os
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, TensorDataset
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm
from transformers import pipeline
import torch_metrics

model_store_dir = os.path.join(os.environ['HOME'],r"KPO/MODELS")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
config_dict = { "max_position_embeddings" :512 , "vocab_size" :100000, 
              "hidden_dropout_prob" : 0.1, "attention_probs_dropout_prob": 0.2,
              }
def create_bert_config(config_dict = config_dict):
    config = BertConfig(  **config_dict )
    return config






def split_data(df,label):

    X_train, X_val, y_train, y_val = train_test_split(df.index.values, 
                                                      df[label].values, 
                                                      test_size=0.10, 
                                                      random_state=42, 
                                                      shuffle=True,
                                                      # df.label.values
                                                      )

    df['data_type'] = ['not_set']*df.shape[0]
    df.loc[X_train, 'data_type'] = 'train'
    df.loc[X_val, 'data_type'] = 'val'
    df.groupby([ label, 'data_type']).count()
    # print(df.head)
    return df

def intitialize_tokenizers(tokenizer_name="bert-base-uncased",max_length=512):    
    tokenizer = BertTokenizer.from_pretrained(tokenizer_name, max_length  ,
                                              model_max_length = max_length,
                                              do_lower_case=True )
    return tokenizer

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


                                              
def tokenize_data(df,features,label):   

    encoded_data_train = tokenizer.batch_encode_plus(
        df[df.data_type=='train'][features].values, 
        add_special_tokens=True, 
        return_attention_mask=True, 
        pad_to_max_length=True, 
        max_length=max_length, 
        return_tensors='pt'
        )    
    encoded_data_val = tokenizer.batch_encode_plus(
        df[df.data_type=='val'][features].values, 
        add_special_tokens=True, 
        return_attention_mask=True, 
        pad_to_max_length=True, 
        max_length=max_length, 
        return_tensors='pt'
    )
        
    input_ids_train = encoded_data_train['input_ids']
    attention_masks_train = encoded_data_train['attention_mask']
    labels_train = torch.tensor(df[df.data_type=='train'][label].values)

    input_ids_val = encoded_data_val['input_ids']
    attention_masks_val = encoded_data_val['attention_mask']
    labels_val = torch.tensor(df[df.data_type=='val'][label].values)

    dataset_train = TensorDataset(input_ids_train, attention_masks_train, labels_train)
    dataset_val = TensorDataset(input_ids_val, attention_masks_val, labels_val) 
    return dataset_train, dataset_val 

def tokenize_data_with_tokenizer(tokenizer,df,features,label,max_length,model_store_dir,save_model_name):   

    encoded_data_train = tokenizer.batch_encode_plus(
        df[df.data_type=='train'][features].values, 
        add_special_tokens=True, 
        return_attention_mask=True, 
        pad_to_max_length=True, 
        max_length=max_length,
        truncation=True,
        return_tensors='pt'

        )    
    encoded_data_val = tokenizer.batch_encode_plus(
        df[df.data_type=='val'][features].values, 
        add_special_tokens=True, 
        return_attention_mask=True, 
        pad_to_max_length=True, 
        max_length=max_length, 
        return_tensors='pt'

    )

        
    input_ids_train = encoded_data_train['input_ids']
    print(f'{encoded_data_train.keys()}')
    attention_masks_train = encoded_data_train['attention_mask']
    labels_train = torch.tensor(df[df.data_type=='train'][label].values)

    input_ids_val = encoded_data_val['input_ids']
    attention_masks_val = encoded_data_val['attention_mask']
    labels_val = torch.tensor(df[df.data_type=='val'][label].values)

    dataset_train = TensorDataset(input_ids_train, attention_masks_train, labels_train)
    dataset_val = TensorDataset(input_ids_val, attention_masks_val, labels_val) 

    tokenizer.save_pretrained(f'{model_store_dir}/{save_model_name}_{max_length}_tokenizer') 
    return dataset_train, dataset_val 
def bind_data_loader(dataset_train,dataset_val,batch_size = 3):
    dataloader_train = DataLoader(dataset_train, 
                                  sampler=RandomSampler(dataset_train), 
                                  batch_size=batch_size)
    dataloader_validation = DataLoader(dataset_val, 
                                       sampler=SequentialSampler(dataset_val), 
                                       batch_size=batch_size) 
    return dataloader_train, dataloader_validation                                  
                             


def initialize_model(label_dict,model_name = "bert-base-uncased"):
    model = BertForSequenceClassification.from_pretrained(model_name,
                                                          num_labels=len(label_dict),
                                                          output_attentions=False,
                                                          output_hidden_states=False,
                                                          max_position_embeddings= max_length ,
                                                          )
    return model


# def initialize_model_raw(label_dict,bert_sequence_config,model_name = "bert-base-uncased"):
#     model = BertForSequenceClassification(   bert_sequence_config )
#     return model

def load_model(model_path,label_dict,cpu_status = device,model_check_point = 'bert-base-uncased'):
    #label_dict = load_label_dict(model_store_dir = model_store_dir )
    tokenizer = BertTokenizer.from_pretrained(model_check_point, 
                                              do_lower_case=True)
    model = BertForSequenceClassification.from_pretrained(model_check_point,
                                                          num_labels=len(label_dict),
                                                          output_attentions=False,
                                                          output_hidden_states=False)

    
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    # model.load_state_dict(torch.load(model_path))
    return tokenizer, model,
def initialize_model_raw(bert_sequence_config,model_instance ,
                         MODEL_STORE,MODEL_NAME_STRING,
                         model_check_point, num_labels):
    model_files = [ ml_file for ml_file in os.listdir(MODEL_STORE)
                 if ml_file.endswith(".model") and ml_file.startswith(MODEL_NAME_STRING) 
                 and  os.path.isfile(os.path.join(model_store_dir,MODEL_NAME_STRING +".model") )
                 ] 
    print("MODEL_STORE:",MODEL_STORE)
    print("Model name string:",MODEL_NAME_STRING,sep="#")
    print(f' files are {os.listdir(MODEL_STORE)}')
    print("file model", os.path.join(model_store_dir,f'{MODEL_NAME_STRING}.model') )  
    print("file status:", os.path.isfile(os.path.join(model_store_dir,f'{MODEL_NAME_STRING}.model') )  ) 

    print(os.path.join(model_store_dir,f'{MODEL_NAME_STRING}.model'))
    print("model_files:",model_files)
    if model_files:
      model = model_instance.from_pretrained(model_check_point,
                                                          num_labels=num_labels,
                                                          output_attentions=False,
                                                          output_hidden_states=False)
      model_path = os.path.join(model_store_dir,f'{MODEL_NAME_STRING}.model')
      print(f"loading model file:{model_path}")
      model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    else:
      print(f"Loading Pretrained models from HuggingFace")
      model = model_instance.from_pretrained(model_check_point, 
                                             num_labels=num_labels,
                                             output_attentions=False,
                                                          output_hidden_states=False)
      # model = model_instance(   bert_sequence_config )
    return model

def initalize_optimizer(model,  lr=1e-5, eps=1e-8) :
    optimizer = AdamW(model.parameters(),
                      lr=1e-5, 
                      eps=1e-8)
    return optimizer            


def iniatlize_scheduler(dataloader_trainoptimizer,epochs=10):
    scheduler = get_linear_schedule_with_warmup(optimizer, 
                                                num_warmup_steps=0,
                                                num_training_steps=len(dataloader_train)*epochs)
    return  scheduler  
def iniatlize_scheduler_custom_param(dataloader_train,optimizer,epochs=10):
    scheduler = get_linear_schedule_with_warmup(optimizer, 
                                                num_warmup_steps=0,
                                                num_training_steps=len(dataloader_train)*epochs)
    return  scheduler        

def initiate_training_custom(model,dataloader_train,dataloader_validation,epochs,model_store_dir,save_model_name,
                             optimizer,scheduler):
    mlflow.pytorch.autolog()
    # progress_bar = tqdm(epochs, desc='Training in  {:1d} epochs'.format(epochs), leave=False, disable=False)
    for epoch in tqdm(range(1, epochs+1),position=0, leave=True):
        tqdm.write(f'Epoch : {epoch}')
        model = model.to(device, non_blocking=False)
        # model = model.to(device, non_blocking=True)
        model.train()

        loss_train_total = 0

        progress_bar = tqdm(dataloader_train,position=0, leave=True, desc='Epoch {:1d}'.format(epoch),  disable=False)
        for batch_idx,batch in enumerate(progress_bar):
            # print("Batching")
            model.zero_grad()
            
            batch = tuple(b.to(device) for b in batch)
            
            inputs = {'input_ids':      batch[0],
                      'attention_mask': batch[1],
                      'labels':         batch[2],
                     }       

            outputs = model(**inputs)
            # print("Batching ENDS")
            loss = outputs[0]
            loss_train_total += loss.item()
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            optimizer.step()
            scheduler.step()

        # from datetime import datetime
        # date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S')    
        # torch.save(model.state_dict(), f'{model_store_dir}_{save_model_name}_{epoch}_{date_time_}.model')
        
            
        # tqdm.write(f'\nEpoch {epoch}')
        
        loss_train_avg = loss_train_total/len(dataloader_train)            
        tqdm.write(f'Training loss: {loss_train_avg}')
        
        # val_loss, predictions, true_vals = evaluate(dataloader_validation)
        # trg_loss, predictions_trg, true_trg = evaluate_model(dataloader_validation,model,device)
        val_loss, predictions, true_vals = torch_metrics.evaluate_model(dataloader_validation,model,device)

        val_f1 = torch_metrics.f1_score_func(predictions, true_vals)
        tqdm.write(f'Validation loss: {val_loss}')
        tqdm.write(f'F1 Score (Weighted): {val_f1}')

        mlflow.log_metric("avg_train_losses", loss_train_avg, step=epoch)
        mlflow.log_metric("valid_loss", val_loss, step=epoch)
        # mlflow.log_metric(f'{epoch}',val_f1)
        # mlflow.log_metric('epochs',[1,2,3,4,5])
        # step = epoch * len(dataloader_train) + batch_idx
        # log_scalar('train_loss', loss.data.item(), step)
        # log_scalar('val_loss', val_loss, step)
        # log_scalar('test_accuracy', test_accuracy, step)
        # mlflow.log_metric('valid_loss', f'{val_loss}', step=step)
        # mlflow.log_metric('valid_loss',val_loss)

        # mlflow.log_metric('f1_score_val',val_f1)
        # mlflow.log_metric('train_loss',loss_train_avg)
        # progress_bar.set_postfix({'training_loss': '{:.3f}'.format(loss_train_total/len(batch))})        
    from datetime import datetime
    date_time_ =  datetime.now().strftime('%d-%m-%y_%H_%M_%S')
    print('Model device conversation')  
    model.to(device)
    print(f'Saving the model :{model_store_dir}/{save_model_name}.model')
    torch.save(model.state_dict(), f'{model_store_dir}/{save_model_name}.model')
    print('Model saved successfully')
    return None
    return model,      
# pipe_cuda = pipeline("text-classification", model = model, tokenizer = tokenizer,device="cuda:0")       