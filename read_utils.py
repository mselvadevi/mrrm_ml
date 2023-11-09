import json, pandas as pd, os, numpy as np
file_dir = os.path.join(os.environ['HOME'],r"KPO/SOURCE")

def read_from_dir(dir_name=None,file_type=".json"):
  print("Directory:",file_dir)
  if dir_name is None:
    return None
  directory_files = [file_ for file_ in os.listdir(dir_name) 
  if file_.endswith(file_type) and os.path.isfile(os.path.join(dir_name,file_))
  #  and file_ not in ['21-123-1911.txt','21-123-1914.txt','21-123-1923_f.txt']
  #  and file_ in [ '21-123-1930.json' ]
                     ]
  print("directory_files:",directory_files,os.listdir(dir_name), dir_name)
  df = pd.DataFrame()
  for file_name in directory_files:
    if file_type == ".txt" or  file_type == ".json"  :
      print("File name:", file_name)
      df_new = read_json(file_name,file_dir,)
      print(df_new.columns)
      df = pd.concat([df,df_new])
  print(df.columns,df.info(),sep="#")
  uni = df['category'].unique()
  print(uni)
  return df
# read_from_dir(dir_name=file_dir)

def read_json(file_name,file_dir = file_dir,
                  features="Input",
                  labels="target"
                  ):
    json_dict = None
    abs_file_path = os.path.join(file_dir,file_name)
    with open(abs_file_path) as fp:
      json_dict = json.load(fp)
      for index,page_ in enumerate(json_dict):
        for key,value in page_.items():
          if value is np.nan:
            page_[key] = "None"
          if type(value) == list :
            stringfied = '\n'.join(value)
            page_[key] = stringfied
          if key == 'Isstart':
            if bool(value) == True:
              page_[key] = "START"
            else:
              page_[key] = "NO_START"
    df = pd.DataFrame(data=json_dict)
    
    df_new = pd.DataFrame(data=df,columns=['pagenumber','ImageText','category','Isstart'])
    print(df_new.columns)
    df_new.dropna(inplace=True)
    df_cleaned = df_new[ df_new['category'] != 'Duplicates']
    return df_cleaned

def read_json_file(file_name,file_dir = file_dir,
                  features="Input",
                  labels="target"
                  ):
    abs_file_path = os.path.join(file_dir,file_name)
    df = pd.read_json(abs_file_path)
    df.dropna(how="all", inplace=True)
    print("Columns:",df.columns)
    return df

def read_csv_file(file_name,file_dir = file_dir,
                  features="Input",
                  labels="target"
                  ):
    abs_file_path = os.path.join(file_dir,file_name)
    df = pd.read_csv(abs_file_path)
    df.dropna(how="all", inplace=True)
    print("Columns:",df.columns)
    return df

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
    # with open(os.path.join(model_store_dir,MODEL_TYPE + "_label_dict.json"),"w") as fp:
    #   json.dump(label_dict,fp,indent=4)
    return label_dict 
def df_label_dict_column(df,label='label',target_columns = 'ImageText',model_store_dir= os.path.join(os.environ['HOME'],r"KPO/MODELS"),
                        MODEL_TYPE = "PAGE_CATEGORY"
                        ):
    df = df[ df[label] != 'Duplicates']
    label_dict = None
    label_path = os.path.join(model_store_dir,MODEL_TYPE + "_" + target_columns + "_label_dict.json")
    print(f"label_path:{label_path}")
    if os.path.isfile( label_path)  :
      print(f"\t {label_path} exists")
      with open(label_path,"r") as fp:
        label_dict = json.load(fp)
    else:
        print(f"\t {label_path} does not exists")
        label_dict = None
    print("target labels:",label)
    unique_labels = [ str(i) if isinstance(i,np.bool_) else i for i in pd.unique(df[label]) ]
    print("unique labels:",unique_labels)
    if label_dict:
      new_list = [ i for i in unique_labels if i not in  list(label_dict.keys() ) ]
      print(f'New category keys to be added:{new_list}')
      for i in new_list:
          label_dict[i]=len(label_dict)
      print("if label_dict:",label_dict)
    else:
      unique_label_mapping = [ i for i in range(len(unique_labels))]  
      print("unique_label_mapping:",unique_label_mapping) 
      possible_labels = unique_labels
      label_dict = {tag:num for tag,num in zip(possible_labels,unique_label_mapping) }
      print("else label_dict:",label_dict)
    if label_dict:
      with open(label_path,"w") as fp:
        t ={}
        for key,value in label_dict.items():
          if isinstance(key,np.bool_):
            t[str(key)] = value
          else:
            t[key] = value
        print("t:",t,json.dumps(t),sep="#")
        json.dump(t,fp,indent=4)
        label_dict = t
      print("stored results")

    return label_dict     
# df_label_dict_column(df,label='category',target_columns = 'ImageText')
def clean_df(df,label_dict,label):
    df[label] = df[label].replace(label_dict)
    # df = df[df['category'] != 'Duplicates']
    print("df.columns:",df.columns)
    
    return df
def check_directory_exists(model_store_dir,file_dir):
  if os.path.exists(model_store_dir) and  os.path.exists(file_dir):
    print("Directories  exist",model_store_dir,file_dir,sep="\t#\t" )
    return 0
  else:
    print("Directories may not exist",model_store_dir,file_dir,sep="\t#\t" )
    return -1
def create_directories(list_of_directories):
  for i in list_of_directories:
    if os.path.exists(i):
      continue
    else:
      os.makedirs(i)
