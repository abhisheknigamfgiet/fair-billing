# fair-billing
    Code to read the log file which consist of users session start and end details with timestamp
    The sample input log file is present in repo
    Sole purpose of the source code to find the unique users and count number of sessions and their time suration of the sessions

# Clone the repository using the command
    git clone https://github.com/abhisheknigamfgiet/fair-billing.git

# To run the script run command:
    python file_path/UserSessions.py log_file_path/log_file.txt
        
        where file_path is the python script path which is the source code
        log_file_path is the path of the log file

# Code Approach/Logic
    1. Function - get_sys_arguments()
        1.1 Reading the valid number of arguments required to run the script 
        1.2 If found correct than returning the log file path argument passed to the command line

    2. Function - read_file()
        2.1 Function takes filepath as argument and try to read the log file from the given path
        2.2 Applied the exception handling to read the log file, if the file is not found or there is some problem with the file the exception will be raised
        2.3 Otherwise the log file will be read from the specified path each line will be stored as an element in the python list using the list comprehension also striping the new line character from each line while reading the log file

    3. Function - get_user_sessions_details()
        3.1 Actual logic for getting the user's session details with time duration
        3.2 Function takes list as argument which contains user's session details as an elements
        3.3 `Creating the basic dictionary to store the log file start time and end time details which will be used to calculate the sessions details for those session which doesn't have corresponding session details, such as the persistent session which doesn't have START details, similarly for those session which doesn't have END details, applied exceptions to those sessions which doesn't have correct timestamp such as in 24-hr format values can't be greater for hours > 24 hours, minutes > 60 minutes and seconds > 60 seconds`
        3.4 Than reading the each element corresponds to the session details of the users
        3.5 `Than checking the session details are valid corresponding to all the conditions, basic condition it should has 3 entries: timestamp, username, START/END, than last value should be either START or END, than checking for valid username using regular expression, if any of the conditions fails we skip that details using continue keyword`
        3.6 `If all the conditions is passed than we are have entry dictionary which will be update with user session and session duration details, User sessions count and setting start as 1 for first entry or logging setting the timestamp to start_time as list so that when we encounter END than we can pop the first entry to calculate the time period, Also setting time to 0 by calculating the difference using dateime for that purpose so substracting with same values
        If the user entry is already present than incrementing the start+1 to get sessions count, Append the start time of the session to start_time list`
        3.7 `Checking the entry of user of END if no START is found for every END there should be corresponding START, start_time is set to empty list as its a END entry, Than calculating the time period using END timestamp - very first entry in the log file
        Applied the logic which will be run untill there is START and corresponing END is there to get the session duration and the start_time as list will be used as FIFO to calculate the duration so we poping from the start_time from index 0
        Than if the corresponding start is not there for END than we are calcuting the session duration for the very first entry in the log file`
        3.8 `Finally we have last condition where START doesn't have corresponding END session details, and start_time list has elements than we are calculating the session duration from the very last entry in the log file`
        3.9 We get the output after handling all the above scenarios and printing the session duration

