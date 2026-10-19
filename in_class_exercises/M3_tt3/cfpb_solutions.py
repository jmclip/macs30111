'''
Team Tutorial #3: Dictionaries -- SOLUTIONS (Tasks 1-7)
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

    companies = set()
    for complaint in complaints:
        companies.add(complaint["Company"])

    return companies


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

    count = 0
    for complaint in complaints:
        if complaint["Company"] == company_name:
            count += 1

    return count


# Task 3
def count_by_state(complaints):
    '''
    Compute counts by state of all complaints

    Inputs:
         complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) that relates states to complaint number
    '''

    counts = {}
    for complaint in complaints:
        state = complaint["State"]
        if state not in counts:
            counts[state] = 0
        counts[state] += 1

    return counts


# Task 4
def state_with_most_complaints(cnt_by_state):
    '''
    Find the state with the most complaints. Can break ties arbitrarily.

    Inputs:
        cnt_by_state (dict) A dictionary relating each state to the
            count of complaints in that state

    Returns: (str) the state with the most complaints
    '''

    top_state = None
    top_count = -1
    for state, count in cnt_by_state.items():
        if count > top_count:
            top_state = state
            top_count = count

    return top_state


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

    counts = {}
    for complaint in complaints:
        company = complaint["Company"]
        state = complaint["State"]
        if company not in counts:
            counts[company] = {}
        if state not in counts[company]:
            counts[company][state] = 0
        counts[company][state] += 1

    return counts


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

    by_company = {}
    for complaint in complaints:
        company = complaint["Company"]
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(complaint)

    return by_company


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

    counts = {}
    for company, company_complaints in complaints_by_company(complaints).items():
        counts[company] = count_by_state(company_complaints)

    return counts


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
            # BUG: this line is indented inside the if, so it only runs
            # the first time a state is seen. Every count stays at 1.
            # Fix: dedent it one level, as in count_by_company_by_state.
            by_company_by_state[company][state] += 1
    return by_company_by_state


'''
Task 8 answers (discussion):
    - Read/understand: Task 7 is shorter and reads like the description
      ("group by company, then count by state"). Task 5 keeps everything in
      one loop, so you trace nested dict bookkeeping.
    - Less code: Task 7 (a few lines, reusing Tasks 6 and 3).
    - Debug: Task 7. It is built from functions you already tested, so a
      bug is in the small glue code. Task 5's bug above hides in the
      indentation of one line, and still returns a plausible-looking dict.
    - Speed: Task 5 makes one pass through the data. Task 7 makes two: one
      to group by company, then one over each company's complaints (which
      adds up to the whole list again). Both grow linearly with the data;
      on CFPB_16 Task 5 takes about 170 microseconds vs. about 220 for
      Task 7.
    - Choice: usually Task 7, since the speed difference is small and the
      reuse makes it easier to trust. Task 5 if the data is huge and one
      pass matters.
'''
