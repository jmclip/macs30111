'''
Team Tutorial #3: Dictionaries
MACS 30111
'''

import json

CFPB_16 = json.load(open("cfpb16_1000.json"))

# Task 1
def find_companies(complaints):
    '''
    Compute a list of companies complained about

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (list or set) of companies
    '''

    # Your code goes here
    # replace [] with a suitable return value
    return []


# Task 2
def count_complaints_about(complaints, company_name):
    '''
    Count complaints about a specified company

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary
        company_name (str): The company name to count complaints for

    Returns: count of complaints (int)
    '''

    # Your code goes here
    # replace 0 with a suitable return value
    return 0


# Task 3
def count_by_state(complaints):
    '''
    Compute counts by state of all complaints

    Inputs:
         complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) that relates states to complaint number
    '''

    # Your code goes here
    # replace {} with a suitable return value
    return {}


# Task 4
def state_with_most_complaints(cnt_by_state):
    '''
    Find the state with the most complaints. Can break ties arbitrarily.

    Inputs:
        cnt_by_state (dict) A dictionary relating each state to the
            count of complaints in that state

    Returns: (str) the state with the most complaints
    '''

    # Your code goes here
    # replace "" with a suitable return value
    return ""


# Task 5
def count_by_company_by_state(complaints):
    '''
    Computes a dict of {company: {state: count, state: count}} for all states
        and companies

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) with count per company per state
    '''

    # Your code goes here
    # replace {} with a suitable return value
    return {}


# Task 6
def complaints_by_company(complaints):
    '''
    Create a dictionary that maps the name of a company to a list of the
    complaint dictionaries that concern that company.

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) mapping the name of the company to a list of complaints
    '''

    # Your code goes here
    # replace {} with a suitable return value
    return {}


# Task 7
def count_by_company_by_state_2(complaints):
    '''
    Computes a dict of {company: {state: count, state: count}} for all states
        and companies

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) with count per company per state

    This implementation involves composing complaints_by_company with 
        count_by_state
    '''

    # Your code goes here
    # replace {} with a suitable return value
    return {}


# Task 8
'''
With your team, compare the implementations of count_by_company_by_state
(Task 5) and count_by_company_by_state_2 (Task 7), and discuss the
advantages and disadvantages of each. Some aspects to consider:
    - Which is easier to read and understand?
    - Which uses less code?
    - Which is easier to debug?
    - Which is faster? As a proxy for speed, you can ask: which requires
      fewer passes through the data?
    - Which implementation would you choose?

Below is the Task 5 version from the slides. Run it on CFPB_16 and compare
its answer to your Task 7. Do they match? If not, why not?
'''

def count_by_company_by_state_slides(complaints):
    '''
    The Task 5 version from the slides (copied as-is)

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) with count per company per state
    '''

    by_company_by_state = {}
    for complaint in complaints:
        company = complaint["Company"]
        state = complaint["State"]
        if company not in by_company_by_state:
            by_company_by_state[company] = {}
        if state not in by_company_by_state[company]:
            by_company_by_state[company][state] = 0
            by_company_by_state[company][state] += 1
    return by_company_by_state
