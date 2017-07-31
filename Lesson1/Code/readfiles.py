import unicodecsv
from datetime import datetime 
from collections import defaultdict
import numpy as np

def read_files(file_name):
    f = open(file_name, 'rb')
    reader = unicodecsv.DictReader(f)
    enrollments = list(reader)
    f.close()
    return enrollments

def parse_int(i):
    if i == '':
        return None
    else:
        return int(i)
def parse_date(date):
    if date == '':
        return None
    else:
        return datetime.strptime(date,'%Y-%m-%d')

def get_account_key(enrollment):
    return enrollment['account_key']

def get_acct(engagement):
    return engagement['acct']

def set_for_list(collection, key):
    uniques = set()
    for item in collection:
        uniques.add(item[key])
    return uniques


def remove_accounts(data, accounts):
    non_udacity = []
    for item in data:
        if item['account_key'] not in accounts:
            non_udacity.append(item)
    return non_udacity

def is_within_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0
def total_minutes_for_engagements(engagements):
    minutes = 0
    for eng in engagements:
        minutes += eng['total_minutes_visited']
    return minutes
def total_lessons_for_engagements(engagements):
    lessons = 0
    for eng in engagements:
        lessons += eng['lessons_completed']
    return lessons
def days_visited_a_course(engagements):
    number = 0
    for eng in engagements:
        if eng['num_courses_visited'] > 0:
            number += 1
    return number

def students_who_pass_projects(submissions, projects, filter_students):
    students = set()
    for sub in submissions:
        acc_key = sub['account_key']
        if sub['lesson_key'] in projects and (sub['assigned_rating'] == 'PASSED' or sub['assigned_rating'] == 'DISTINCTION' ) and acc_key in filter_students:
            students.add(acc_key)
    return students

enrollments_filename = '../enrollments.csv'
engagement_filename = '../daily_engagement.csv'
submissions_filename = '../project_submissions.csv'

enrollments = read_files(enrollments_filename)
daily_engagement = read_files(engagement_filename)
project_submissions = read_files(submissions_filename)



for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'    
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

for engagement_record in daily_engagement:
    engagement_record['account_key'] =  engagement_record['acct']
    del engagement_record['acct']



# Removing test acounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])

print udacity_test_accounts

non_udacity_enrollments = remove_accounts(enrollments, udacity_test_accounts)
non_udacity_daily_engagement = remove_accounts(daily_engagement, udacity_test_accounts)
non_udacity_project_submissions = remove_accounts(project_submissions, udacity_test_accounts)

paid_students = {}
for enroll in non_udacity_enrollments:
    if not enroll['is_canceled'] or enroll['days_to_cancel'] > 7:
        account_key = enroll['account_key']
        enrollment_date = enroll['join_date']
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date


subway_project_lessson_keys = ['746169184', '3176718735']

passing_students = students_who_pass_projects(non_udacity_project_submissions, subway_project_lessson_keys, paid_students)
# passing_engagements = engagements_for_students(non_udacity_daily_engagement, passing_students)

# non_passing_students = students_who_not_pass_projects(non_udacity_project_submissions, subway_project_lessson_keys, paid_students)
# non_passing_engagements = engagements_for_students(non_udacity_daily_engagement, non_passing_students)

# print 'Students Passing = ', len(passing_students)
# print 'Students Non Passing = ', len(non_passing_students) 

# print 'Passing = ', len(passing_engagements)
# print 'Non Passing = ', len(non_passing_engagements)

first_week_engagement = []
for engagement in non_udacity_daily_engagement:
    student_account_key = engagement['account_key']
    if student_account_key in paid_students \
     and is_within_week(paid_students[student_account_key], engagement['utc_date']):
        first_week_engagement.append(engagement)

print 'first_week_engagement = ',  len(first_week_engagement)


engagements_by_account = defaultdict(list)
for engagement in first_week_engagement:
    account_key = engagement['account_key']
    engagements_by_account[account_key].append(engagement)

# total_minutes_by_account = {}

# for account_key, engagements_student in engagements_by_account.items():
#     total_minutes_by_account[account_key] = total_minutes_for_engagements(engagements_student)

# total_lessons = {}
# total_minutes = total_minutes_by_account.values()
total_lessons_by_account = {}
total_lessons_pass = {}
total_lessons_not_pass = {}
for account_key, engagements_student in engagements_by_account.items():
    total = total_lessons_for_engagements(engagements_student)
    total_lessons_by_account[account_key] = total
    if account_key in passing_students:
        total_lessons_pass[account_key] = total
    else:
        total_lessons_not_pass[account_key] = total

# total_courses_visited = {}
# for account_key, engagements_student in engagements_by_account.items():
#     total_courses_visited[account_key] = days_visited_a_course(engagements_student)


def print_analisys(data):
    print 'Mean = ', np.mean(data)

# print print_analisys(total_courses_visited.values())
# print_analisys(total_minutes)
# print '============='
print_analisys(total_lessons_by_account.values())
print_analisys(total_lessons_pass.values())
print_analisys(total_lessons_not_pass.values())

# print 'paid_students count', len(paid_students) 
# print enrollments
# print daily_engagement
# enroll_accounts = set_for_list(enrollments, 'account_key')
# enrollment_num_rows = len(enrollments)
# enrollment_num_unique_students = len(enroll_accounts)  

# engagement_accounts = set_for_list(daily_engagement, 'account_key')
# engagement_num_rows = len(daily_engagement)            
# engagement_num_unique_students = len(engagement_accounts)  

# submissions_accounts = set_for_list(project_submissions, 'account_key')
# submission_num_rows = len(project_submissions)
# submission_num_unique_students = len(submissions_accounts)



# print 'enrollment_num_rows = ', enrollment_num_rows
# print 'enrollment_num_unique_students = ', enrollment_num_unique_students

# print 'engagement_num_rows = ', engagement_num_rows
# print 'engagement_num_unique_students = ', engagement_num_unique_students

# print 'submission_num_rows = ', submission_num_rows
# print 'submission_num_unique_students = ', submission_num_unique_students

# print 'daily_engagement[0][\'account_key\'] = ', daily_engagement[0]['account_key']


