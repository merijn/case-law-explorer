## DO NOT USE THIS FILE. WORK IS NOT YET FINISHED

import requests, json, xmltodict, pandas as pd, argparse
from datetime import date, datetime
import glob

from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
from definitions.storage_handler import DIR_RECHTSPRAAK_CSV

# Check whether the API is working
def check_api(url):
    response = requests.get(f"{url}")

    # Return with the response code
    return response.status_code

def get_data(url):
    res = requests.get(url)
    res.raw.decode_content = True

    xpars = xmltodict.parse(res.text)
    json_string = json.dumps(xpars)
    json_object = json.loads(json_string)
    json_object = json_object['open-rechtspraak']['uitspraak']

    return json_object

def save_csv(json_object, file_name):
    df = pd.DataFrame(columns=['id', 'uitspraak'])
    ecli_id = []
    uitspraak = []
    pass

def read_csv():
    path = DIR_RECHTSPRAAK_CSV
    csv_files = glob.glob(path + "/*.csv")
    return csv_files

if __name__ == '__main__':
    print("Reading CSV files...")
    csv_files = read_csv()

    for f in csv_files:
        df = pd.read_csv(f)
        print(df)

        for l in df.iterrows():
            
            print(l)
            break
        # break




        for k in df.itertuples():
            # Define the URL
            url = str(k.link)
            print("Rechtspraak metadata API")

            # Check if API is working
            response_code = check_api(url)
            if response_code == 200:
                print("API is working fine!")

                # Get response from the URL and convert it to JSON object
                json_object = get_data(url)

                if json_object:
                    # Define the pandas dataframe
                    df = pd.DataFrame(columns=['uitspraak'])
                    # ecli_id = []
                    uitspraak_df = []
                    uitspraak = ''

                    for index, val in json_object.items():
                        # if i == 'uitspraak.info':

                        if index == 'section':
                            for x in val:
                                uitspraak = uitspraak + str(x['title']['#text'])
                                uitspraak = uitspraak + "\n"

                                if 'parablock' in x:
                                    for y in x['parablock']:
                                        # print(type(y))
                                        if type(y) is dict:
                                            uitspraak = uitspraak + str(y['para'])
                                        if type(y) is not dict:
                                            uitspraak = uitspraak + str(y)
                                        uitspraak = uitspraak + "\n\n"
                                # if x['parablock'] in val:
                                #     print(x['parablock'])
                                #     for y in x['parablock']:
                                        # uitspraak.append(y['para'])
                                        # print(y['para'])
                                # if x['paragroup'] in val:
                                #     print(val)

                        uitspraak_df.append(uitspraak)
                        uitspraak = ''

                    df['uitspraak'] = uitspraak_df
                    # print(df.head())


                    # Get current time
                    # now = datetime.now()
                    # current_time = now.strftime("%H:%M:%S")
                    #
                    # # Create file name
                    # file_name = 'Rechtspraak_metadata_' + current_time
                    #
                    # if (save_csv(json_object, file_name)):
                    #     print("Metadata saved to CSV file successfully!")
                    # else:
                    #     print("Error saving metadata to CSV file!")
                else:
                    print("No metadata found!")
                break
            else:
                print(f"API returned with a {response_code} error code")
            break
        break