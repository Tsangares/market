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
#question=questions[6]
answer=input(question['prompt']+"\n")
corret=None
correctAnswer=question['answer']
if issubclass(type(correctAnswer),str):
    correct=answer.lower()==correctAnswer.lower()
elif issubclass(type(correctAnswer),dict):
    try:
        correct=float(answer)==float(correctAnswer['number'])
    except:
        correct=str(answer)==str(correctAnswer['string'])
else:
    raise Exception("Problem with the oracle!")

print("That is %s!\n"%str(correct).lower())
if correct:
    me=getProfile()
    if me is None: print ("You dont have an account!")
    else:
        print("\nYou have earned %s Creativity!"%question['reward'])
        me.money+=question['reward']
        me.save()
        me.display()
