from json import load 

class Question(object):
    def __init__(self, question):
        self.text = question.get("text")
        self.answers = question.get("answers")

    def getText(self):
        return self.text

    def getAnswers(self):
        return self.answers

class Questionare(object):
    def __init__(self, questions):
        self.questions = questions

    def getQuestionById(self, index):
        return Question(question=
                self.questions[index])
    
    def getQuestionsCount(self):
        return len(self.questions)

def openQuestionareJson(path):
    with open(path) as data_file:
         json = load(data_file)
    return json

def parseJsonToQuestionare(json_dict):
    return Questionare (questions= json_dict['questionare'])
