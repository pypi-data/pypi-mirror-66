import pandas as pd

def upload_df(file, encoding, dataframe_name):
    
    with open(file, encoding = encoding) as upload:
        texts = upload.read()
    
    texts = texts.split('\n')
    
    text_all = []
    for txt in texts:
        text_all.append(txt.split(' - '))
        
    text_date = []
    for txt in text_all:
        text_date.append(txt[0])
    
    text_hr = []
    for txt in text_date:
        text_hr.append(str(txt).split(' '))
    
    text_dt = []
    for txt in text_hr:
        text_dt.append(txt[0])
    
    for txt in text_hr:
        del txt[0]
    
    text_hr_clean = []
    for txt in text_hr:
        text_hr_clean.append(str(txt).replace('[', '').replace(']', ''))
    
    for txt in text_all:
        del txt[0]
    
    text_txt = []
    for txt in text_geral:
        text_txt.append(str(txt).replace("['", '').replace("']", ''))
    
    text_msg = []
    for txt in text_txt:
        text_msg.append(str(txt).split(': '))
     
    text_speaker = []
    for txt in text_msg:
        text_speaker.append(txt[0])
    
    for txt in text_msg:
        del txt[0]
    
    text_msg_clean = []
    for txt in text_msg:
        text_msg_clean.append(str(txt).replace('[', '').replace(']',''))

    dict_text = {}
    dict_text['Date'] = text_dt
    dict_text['Hour'] = text_hr_clean
    dict_text['Speaker'] = text_speaker
    dict_text['Message'] = text_msg_clean
    
    dataframe_name = pd.DataFrame.from_dict(dict_text)
    
    dataframe_name.Hour = dataframe_name.Hour.str.replace("'", '')
    dataframe_name.Message = dataframe_name.Message.str.replace("'", '')
    
    check_dates = dataframe_name[dataframe_name.Data.str.match('../../....')]
    
    if check_dates.all().sum() = 0:
        print("Please use the clean function, there are some data that is not date in your column date")
    else:
        pd.to_datetime(dataframe_name.Date)
        pd.to_datetime(dataframe_name.Hour)
        dataframe_name.head()
        
def clean(dataframe_name, new_dataframe)
    new_dataframe = dataframe_name[dataframe_name.Data.str.match('../../....')]
    pd.to_datetime(new_dataframe.Date)
    pd.to_datetime(new_dataframe.Hour)
    new_datadataframe.head()