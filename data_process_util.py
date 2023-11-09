import torch
from torch.utils.data import Dataset, TensorDataset, DataLoader,RandomSampler, SequentialSampler
def df_label_dict(df,label='label'):
    print("target labels:",label)
    unique_labels = pd.unique(df[label])
    print("unique labels:",unique_labels)
    unique_label_mapping = [ i for i in range(len(unique_labels))]
    print(unique_label_mapping)    
    possible_labels = unique_labels
    label_dict = {}
    for index, possible_label in enumerate(possible_labels):
        if possible_label is np.nan: print(index)
        label_dict[possible_label] = index
    print("label_dict:",label_dict)
    return label_dict 


def tokenize_data_with_tokenizer(tokenizer,df,features,label,max_length):   

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
    # dataset_val = tf.data.Dataset.from_tensor_slices((input_ids_val, attention_masks_val, labels_val)) 
    return dataset_train, dataset_val 

# dataset_train, dataset_val  = tokenize_data_with_tokenizer(tokenizer,df,features=features,label=label,max_length = max_length)
def bind_data_loader(dataset_train,dataset_val,batch_size = 3):
    dataloader_train = DataLoader(dataset_train, 
                                  sampler=RandomSampler(dataset_train), 
                                  batch_size=batch_size)
    dataloader_validation = DataLoader(dataset_val, 
                                       sampler=SequentialSampler(dataset_val), 
                                       batch_size=batch_size) 
    return dataloader_train, dataloader_validation     