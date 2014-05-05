#coding: utf-8
#Programming by Szymon Wanot & Paweł Siemienik
#Graphics by Marcelina Stuchlik
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty,StringProperty,\
        ListProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
import question

class PlayWidget(Widget):
    current_question = NumericProperty(0)
    current_q_text = StringProperty('')
    current_a_list = ListProperty(['a','a','a','a'])

    def depackQuestionary(self, quiz_type):
        self.path = 'questionares/'+ quiz_type +'.json'
        self.parsed_json = question.openQuestionareJson(self.path)
        self.questionare = question.parseJsonToQuestionare(self.parsed_json)

    def setQuestion(self):
        self.current_q = self.questionare.getQuestionById(self.current_question)
        self.current_q_text = self.current_q.getText()
        self.current_answers = self.current_q.getAnswers()
        self.current_a_list = self.current_answers.keys()[:]
        print 'questions: ', self.questionare.getQuestionsCount()
         
    def onClick(self, text):
        self.parent.score.append(self.current_answers[text])
        print self.current_answers[text] , self.current_question
        if self.current_question + 1 >= self.questionare.getQuestionsCount():
            self.current_question = 0
            self.parent.countScore()
        
class StartScreen(Screen):
    pass

class ChooseQuiz(Screen):
    def setOption(self, text):
        self.parent.option = text

class PlayScreen(Screen):
    quiz = ObjectProperty(None)
    score = ListProperty([])

    def on_pre_enter(self):
        self.quiz.depackQuestionary(self.parent.option)
        self.quiz.setQuestion()

    def countScore(self):
        self.ra = 0
        self.wa = 0
        for i in self.score:
            if i == 'True':
                self.ra += 1
            elif i == 'False':
                self.wa += 1
        self.parent.right_answers = self.ra
        self.parent.wrong_answers = self.wa
        self.manager.current = 'score'

    def on_leave(self):
        self.quiz.current_question = 0 
        del self.score[:]   
            
class HighScoreScreen(Screen):
    right_answers = NumericProperty(0)
    wrong_answers = NumericProperty(0)
    
    def on_pre_enter(self):
        self.right_answers = self.parent.right_answers
        self.wrong_answers = self.parent.wrong_answers

    def on_leave(self):
        self.right_answers = 0
        self.wrong_answers = 0
        self.manager.right_answers = self.right_answers
        self.manager.wrong_answers = self.wrong_answers

class QuizApp(App):
    def build (self):
        Config.set('graphics', 'widht', 745)
        Config.set('graphics', 'height', 1049)
        Config.set('graphics', 'resizable', 0)
        sm = ScreenManager()
        sm.right_answers = NumericProperty(0)
        sm.wrong_answers = NumericProperty(0)
        sm.add_widget(StartScreen(name = 'menu'))
        sm.add_widget(ChooseQuiz(name = 'chooser'))
        sm.add_widget(PlayScreen(name = 'play'))
        sm.add_widget(HighScoreScreen(name = 'score'))
        return sm

if __name__ == '__main__':
    QuizApp().run();
