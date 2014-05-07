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
from kivy.animation import Animation
from kivy.core.audio import SoundLoader, Sound
import question

class PlayWidget(Widget):
    current_question = NumericProperty(0)
    current_q_text = StringProperty('')
    current_a_list = ListProperty(['a','a','a','a'])
    correct_sound = SoundLoader.load('sound/Fuzzy Beep-SoundBible.com-1580329899.wav')
    wrong_sound = SoundLoader.load('sound/Computer Error-SoundBible.com-399240903.wav')

    def depackQuestionary(self, quiz_type):
        self.path = 'questionares/'+ quiz_type +'.json'
        self.parsed_json = question.openQuestionareJson(self.path)
        self.questionare = question.parseJsonToQuestionare(self.parsed_json)

    def setQuestion(self):
        self.current_q = self.questionare.getQuestionById(self.current_question)
        self.current_q_text = self.current_q.getText()
        self.current_answers = self.current_q.getAnswers()
        self.current_a_list = self.current_answers.keys()[:]
         
    def onClick(self, text):
        value = self.current_answers[text]
        self.parent.score.append(value)
        if value == 'True':
            self.correct_sound.play()
        elif value == 'False':
            self.wrong_sound.play()
        if self.current_question + 1 >= self.questionare.getQuestionsCount():
            self.current_question = 0
            self.parent.countScore()
            
    def releaseSound(self):
        if self.correct_sound.state == 'play':
            self.correct_sound.stop()
        if self.wrong_sound.state == 'play':
            self.wrong_sound.stop()

class StartScreen(Screen):
    click_sound = SoundLoader.load('sound/Click2-Sebastian-759472264.mp3')
    
    def on_pre_enter(self):
        self.bounce = Animation(size_hint= (0.35, 0.35))\
                + Animation(size_hint= (0.3,0.3))
        self.bounce.repeat = True
        self.bounce.start(self.ids.owl)
        self.bounce.start(self.ids.questions)
    def on_leave(self):
        self.bounce.cancel(self.ids.owl)
        self.bounce.cancel(self.ids.questions)

    def onClickSound(self):
        self.click_sound.play()

class ChooseQuiz(Screen):
    click_sound = SoundLoader.load('sound/Click2-Sebastian-759472264.mp3')
    
    def setOption(self, text):
        self.parent.option = text
    
    def onClickSound(self):
        self.click_sound.play()

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
    click_sound = SoundLoader.load('sound/Click2-Sebastian-759472264.mp3')

    def on_pre_enter(self):
        self.right_answers = self.parent.right_answers
        self.wrong_answers = self.parent.wrong_answers

    def on_leave(self):
        self.right_answers = 0
        self.wrong_answers = 0
        self.manager.right_answers = self.right_answers
        self.manager.wrong_answers = self.wrong_answers
    
    def onClickSound(self):
        self.click_sound.play()

class QuizApp(App):
    def build_config(self, config):
        Config.set('graphics', 'width', 600)
        Config.set('graphics', 'height', 800)
        Config.set('graphics', 'resizable', 0)

    def build (self):
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
