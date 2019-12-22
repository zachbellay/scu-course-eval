import re
import os
import linecache
from tqdm import tqdm
import sys
import itertools
import csv

subjects = ['ACTG', 'AERO', 'AMTH', 'ANTH', 'ARAB', 'ARTH', 'ARTS', 'ASCI', 'BIOE', 'BIOL', 'BS', 'BSHS', 'BSPT', 'BSST', 'BUSN', 'CATE', 'CE', 'CEFT', 'CEHS', 'CENG', 'CEPS', 'CERS', 'CEST', 'CHEM', 'CHIN', 'CHST', 'CLAS', 'COEN', 'COMM', 'CPSY', 'CSCI', 'DANC', 'DM', 'DMPS', 'DMRS', 'DMSP', 'DR', 'ECON', 'ED', 'EDUC', 'ELEN', 'ELSJ', 'EMBA', 'EMGT', 'ENGL', 'ENGR', 'ENVS', 'ETHN', 'FE', 'FERS', 'FNCE', 'FREN', 'FT', 'FTCE', 'FTLS', 'FTRS', 'FTST', 'GERM', 'GTUC', 'HIST', 'HM', 'HMLS', 'HNRS', 'HR', 'HRBS', 'HRCE', 'HRFT', 'HRHS', 'HRIR', 'HRPH', 'HRPS', 'HRRA', 'HRRS', 'HRSP', 'HRST', 'HS', 'HSFT', 'HSHR', 'HSRA', 'HSRS', 'HSSP', 'HSST', 'IDIS', 'IDS', 'INTL', 'ITAL', 'JAPN', 'LANG', 'LAW', 'LEAD', 'LS', 'LSFT', 'LSHM', 'LSHS', 'LSRA', 'LSST', 'MA', 'MATH', 'MDV', 'MECH', 'MGMT', 'MILS', 'MKTG', 'MLS', 'MSIS', 'MTS', 'MUSC', 'NEUR', 'NOV', 'NT', 'NTBS', 'NTHM', 'OMIS', 'OT', 'OTRS', 'OTSP', 'PH', 'PHCE', 'PHHS', 'PHIL', 'PHRA', 'PHSC', 'PHST', 'PHYS', 'PLIT', 'PMIN', 'POLI', 'PS', 'PSRS', 'PSYC', 'PTBS', 'RA', 'RAFT', 'RAHR', 'RAHS', 'RALS', 'RAST', 'RELS', 'RJUS', 'RS', 'RSCE', 'RSED', 'RSFT', 'RSHR', 'RSOC', 'RSRA', 'RSSP', 'RSST', 'SCTR', 'SOCI', 'SP', 'SPAN', 'SPBS', 'SPFT', 'SPIR', 'SPLS', 'SPNT', 'SPPS', 'SPRA', 'SPRS', 'SPST', 'SRC', 'ST', 'STCE', 'STD', 'STED', 'STHR', 'STHS', 'STL', 'STLS', 'STPH', 'STPS', 'STRS', 'STSP', 'TESP', 'THTR', 'UCB', 'UGST', 'UNIV', 'WGST']


def parse():
    rel_txt_dir = '../txts'
    cd = os.getcwd()
    txt_dir = os.path.abspath(os.path.join(cd, rel_txt_dir))

    if(os.path.exists('course_evals.csv')):
        os.remove('course_evals.csv')
    

    with open('course_evals.csv', mode='w') as eval_file:

        field_names = ['year', 'quarter', 'course_id', 'instructor_name', 'subject', 'subject_number', 'response_rate', 'num_enrolled', 'num_responses', 'class_name', 'overall_avg', 'overall_std_dev', 'difficulty_avg', 'difficulty_med', 'difficulty_std_dev', 'zero_one', 'two_three', 'four_five', 'six_seven', 'eight_ten', 'eleven_fourteen', 'fifteen_plus']
        eval_writer = csv.DictWriter(eval_file, fieldnames=field_names)
        eval_writer.writeheader()

        # Iterate over all txt files
        for subdir, dirs, files in os.walk(txt_dir):
            
            # Iterate over every txt file
            for file in files:

                # # Ignore non-txt files
                if(".txt" not in file):
                    continue

                quarter, year = subdir.split('/')[-1].split('_')

                # Ignore everything before this year
                if(int(year) < 2015):
                    continue

                abs_txt_path = os.path.join(txt_dir, subdir, file)

                _file = parse_file(abs_txt_path, quarter, year)

                if(_file is not None):
                    eval_writer.writerow(_file)
                else:
                    print(quarter, year, file)

def parse_file(file, quarter, year):

    # Check that the file doesn't have no data (because a lack of responses)
    if(eval_valid(file)):
        eval_info = {}

        eval_info['year'] = year

        eval_info['quarter'] = quarter

        eval_info['course_id'] = int(file.split('/')[-1].replace('.txt', ''))
        
        eval_info['instructor_name'] = get_instructor_name(file)

        subject, subject_number = get_subject(file)
        
        eval_info['subject'] = subject
        eval_info['subject_number'] = subject_number

        eval_info['response_rate'] = get_response_rate(file)

        eval_info['num_enrolled'] = get_num_enrolled(file)

        eval_info['num_responses'] = get_num_responses(file)

        eval_info['class_name'] = get_class_name(file)
        
        overall_avg, overall_std_dev = get_overall_score(file)
        
        eval_info['overall_avg'] = overall_avg
        eval_info['overall_std_dev'] = overall_std_dev

        difficulty_avg, difficulty_med, difficulty_std_dev = get_difficulty(file)

        eval_info['difficulty_avg'] = difficulty_avg
        eval_info['difficulty_med'] = difficulty_med
        eval_info['difficulty_std_dev'] = difficulty_std_dev
       
        zero_one, two_three, four_five, six_seven, eight_ten, eleven_fourteen, fifteen_plus = get_time_spent(file)

        eval_info['zero_one'] = zero_one
        eval_info['two_three'] = two_three
        eval_info['four_five'] = four_five
        eval_info['six_seven'] = six_seven
        eval_info['eight_ten'] = eight_ten
        eval_info['eleven_fourteen'] = eleven_fourteen
        eval_info['fifteen_plus'] = fifteen_plus

        return eval_info
    
def get_instructor_name(file):
    _id_string = 'No. of students enrolled'
    
    # Get the third line by default
    instructor_name = linecache.getline(file, 3).replace('\n','')

    # If the id_string or left paren is in the name, then get the first line
    if(_id_string in instructor_name or '(' in instructor_name):
        instructor_name = linecache.getline(file, 1).replace('\n','')
    
    # If there is a comma, get the first part of the split string
    if(',' in instructor_name):
        instructor_name = instructor_name.split(',')[0]

    return instructor_name

def get_subject(file):
    pattern = r'\b[A-Z]{4}[0-9][0-9A-Z]*'

    # Get first 5 lines of file
    with open(file) as f:
        header = [next(f) for i in range(5)]
    header = ''.join(header)

    subjects = re.findall(pattern, header)
    
    if(len(subjects) is not 1):
        raise Exception(f"More than one subject candidate found {subjects}")

    subject = "".join(itertools.takewhile(str.isalpha, subjects[0]))
    number = subjects[0][len(subject):]

    return subject, number

def get_response_rate(file):
    pattern = r'Rate = (.*?) %'

    with open(file) as f:
        header = [next(f) for i in range(10)]
    header = ''.join(header)

    response_rate = re.findall(pattern, header)[0]

    return float(response_rate)

def get_num_enrolled(file):
    pattern = r'enrolled = (.*?) No.'

    with open(file) as f:
        header = [next(f) for i in range(10)]
    header = ''.join(header)

    num_enrolled = re.findall(pattern, header)[0]

    return int(num_enrolled)
    
def get_num_responses(file):
    pattern = r'No. of responses = (.*?)\s'

    with open(file) as f:
        header = [next(f) for i in range(10)]
    header = ''.join(header)

    num_responses = re.findall(pattern, header)[0]
    
    return int(num_responses)

def get_class_name(file):
    pattern = r'\n(.*?)\('

    with open(file) as f:
        header = [next(f) for i in range(10)]
    header = ''.join(header)

    class_name = re.findall(pattern, header)[0]
    
    return class_name

def get_overall_score(file):
    pattern = r'\nav.=(.*?) dev.=(.*?)\s'
    pattern2 = r'-\s*av.=(.*?)\s*most clearly describes your experience with 5 being\s*dev.=(.*?)\s*'

    f = open(file, 'r')
    _survey = f.readlines()
    _survey = ''.join(_survey)


    if(len(re.findall(pattern, _survey)) > 0):
        overall_avg, overall_std_dev = re.findall(pattern, _survey)[0]
    elif(len(re.findall(pattern2, _survey)) > 0):
        overall_avg, overall_std_dev = re.findall(pattern2, _survey)[0]
    else:
        raise Exception("Could not find overall score for   ")

    return overall_avg, overall_std_dev
    
    
    
def eval_valid(file):
    
    f = open(file, 'r')
    _survey = f.readlines()
    _survey = ''.join(_survey)

    if('The evaluation will not be displayed due to low response rate.' in _survey):
        return False
    else:
        return True

def get_difficulty(file):

    f = open(file, 'r')
    _survey = f.readlines()
    _survey = ''.join(_survey)

    if('This course was conceptually challenging compared to most courses I have taken at SCU' in _survey):
        
        instructor_name = get_instructor_name(file)
        class_name = get_class_name(file)

        pattern = r'Much more\s*n=[0-9]*\s*av.=(.*?)\s*md=(.*?)\s*dev.=(.*?)\s'
        pattern2 = r'Much more\s*' + instructor_name + r', ' + class_name +\
                   r'\s*n=[0-9]*\s*av.=(.*?)\s*md=(.*?)\s*dev.=(.*?)\s'

        if(len(re.findall(pattern, _survey)) > 0):
            difficulty_avg, difficulty_med, difficulty_std_dev = re.findall(pattern, _survey)[0]
        elif(len(re.findall(pattern2, _survey)) > 0):
            difficulty_avg, difficulty_med, difficulty_std_dev = re.findall(pattern2, _survey)[0]
        else:
            raise Exception("Could not get difficulties")

        return difficulty_avg, difficulty_med, difficulty_std_dev

    else:
        return None, None, None


def get_time_spent(file):
    f = open(file, 'r')
    _survey = f.readlines()
    _survey = ''.join(_survey)

    pattern = r'2.1\) In an average week, the approximate number of hours I spent doing work for this course outside regularly scheduled class/lab time was:' \
              + r'\s*0-1\s*(.*?)%\s*n=[0-9]*\s*2-3\s*(.*?)%\s*4-5\s*(.*?)%\s*6-7\s*(.*?)%\s*8-10\s*(.*?)%\s*11-14\s*(.*?)%\s*15\+\s*(.*?)%\s*2.2'
    
    
    if(len(re.findall(pattern, _survey)) > 0):
        zero_one, two_three, four_five, six_seven, eight_ten, eleven_fourteen, fifteen_plus = re.findall(pattern, _survey)[0]
        return zero_one, two_three, four_five, six_seven, eight_ten, eleven_fourteen, fifteen_plus
    else:
        raise Exception("Could not get time spent")
# 2.1) In an average week, the approximate number of hours I spent doing work for this course outside regularly scheduled class/lab time was:

# 0-1

# 0%

# n=12

# 2-3

# 0%

# 4-5

# 25%

# 6-7

# 33.3%

# 8-10

# 33.3%

# 11-14

# 8.3%

# 15+

# 0%

# 2.2) This course was conceptually challenging compared to most courses I have taken at SCU:



if __name__ == '__main__':
    parse()