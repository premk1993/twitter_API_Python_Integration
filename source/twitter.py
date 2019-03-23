import os
import tweepy
import time
import datetime

from collections import Counter


ACCESS_TOKEN = '156985159-gCmoOXDfcp7YQKQbEgNqlgrNSI0Cs1nxhDJRoP1B'
ACCESS_SECRET = 'Qkdx7wxmJ3uLLLrYQDagkJRVPXTyp4L3dyOkXtXFn5qny'
CONSUMER_KEY = 'd0rN4ESM0dQCIhH6FExP1fmRN'
CONSUMER_SECRET = 'V3SZ4Qf0RtrMtw8Y3LrZGKYAzL48Rkw4EkoPrgSG2tDFk4hOZs'
SEARCH=input("Enter the search string : ")
#FROM=input("Enter the from date (YYYY-MM-DD format) ")
#TO=input("Enter the to data (YYYY-MM-DD format) ")

timestamp=datetime.datetime.now().timestamp()
output_file_dir='./output_files/'+SEARCH+'_'+str(round(timestamp))

try:
	os.makedirs(output_file_dir)
except OSError:  
    print ("Error in Creation of the directory %s for genearting the file failed" % output_file_dir)

#INPUT_FILE_PATH= './output_files/testfhgfkk/'+SEARCH+'.txt'
INPUT_FILE_PATH= output_file_dir+'/'+SEARCH+'.txt'
#print ('Output_dir: '+output_file_dir)
#print (INPUT_FILE_PATH)
num=int(input("Enter the number of tweets you want to retrieve for the search string : "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
i=0

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')

#for res in tweepy.Cursor(api.search, q=SEARCH, lang="en", rpp=5,count=100, result_type="recent", include_entities=True).items(num):
for res in tweepy.Cursor(api.search, q=SEARCH, lang="en", rpp=5).items(num):
 #count=20, result_type="recent", since = FROM,until =TO, include_entities=True, lang="en").items(num):
	
	i+=1
	f.write(res.user.screen_name)
	f.write(' ')
	f.write('[')
	f.write(res.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"))
	f.write(']')	
	f.write(" ")
	f.write(' &" ')
	f.write(res.text.replace('\n',''))
	f.write(' &" ')
	f.write(" ")
	f.write(str(res.user.followers_count))
	f.write(" ")
	f.write(str(res.retweet_count))
	f.write('\n')
f.close

	
if i==0:
	print('No tweets recieved for the search string. Kindly search for another string.')
	exit()

f = open(INPUT_FILE_PATH, 'r', encoding='utf-8')

f=f.read()
#
# print("filedata:"+f)

file_data=f.split('\n')
file_data.pop()



print("Total no. of Tweets retrieved ",i)	

top_n_value = int(input("\nSelect the TOP n values below "+ str(i)+" : "))
n_value_from_user = str(top_n_value)

print("\nChoose one of the below:-")
print("1. The top "+n_value_from_user+" users who have tweeted the most for the entire timeline\n2. The top "+n_value_from_user+" users who have tweeted the most for every hour\n3. The top "+n_value_from_user+" users who have the maximum followers\n4. The top "+n_value_from_user+" tweets which have the maximum retweet count")
ip_selected = int(input("Select: "))


def logicBasedOnSelection(user_selected_value):
    
	global top_n_value
	global file_data
	file_data_instance_list = []
	file_data_instance_list_t = []
	final_file_data_instance_list = []
	final_object = {}
	final_list_with_freq = []
	#print("\n test prem")
	for i in file_data:
		file_data_instance_list.append(i.split('&"'))


	#print(file_data_instance_list)
	#print(file_data)

	if user_selected_value == 1 or user_selected_value == 2:
		ite = 0
		for i in file_data_instance_list:
			file_data_instance_list_t.append(i[0].split(' '))
			final_file_data_instance_list.append(str(file_data_instance_list_t[ite][0]))
			ite += 1
		final_list_with_freq = Counter(final_file_data_instance_list)
	elif user_selected_value == 3 or user_selected_value == 4:
		ite = 0
		for i in file_data_instance_list:
			file_data_instance_list_t.append(i[0].split(' '))
			final_file_data_instance_list.append(i[2].split(' '))
			#print(file_data_instance_list_t)
			#print(final_file_data_instance_list)
			if user_selected_value == 3:
				#print(final_file_data_instance_list[ite][1])
				final_object.update({file_data_instance_list_t[ite][0] : int(final_file_data_instance_list[ite][3])})                       
			else:
				final_object.update({i[1] : int(final_file_data_instance_list[ite][2])})
			ite+=1
		final_list_with_freq = Counter(final_object)
	generate_file(final_list_with_freq, top_n_value, user_selected_value)


def generate_file(final_list, max_val, s_value):

	#print("max_value:"+str(max_val) +"final_list: "+str(len(final_list)))
	if s_value == 1 or s_value == 2 :
		
		if (max_val <= len(final_list) or 1==1):

			
			with open(output_file_dir+'/final_op_file.txt', encoding='utf-8-sig', mode='w') as fp:
				fp.write('Names of Users  |  No. of Tweets\n')  
				counter=0
				for tag, count in final_list.most_common():
				  
				 fp.write('{}  |  {}\n'.format(tag, count))
				 counter+= 1
				 #print(counter)
				 if counter >= max_val:
				  break

			print("The final output file is generated at location: " + output_file_dir+"/final_op_file.txt")	
		# f.close
		else:
			print("The top n value selected is greater than the total final list")
	elif s_value == 3 or s_value == 4:
		if max_val <= len(final_list) or 1==1:
			with open(output_file_dir+'/final_op_file.txt', encoding='utf-8-sig', mode='w') as fp:
				if s_value==4:
					fp.write('Tweets  |  Count\n')  

				else:
					fp.write('Users  |  Followers count\n')  

				counter=0
				for tag, count in final_list.most_common():
				  
				 fp.write('{}  |  {}\n'.format(tag, count))
				 counter+= 1
				 #print(counter)
				 if counter >= max_val:
				  break

			print("The final output file is generated at location: " + output_file_dir+"/final_op_file.txt")	
		else:
			print("The top n value selected is greater than the total final list")

if ip_selected == 1:
    logicBasedOnSelection(1)
elif ip_selected == 2:
    logicBasedOnSelection(2)
elif ip_selected == 3:
    logicBasedOnSelection(3)
elif ip_selected == 4:
    logicBasedOnSelection(4)
else:
  print('Please select values from on the above mentioned.')