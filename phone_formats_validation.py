from ContactInfo_validation_class import CheckContact
from bs4 import BeautifulSoup
import requests
import pandas as pd

# We check the mobile formats first. For those that are invalid, we run the area codes check against them. From there
# we coalese the two check outputs together, replacing invalid with valid area code to get the final output.

# To get the area codes for the different regions, we will scrape the web to extract them.
# The url given below has the area codes we need.
url = 'https://www.ofcom.org.uk/phones-telecoms-and-internet/advice-for-consumers/advice/telephone-area-codes-tool'
webpage = requests.get(url).text
soup = BeautifulSoup(webpage, 'html5lib')
table = soup.findAll('table')[0]
table_body = table.find_all('tbody')
areas = [table_body[0].find_all('td')[area].contents[0] for area in range(0, len(table_body[0].find_all('td')))]
codes = [table_body[0].find_all('th')[code].contents[0] for code in range(0, len(table_body[0].find_all('th')))]
areas = [area.strip(' ') for area in areas]

areas = areas[:755 + 1]
codes = codes[:755 + 1]

df = pd.DataFrame(data=[areas, codes])
df = df.transpose()
df.columns = ['Area', 'Code']

# Now that we have the areacodes saved in a dataframe, we can continue to validate phone numbers. I will use a list
# with random made up numbers and validate them. There will be a a couple mobile numbers with valid format and a couple
# with a valid area code.

phone_numbers = ['07719133871', '12432534', '+447712347824', '+232323455666', '2335223', '02012358765', '01132346845']
dummy = [i for i in range(0, len(phone_numbers))]
dummy2 = [i for i in range(0, len(phone_numbers))]
# Put these in a dataframe.
phone_check_df = pd.DataFrame(data=[phone_numbers, dummy, dummy2])
phone_check_df = phone_check_df.transpose()
phone_check_df.columns = ['Phone Numbers', 'Mobile Format Check', 'Area Code Check']

phone_check_df['Mobile Format Check'] = phone_check_df['Phone Numbers'].apply(lambda x:
                                                                              CheckContact(x).uk_mobile_format_check())

# Check the invalid mobile formats against area codes.
phone_check_df['Area Code Check'] = phone_check_df['Phone Numbers'].apply(lambda x:
                                                                          CheckContact(x).uk_area_codes_check(
                                                                              df['Code']))

valid_mobile = pd.DataFrame(columns=phone_check_df.columns)
valid_mobile = valid_mobile.append(phone_check_df[phone_check_df['Mobile Format Check'] == 'Valid Mobile Format'])
valid_mobile['phone_format'] = valid_mobile['Mobile Format Check']

valid_area_code = pd.DataFrame(columns=phone_check_df.columns)
valid_area_code = valid_area_code.append(phone_check_df[phone_check_df['Area Code Check'] == 'Valid Area Code Format'])
valid_area_code['phone_format'] = valid_area_code['Area Code Check']

invalid = pd.DataFrame(columns=phone_check_df.columns)
invalid = invalid.append(phone_check_df[(phone_check_df['Mobile Format Check'] == 'Invalid Mobile Format')
                                        & (phone_check_df['Area Code Check'] == 'Invalid Phone Format')])
invalid['phone_format'] = 'Invalid Phone Format'

valid_mobile = valid_mobile.append(valid_area_code).append(invalid)
final_df = valid_mobile[['Phone Numbers', 'phone_format']]

breakpoint()
