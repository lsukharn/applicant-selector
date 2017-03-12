'''

Main script

'''

from lib import Question, Applicant, Match
from dynamoConn import put_list_item, get_questions

def main():
    #First create three employers' questionnaires: 
    #Starbucks, TGI Friday and Hillton
    '''
    e1 = Question('[ { "Id": "1", "Question": "Do you have high school diploma", "Answer": "yes" }, \
    { "Id": "2", "Question": "What was your main duty", "Answer": "barista" }, \
    { "Id": "3", "Question": "Do you have driver license", "Answer": "yes" }]', 'Starbucks')
    e2 = Question('[ { "Id": "1", "Question": "Do you have high school diploma", "Answer": "yes" }, \
    { "Id": "2", "Question": "What was your main duty", "Answer": "bartender" }, \
    { "Id": "3", "Question": "Do you have driver license", "Answer": "yes" }]', 'TGI Friday')
    e3 = Question('[ { "Id": "1", "Question": "Do you have high school diploma", "Answer": "yes" }, \
    { "Id": "2", "Question": "What was your main duty", "Answer": "front desk" }, \
    { "Id": "3", "Question": "Do you have driver license", "Answer": "yes" }]', 'Hilton')
    
    #Then write them into dynamodb 'Questions' table (one employer per row)
    put_list_item(e1.check_question(), 'Questions')
    put_list_item(e2.check_question(), 'Questions')
    put_list_item(e3.check_question(), 'Questions')
    '''
    #Second, create three applicantions
    a1 = Applicant('{ "Name": "Jack Doe",  "Questions": [ {  "Id": "1", "Answer": "yes" }, \
    {  "Id": "2", "Answer": "barista" }, {"Id": "3", "Answer": "yes" }] }')
    a2 = Applicant('{ "Name": "John Smith",  "Questions": [ {  "Id": "1", "Answer": "yes" }, \
    {  "Id": "2", "Answer": "bartender" }, {"Id": "3", "Answer": "yes" }] }')
    a3 = Applicant('{ "Name": "Cathy Bell",  "Questions": [ {  "Id": "1", "Answer": "yes" }, \
    {  "Id": "2", "Answer": "front desk" }, {"Id": "3", "Answer": "yes" }] }')
    
    #Then check their applications (all correct)
    m1 = Match('Starbucks', a1.check_application()).match_questions()
    m2 = Match('TGI Friday', a2.check_application()).match_questions()
    m3 = Match('Hilton', a3.check_application()).match_questions()
    print("m1: %s, m2: %s, m3: %s" % (m1, m2, m3))
    with open('reult.txt', 'a') as f:
        for n in [m1, m2, m3]:
            if n[0]:
                f.write(n[1]+'\n')
    
    #Then check more applications (all incorrect, wrong questionnaire)
    m1 = Match('TGI Friday', a1.check_application()).match_questions()
    m2 = Match('Starbucks', a2.check_application()).match_questions()
    m3 = Match('Starbucks', a3.check_application()).match_questions()
    print("m1: %s, m2: %s, m3: %s" % (m1, m2, m3))
    with open('result.txt', 'a') as f:
        for n in [m1, m2, m3]:
            if n[0]:
                f.write(n[1]+'\n')
                
    #Create application with incorrect answer
        a4 = Applicant('{ "Name": "Amy Wong",  "Questions": [ {  "Id": "1", "Answer": "yes" }, \
    {  "Id": "2", "Answer": "engineer" }, {"Id": "3", "Answer": "yes" }] }')
    m4 = Match('Starbucks', a4.check_application()).match_questions()
    print(m4)

if __name__ == '__main__':
    main()