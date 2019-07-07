class test:
    def __iter__(self):
        yield 'ame', 'a'

class quiz(test):
    def __iter__(self):
        yield 'hey','apple'
        return super(quiz,self).__iter__()

print(dict(quiz()))
