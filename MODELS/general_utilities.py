import json,os
def load_json(dir_,file):
    data ={}
    with open( os.path.join(dir_,file) , "r") as fp:
        data = json.load(fp)
        # data_formatted_str = json.dumps(data, indent=2)
        # print(data_formatted_str)
    return data
import re
def format_data(my_sent):
    my_sent = my_sent.strip("\n")
    my_sent = re.sub(r'(\s)+',r'\1',my_sent)
    my_sent = my_sent.lower()
    return my_sent
