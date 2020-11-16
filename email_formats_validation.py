from ContactInfo_validation_class import CheckContact
import pandas as pd
import re

email_list = ['sk432@gmail.com', 'ss.kr@hotmail.co.uk', '134fds@gmail.com',
              'lsjfdasljf@2rwe.csd...casd', 'no_one@here.org', 'sfsasdf@',
              's.s.s.m.@gmail.com', 'Sam Clint <sam_clint@gmail.com>']

df = pd.DataFrame(data=email_list, columns=['email'])
df['email_format_validation'] = df['email'].apply(lambda x: CheckContact(x).email_validation())
print(df)


