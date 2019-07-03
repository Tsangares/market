import sys
sys.path.insert(0,'../src')

import yaml,random
from Business import Business
from db import getProfile
questions=None
with open('oracle.yaml', 'r') as f:
    oracleQuestions=yaml.safe_load(f.read())
    questions=oracleQuestions

question=random.choice(questions)
answer=input(question['prompt']+"\n")
corret=None
if issubclass(type(answer),str):
    correct=answer.lower()==str(question['answer']).lower()
else issubclass(type(answer),dict):
    try:
        correct=float(answer)==float(question['answer']['number'])
    except:
        correct=str(answer)==str(question['answer']['string'])
        

print("That is %s!\n"%str(correct).lower())
if correct:
    me=getProfile()
    if me is None: print ("You dont have an account!")
    else:
        print("\nYou have earned %s Creativity!"%question['reward'])
        me.money+=question['reward']
        me.save()
        me.display()
