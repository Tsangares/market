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
#question=questions[0]
answer=input(question['prompt']+"\n")
corret=None
try:
    question['no_answer']
    correct=True
except:
    correctAnswer=question['answer']
if correct==True:
    pass
elif issubclass(type(correctAnswer),dict):
    try:
        correct=float(answer)==float(correctAnswer['number'])
    except:
        correct=str(answer)==str(correctAnswer['string'])
elif issubclass(type(correctAnswer),str):
    correct=str(answer).lower()==correctAnswer.lower()
elif issubclass(type(correctAnswer),int):
    correct=int(answer)==correctAnswer
elif issubclass(type(correctAnswer),float):
    correct=float(answer)==correctAnswer
else:
    raise Exception("Problem with the oracle!",type(answer), type(correctAnswer))

print("That is %s!\n"%str(correct).lower())
if correct:
    me=getProfile()
    if me is None: print ("You dont have an account!")
    else:
        print("\nYou have earned %s Creativity!"%question['reward'])
        me.money+=question['reward']
        me.save()
        me.display()
