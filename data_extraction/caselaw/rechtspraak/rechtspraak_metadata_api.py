## DO NOT USE THIS FILE. WORK IS NOT YET FINISHED

import requests, json, xmltodict, pandas as pd, re
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

def save_csv(dataframe, file_name):
    # df = pd.DataFrame(columns=['id', 'uitspraak'])
    # ecli_id = []
    # uitspraak = []
    dataframe.to_csv(DIR_RECHTSPRAAK_CSV + "/" + file_name + "_metadata.csv")
    print("Metadata of " + file_name + " saved")

def read_csv():
    path = DIR_RECHTSPRAAK_CSV
    csv_files = glob.glob(path + "/*.csv")
    print("Found " + str(len(csv_files)) + " CSV file(s)")
    return csv_files

def myprint(d, l:list):

    output = ''

    if isinstance(d, str):
        output = output + str(d) + "\n"
        l.append(output)
        output = ""
    elif isinstance(d, dict):
        for v in d.values():
            myprint(v, l)
    elif isinstance(d, list):
        for v in d:
            myprint(v, l)

    # for v in d.values():
    #     if isinstance(v, dict):
    #         myprint(v)
    #     elif isinstance(v, list):
    #         myprint(v)
    #     else:
    #         # return "{0} : {1}".format(k, v)
    #         output = output + str(v) + "\n"
    #         # print("{0} : {1}".format(k, v))
    return l

if __name__ == '__main__':
    print("Reading CSV files...")
    csv_files = read_csv()

    if len(csv_files) > 0:

        items_to_remove = ["'emphasis': ", "{'@role': ", " '#text': '", "{'para': '", "{'para': {", "{'para': [{", "{'para': ['", "','",  "'bold',", "'italic',", 'None', "'}", "']}", "}}", "}, ", "', '", "['", ", '"]

        for f in csv_files:
            df = pd.read_csv(f)

            for k in df.itertuples():
                # Build the URL
                ecli_id = str(k.id)
                url = "https://data.rechtspraak.nl/uitspraken/content?id=" + ecli_id
                print("Rechtspraak metadata API")

                # Check if API is working
                response_code = check_api(url)
                if response_code == 200:
                    print("API is working!")

                    # Get response from the URL and convert it to JSON object
                    json_object = get_data(url)

                    if json_object:
                        # Define the pandas dataframe
                        df = pd.DataFrame(columns=['uitspraak'])

                        ecli_id = []
                        uitspraak_df = []
                        uitspraak = ''

                        for index, val in json_object.items():

                            print(myprint(val, []))


                            if index == 'uitspraak.info':
                                ### THE FOLLOWING IS ONE WAY OF GETTING THE DATA
                                # for i, j in val.items():
                                #     if i == 'bridgehead':
                                #         uitspraak = uitspraak + j['#text']
                                #         uitspraak = uitspraak + "\n"
                                #     if i == 'para':
                                #         for k in range(len(j)):
                                #             if j[k] is not None:
                                #                 uitspraak = uitspraak + j[k]
                                #                 uitspraak = uitspraak + "\n"
                                #     if i == 'parablock':
                                #         for k in range(len(j)):
                                #             if type(j[k]['para']) is list:
                                #                 print(j[k]['para'][0])
                                #             if type(j[k]['para']) is dict:
                                #                 pass

                                ### THIS IS ANOTHER WAY
                                for x in val:
                                    if str(x) == 'bridgehead':
                                        uitspraak = uitspraak + str(val[x])
                                        uitspraak = uitspraak + "\n"
                                    if str(x) == 'para':
                                        for y in val[x]:
                                            if str(y) != 'None':
                                                uitspraak = uitspraak + str(y)
                                                uitspraak = uitspraak + "\n"
                                    if str(x) == 'parablock':
                                        for y in val[x]:
                                            # print(type(y.get('para', {})))
                                            # print(y.get('para', {}))
                                            for z in y:
                                                uitspraak = uitspraak + str(y)
                                                uitspraak = uitspraak + "\n"

                                # print(uitspraak)
                                # for i in items_to_remove:
                                #     uitspraak = uitspraak.replace(i, " ")
                                #
                                # print(uitspraak)
                                # sys.exit()

                            # print(uitspraak)


                            if index == 'section':
                                for i in range(len(val)):
                                    for x, y in val[i].items():
                                        if x == 'title':
                                            uitspraak = uitspraak + y['nr'] + " "
                                            uitspraak = uitspraak + y['#text']
                                            uitspraak = uitspraak + "\n"
                                        if x == 'para':
                                            if y is not None:
                                                for z in y:
                                                    if z is not None:
                                                        uitspraak = uitspraak + str(z)
                                                        uitspraak = uitspraak + "\n"
                                        if x == 'parablock':
                                            if type(y) is dict:
                                                uitspraak = uitspraak + y['para']
                                                uitspraak = uitspraak + "\n"
                                            if type(y) is list:
                                                for z in y:
                                                    if z is not None:
                                                        # print(z['para'])
                                                        for w in z.items():
                                                            for u in range(len(w)):
                                                                # print(w[u])
                                                                if u != 'para':
                                                                    pass
                                                        uitspraak = uitspraak + str(z['para'])
                                                        uitspraak = uitspraak + "\n"
                                                        # print(z['para'])
                                                # print(y)
                                            if type(y) is not dict or type(y) is not list:
                                                uitspraak = uitspraak + str(z)
                                                uitspraak = uitspraak + "\n"
                                        if x == 'paragroup':
                                            if type(y) is list:
                                                for z in y:
                                                    if z is not None:
                                                        # uitspraak = uitspraak + str(z['nr']) + " "
                                                        for w in z.items():
                                                            for u in range(len(w)):
                                                                if w[u] == 'nr':
                                                                    uitspraak = uitspraak + str(w[u+1])
                                                                if w[u] == 'para':
                                                                    uitspraak = uitspraak + str(w[u + 1])
                                                                if w[u] == 'parablock':
                                                                    for t in w[u + 1]:
                                                                        pass
                                                                        # print(type(t))
                                                                    # print(w[u + 1])
                                                                # print(w[u])
                                                                # print(u)
                                            if type(y) is dict:
                                                pass
                                # sys.exit()
                                #
                                # print(uitspraak)
                                # sys.exit()
                                for x in val:
                                    # print(type(val))
                                    # print(type(x))
                                    uitspraak = uitspraak + str(x['title'].get('nr')) + " "
                                    # uitspraak = uitspraak + str(x['title']['nr']) + " "
                                    uitspraak = uitspraak + str(x['title'].get('#text'))
                                    # uitspraak = uitspraak + str(x['title']['#text'])
                                    uitspraak = uitspraak + "\n"
                                    # print(uitspraak)
                                    # sys.exit()


                                    if 'parablock' in x:
                                        for y in x['parablock']:
                                            if y is not None:
                                                if type(y) is dict:
                                                    uitspraak = uitspraak + str(y.get('para', {}))
                                                if type(y) is not dict:
                                                    uitspraak = uitspraak + str(y)
                                                if type(y) is str:
                                                    uitspraak = uitspraak + str(y)
                                                uitspraak = uitspraak + "\n\n"

                                    if 'paragroup' in x:
                                        for y in x['paragroup']:
                                            if y is not None:
                                                if type(y) is dict:
                                                    # print(y['nr'])
                                                    # print(y.get('para', {}))
                                                    # print(y.get('parablock', {}))

                                                    # for z in y['para']:
                                                    #     if z is not None:
                                                    #         print(type(z))
                                                    #         print(z.get('#text'))
                                                    #     # print(z['emphasis']['#text'])
                                                    #     print(y)
                                                    uitspraak = uitspraak + str(y['nr']) + " "
                                                    uitspraak = uitspraak + str(y['para'])
                                                    uitspraak = uitspraak + "\n"
                                                    uitspraak = uitspraak + str(y['parablock'])
                                                if type(y) is not dict:
                                                    uitspraak = uitspraak + str(y)
                                                if type(y) is str:
                                                    uitspraak = uitspraak + str(y)
                                                uitspraak = uitspraak + "\n\n"

                            uitspraak_df.append(uitspraak)
                            uitspraak = ''
                        # sys.exit()
                        df['uitspraak'] = uitspraak_df
                        # print(uitspraak_df)
                        # save_csv(df, f.split('/')[-1][:len(f.split('/')[-1]) - 4])
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
                        # print(df.shape)
                    else:
                        print("No metadata found!")
                    break
                else:
                    print(f"API returned with a {response_code} error code!")
                break
            break
    else:
        print("No CSV files found!")
        sys.exit()