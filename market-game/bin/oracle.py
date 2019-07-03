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
correct= str(answer).lower()==str(question['answer']).lower()
print("That is %s!\n"%str(correct).lower())
if correct:
    me=getProfile()
    print("\nYou have earned %s Creativity!"%question['reward'])
    me.money+=question['reward']
    me.save()
    me.display()

