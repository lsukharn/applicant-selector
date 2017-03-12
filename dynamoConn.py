from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

#Notice: you must apply AWS credentials through AWS CLI 
dn = boto3.resource('dynamodb')

'''
Returns the last employer's questionnaire Id 
'''
def get_recent_id(table_dn):
    response = table_dn.scan(ProjectionExpression="list_id")
    ids = map(lambda x: x.values()[0], response['Items'])
    #print(ids)
    if len(ids) != 0:
        last_in = max(ids)
    else:
        last_in = 1
    return last_in
    
'''
    Inserts an item into dynamodb table (parameter: table) 
    
    Args:
        item (list): a list of dictionaries that describe employer and 
                    questions, for example:
                    
        [{u'Answer': u'string', u'Question': u'string', u'Id': u'id1'}, 
        {u'Answer': u'string', u'Question': u'string', u'Id': u'id2'}, 
        {'employer': 'Starbucks'}]
                
        table (str): The name of table in dynamodb.

    Returns:
        response: Returns an object that indicates success or 
        failure of the insertion.

'''
def put_list_item(item, table):
    if item == False:
        print("Incorrect question format")
        return False
        
    table_dn = dn.Table(table)
    list_id = get_recent_id(table_dn)
    print("list_id: %s" % list_id)
    row = dict()
    count = 0
    for d in item:
        if d.get('Id', '') == '':
            if table == 'Questions':
                row['employer'] = d.get('employer', '')
                continue
        count += 1
        row['list_id'] = list_id + 1
        
        #add counts to column names to distinguish columns
        d['Id'+str(count)] = d.pop('Id')
        d['Question'+str(count)] = d.pop('Question')
        d['Answer'+str(count)] = d.pop('Answer')
        row.update(d)
    response = table_dn.put_item(
            Item=row,
            Expected={
               'list_id': {'Exists': False} #check for collisions
            }
    )
    return response


'''
    Returns a dictionary of employer questions and other 
    employer information. 
    
    Args:
        employer (str): Name of the employer

    Returns:
        questions: Returns an object that contains employer's 
        questions

'''
def get_questions(employer):
    table = dn.Table('Questions')
    
    fe = Key('employer').eq("employer")
    response = table.scan(
    FilterExpression=Attr('employer').eq(employer)
)
    questions = list()
    for i in response['Items']:
        #print("i: %s" % i)
        questions.append(i)
        return questions[0]
