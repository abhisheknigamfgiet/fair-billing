import sys
from datetime import datetime
import re

def get_sys_arguments():
    # Check if arguments are provided
    if len(sys.argv) == 2:
        return sys.argv[1] 
    else:
        print("Please provide correct numbers of command-line arguments")
        sys.exit(1)

def read_file(file_path):
    # check and read file if exists
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read all lines from the file and store them in a list, removing newline characters
            return [line.rstrip('\n') for line in file.readlines()]
    except FileNotFoundError:
        print("File not found!")
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

def get_user_sessions_details(users_logs):
    # functions to return user sessions and log time
    start_end_time_dict = {}
    for user_log in users_logs: # storing the start time and end time if corresponding start and end details are not present
        if start_end_time_dict.get('start_time') is None:
            try:
                start_end_time_dict['start_time'] = datetime.strptime(user_log.split(' ')[0], "%H:%M:%S")
            except ValueError:
                continue
        try:
            start_end_time_dict['end_time'] = datetime.strptime(user_log.split(' ')[0], "%H:%M:%S")
        except ValueError:
            continue
        
    cnt_usr_sessions = {}
    for user_log in users_logs:
        # pdb.set_trace()
        # block to check the timestamp is a valid timestamp in 24 hr format
        try:
            time_chk = datetime.strptime(user_log.split(' ')[0], "%H:%M:%S")
            if 0 <= time_chk.hour < 24 and 0 <= time_chk.minute < 60 and 0 <= time_chk.second < 60:
                pass
            else:
                continue
        except ValueError:
            continue
        if len(user_log.split(' ')) != 3 or \
            user_log.split(' ')[2] not in ['Start', 'End'] or \
                re.search(r'[^a-zA-Z0-9_]', user_log.split(' ')[1]):    # block to check log file has valid entries
                continue
        else:   # block to get the user log details
            if user_log.split(' ')[2] == 'Start':   # checking the entry of user end or start
                if cnt_usr_sessions.get(user_log.split(' ')[1]) is None:    # inserting the first entry for user
                    '''User sessions count and setting start as 1 for first entry or logging
                    setting the timestamp to start_time as list so that when we encounter END than we can pop the first entry
                    to calculate the time period
                    Also setting time to 0 by calculating the difference using dateime for that purpose so substracting with same values'''
                    cnt_usr_sessions[user_log.split(' ')[1]] = {'start': 1, 'end': 0, \
                        'start_time': [datetime.strptime(user_log.split(' ')[0], "%H:%M:%S")], \
                            # 'end_time': [], \
                                'time':datetime.strptime(user_log.split(' ')[0], "%H:%M:%S") - datetime.strptime(user_log.split(' ')[0], "%H:%M:%S")}
                else:
                    '''If the user entry is already present than incrementing the start+1 to get sessions count
                    Append the start time of the session to start_time list'''
                    cnt_usr_sessions[user_log.split(' ')[1]]['start'] += 1
                    cnt_usr_sessions[user_log.split(' ')[1]]['start_time'].append(datetime.strptime(user_log.split(' ')[0], "%H:%M:%S"))
            else:
                '''Checking the entry of user of END if no START is found for every END there should be corresponding START'''
                if cnt_usr_sessions.get(user_log.split(' ')[1]) is None:
                    '''start_time is set to empty list as its a END entry
                    Than calculating the time period using END timestamp - very first entry in the log file'''
                    cnt_usr_sessions[user_log.split(' ')[1]] = {'start': 1, 'end': 1, \
                        'start_time': [], \
                            'time':datetime.strptime(user_log.split(' ')[0], "%H:%M:%S") - start_end_time_dict.get('start_time')}
                else:
                    cnt_usr_sessions[user_log.split(' ')[1]]['end'] += 1
                    # Below block will be run untill there is START and corresponing END is there to get the session
                    # And the START and END will work like a FIFO so we poping from the start_time from index 0
                    if len(cnt_usr_sessions[user_log.split(' ')[1]]['start_time']) > 0:
                        cnt_usr_sessions[user_log.split(' ')[1]]['time'] += datetime.strptime(user_log.split(' ')[0], "%H:%M:%S") - \
                            cnt_usr_sessions[user_log.split(' ')[1]]['start_time'].pop(0)
                    else:
                        cnt_usr_sessions[user_log.split(' ')[1]]['time'] += datetime.strptime(user_log.split(' ')[0], "%H:%M:%S") - \
                            start_end_time_dict.get('start_time')

    print()
    for key, value in cnt_usr_sessions.items():
        if len(value['start_time']) > 0:
            for v in value['start_time']:
                value['time'] += start_end_time_dict.get('end_time') - v
        print(f"{key} {value['start'] if value['start'] >= value['end'] else value['end']} {value['time'].seconds}")

def main():
    file_path = get_sys_arguments()
    logs = read_file(file_path)
    get_user_sessions_details(logs)
    print()


if __name__ == "__main__":
    main()