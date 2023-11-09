def batch_files_put_pull(hostname='prelsftp.preludesys.com',username='SFTP_AI-ML', password='M{\^SJ:FA$0*&L)',port=2332
                        ,ENVIRON=None):
    
    from paramiko.client import SSHClient
    import os
    client = SSHClient()
    # client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='prelsftp.preludesys.com',username='SFTP_AI-ML', password='M{\^SJ:FA$0*&L)',port=2332)
    # stdin, stdout, stderr = client.exec_command('ls -l')
    with client.open_sftp() as sftp:
        print("sftp established")
        ENVIRON = os.environ.get('ENVIRON')
        print('ENVIRON',ENVIRON)
        # ENVIRON = "/DEV"
        dir_ = 'FROM_KPO'
        files = [ file for file in sftp.listdir(os.path.join(ENVIRON,dir_)) if file.endswith('.json')]
        for file in files:
            remote_abs_file = os.path.join(ENVIRON,dir_,file)
            if file.startswith('Train_'):
                _dir = '/MODELS/KPO/TRG_SOURCE_DIR'
            elif file.startswith('Predict_'):
                _dir = '/MODELS/KPO/SOURCE_INFERENCE'
            else:
                continue
            local_abs_file = os.path.join(_dir,file)
            sftp.get(remote_abs_file,local_abs_file)
            print(abs_file)
        predicted_dir = '/MODELS/KPO/PREDICTED_INFERENCE'
        send_files = [ file for file in os.listdir(predicted_dir) file.endswith('.json') ]
        for file in send_files:
            local_abs_file = os.path.join(predicted_dir,file)
            dir_ = 'TO_KPO'
            remote_abs_file = os.path.join(ENVIRON,dir_,file)
            sftp.put(local_abs_file,remote_abs_file)
    
if  __name__== '__main__':
    batch_files_put_pull(hostname='prelsftp.preludesys.com',username='SFTP_AI-ML', password='M{\^SJ:FA$0*&L)',port=2332
                        ,ENVIRON=None)