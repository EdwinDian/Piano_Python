#######START: Get API users#######
import json
import requests
import csv


api_url_base = 'https://sandbox.tinypass.com'
api_url_users = '/api/v3/publisher/user/list'
api_app_id = 'o1sRRZSLlw'
api_token = 'zziNT81wShznajW2BD5eLA4VCkmNJ88Guye7Sw4D'

def get_users():

	api_url = '{0}{1}?api_token={2}&aid={3}'.format(api_url_base, api_url_users, api_token, api_app_id)

	response = requests.get(api_url)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None
		
		
api_users = get_users()
api_users_list = api_users['users']
#######END: Get API users#######

#######START: Prompt for CSV URL and import as a list of dictionaries#######
csv_url = input("To validate a Client CSV, please enter the path on your local machine: \n") 
print(csv_url)

with open(csv_url, encoding='utf-8-sig') as f:
	csv_users_list = [{k: v for k, v in row.items()}
		for row in csv.DictReader(f, skipinitialspace=True)]
#print("Original CSV: ")
#print(csv_users_list)
#######END: Prompt for CSV URL and import as a list of dictionaries#######

######START: Get email from csv and search it in the DB, returning the ID#######
def lookup_uid(csv_user_email):
	if api_users_list is not None and any(d['email'] == csv_user_email for d in api_users_list):
		api_user = next(item for item in api_users_list if item["email"] == csv_user_email)
		api_user_id = api_user['uid']
		
		for key in api_user.keys():
			if key == 'uid':
				csv_user['user_id'] = api_user_id

		#print("\nNew CSV: ")
		#print(csv_users_list)
		
for csv_user in csv_users_list:
	#print("User: ")
	#print(csv_user)
	csv_user_email = csv_user['email']
	api_user_id = lookup_uid(csv_user_email)
######END: Get email from csv and search it in the DB, returning the ID#######

######START: save updated csv_user_list to CSV######
keys = csv_users_list[0].keys()

with open('data/piano_clientfile_validatedIDs.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csv_users_list)
######END: save updated csv_user_list to CSV######