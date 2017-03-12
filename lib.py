'''
==================
Library of classes
==================

:mod:`lib` -- Classes 'Question' and 'Applicant'
===============================================

.. module:: lib
   :platform: Linux, Windows
   :synopsis: Check whether to save applicantion or not
.. moduleauthor:: Leonid Sukharnikov <leonid.sukharn@gmail.com>
'''
from __future__ import print_function
import json
from dynamoConn import put_list_item, get_questions
import re

'''
.. class:: Question

    Question creates an object of questionnaire made by an employer.
    Main functionality: check the validity of the questionnaire.

      .. data:: question

         JSON formatted list of questions

      .. data:: employer

        Name of the employer who creates the questionnaire        
'''

class Question:
    def __init__(self, question, employer):
        self.question = question
        self.employer = employer
    
    def check_question(self):
        if self.question is not None:
            return self._check_question()
    
    def _check_question(self):
        'Returns a list of python dictionaries if the input in the correct format'
        l = Question.is_json(self.question)
        if l:
            if not isinstance(l, list):
                print('Wrong input data format. Are you loading a list of dictionaries?')
                return False
                
            for d in l:
                try:
                    d_keys = d.keys() 
                    d_values = d.values()
                except AttributeError, e:
                    print('Wrong input data format. Are you loading a list of dictionaries?')
                    return False
                #check whether keys are in place
                is_keys = [True for k in ["Id","Answer", "Question"] if k in d_keys]
                if not all(is_keys):
                    return 'One of the keys is missing. Please correct question'
                #check whether answers are in place
                is_values = [True for m in d_values if m != None]
                if not all(is_values):
                    return 'One of the values is missing. Please correct question'
        else:
            return 'Not a JSON object. Please correct input'
        l.append({'employer':self.employer})
        return l
        
    @staticmethod
    def is_json(json_obj):
        try:
            json_dict = json.loads(json_obj)
        except ValueError, e:
            return False
        return json_dict
        
'''
.. class:: Applicant

    Applicant creates an object of applicant's answers to a questionnaire.
    Main functionality: check the validity of the application.

      .. data:: application

         JSON formatted list of applicant answers     
'''

class Applicant:
    def __init__(self, application):
        self.application = application
    
    def check_application(self):
        if self.application is not None:
            return self._check_application()
    
    def _check_application(self):
        'Returns a list of python dictionaries if the input in the correct format'
        d = Question.is_json(self.application)
        if d:
            if not isinstance(d, dict):
                return False
            if d.get('Name', '') == '' or d.get('Questions', '') == '':
                return False
            if not isinstance(d['Questions'], list):
                return False
            for q in d['Questions']:
                try:
                    q_keys = q.keys() 
                    q_values = q.values()
                except AttributeError, e:
                    print('Wrong input data format. Are you loading a list of dictionaries?')
                    return False
                #check whether keys are in place
                is_keys = [True for k in ["Id","Answer"] if k in q_keys]
                if not all(is_keys):
                    print('One of the keys is missing. Please correct question')
                    return False
                #check whether answers are in place
                is_values = [True for m in q_values if m != None]
                if not all(is_values):
                    print('One of the values is missing. Please answer all questions')
                    return False
        else:
            return 'Not a JSON object. Please correct input'
        return d

'''
.. class:: Match

    Match contains methods for checking whether applicant's answers to a questionnaire
    are acceptable.
    Main functionality: check whether applicant passes or not.
    
      .. data:: employer

        Name of the employer who creates the questionnaire
        
      .. data:: application

         JSON formatted list of applicant answers     
'''
        
class Match:
    def __init__(self, employer, application):
        self.employer = employer
        self.application = application
        
    def get_employer_questions(self):
        self.questions = get_questions(self.employer)
        if self.questions:
            return True
        
    def match_questions(self):
        r_digits = re.compile('\d+$')
        r_ids = re.compile('Id')
        r_ans = re.compile('Answer')
        applicant_answers = dict()

        for d in self.application['Questions']:
            if isinstance(d, dict): 
                applicant_answers[d.get('Id', 'unknown')] = d.get('Answer')
        size = 0
        self.get_employer_questions()
        for item in self.questions:
            #print('item: %s' % item)
            if r_ids.match(item):
                size += 1
                #print("r_ids.match(item): %s" % r_ids.match(item).group())
        #print("size: %s" % size)
        ids = [0] * size
        answers = [0] * size
        for k, v in self.questions.items():
            if r_ids.search(k):
                ids[int(r_digits.search(k).group())-1] = v
                #print ("Id1: %s, int(r_digits.search(k).group()): %s" % (k, int(r_digits.search(k).group())))
            if r_ans.search(k):
                answers[int(r_digits.search(k).group())-1] = v
                #print ("a2: %s, int(r_digits.search(k).group()): %s" % (k, int(r_digits.search(k).group())))
        if len(ids) == len(answers):
            correct_answers = dict(zip(ids, answers))
        
        passing = True
        #print("correct answers: %s " % correct_answers)
        #print("applicant_answers: %s" % applicant_answers)
        if len(correct_answers) == len(applicant_answers):
            for k, v in correct_answers.items():
                if applicant_answers[k] != correct_answers[k]:
                    passing = False
        else:
            print("Error: maybe wrong questionnaire?")
            return False
            
        return (passing, self.application['Name'])

#testing syntax         
def test():
    q1 = Question('{"foo":[5,6.8],"foo":"bar"}', 'Starbucks')
    print('question: %s ' % q1.question)
    q1.check_question()
    q2 = Question('[ { "Id": "id1", "Question": "string", "Answer": "string" }, \
    { "Id": "id2", "Question": "string", "Answer": "string" }]', 'Starbucks')
    print('question: %s ' % q2.question)
    print(q2.check_question())
    #print(put_list_item(q2.check_question(), 'Questions')
    q3 = Question('[ { "Id": "1", "Question": "Whats your name", "Answer": "Jo" }, \
    { "Id": "2", "Question": "Whats your job?", "Answer": "Bartender" }]', 'Starbucks')
    #print(put_list_item(q3.check_question(), 'Questions'))
    q4 = Question('[ { "Id": "1", "Question": "Do you have high school diploma", "Answer": "yes" }, \
    { "Id": "2", "Question": "What was your main duty", "Answer": "porter" }, \
    { "Id": "3", "Question": "Do you have driver license", "Answer": "yes" }]', 'Hilton')
    #print(put_list_item(q4.check_question(), 'Questions'))
    a1 = Applicant('{ "Name": "Jack",  "Questions": [ {  "Id": "1", "Answer": "yes" }, \
    {  "Id": "2", "Answer": "porter" }, {"Id": "3", "Answer": "yes" }] }')
    apl1 = a1.check_application()
    m1 = Match('Hilton', apl1)
    m1.get_employer_questions()
    if m1.match_questions():
        print(apl1['Name'])
    
if __name__ == '__main__':
    test()        
