#!/usr/bin/env python3

import re
import csv
import operator

def get_error():
	error_count = {}
	regex = r'ticky: ERROR ([\w\' ]+)'
	with open('syslog.log') as f:
		for line in f:
			error = re.search(regex, line)
			if error is None:
				continue
			error = error.group(1).strip()
			if error_count.get(error):
				error_count[error] += 1
			else:
				error_count[error] = 1
	return sorted(error_count.items(), key=operator.itemgetter(1), reverse=True)

def get_user_error_and_info():
	regex = r'\(.*\)'
	dict_user = {}
	with open('syslog.log') as f:
		for line in f:
			user = re.search(regex, line).group(0)
			user = user[1:-1]
			if "ERROR" in line:
				if dict_user.get(user):
					dict_user[user][1] += 1
				else:
					dict_user[user] = [0, 1]
			if "INFO" in line:
        	                if dict_user.get(user):
                	                dict_user[user][0] += 1
                        	else:
                                	dict_user[user] = [1, 0]

	return sorted(dict_user.items())

def write_to_csv(err_count, users):
	with open('error_message.csv', 'w', newline='') as f:
		field = ["Error", "Count"]
		writer = csv.DictWriter(f, fieldnames=field)
		writer.writeheader()
		for key, value in err_count:
			writer.writerow({"Error": key, "Count": value})
	with open('user_statistics.csv', 'w', newline='') as f:
		field = ["Username", "INFO", "ERROR"]
		writer = csv.DictWriter(f, fieldnames=field)
		writer.writeheader()
		for key, value in users:
			writer.writerow({'Username': key, 'INFO': value[0], 'ERROR': value[1]})

 
print(get_error())
users = get_user_error_and_info()
print(users)
write_to_csv(get_error(), users)

