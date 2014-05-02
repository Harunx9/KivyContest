import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty,StringProperty,\
        DictProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
import question


class PlayWidget(Widget):
    current_question = NumericProperty(0)
    current_q_text = StringProperty('')
    current_a_list = DictProperty(None)

    def depackQuestionary(self, quiz_type):
        self.path = 'questionares/'+ quiz_type +'.json'
        self.parsed_json = question.openQuestionareJson(self.path)
        self.questionare = question.parseJsonToQuestionare(self.parsed_json)

    def setQuestion(self):
        self.current_q = self.questionare.getQuestionById(self.current_question)
        self.current_q_text = self.current_q.getText()

    def onClick(self, touch):
        pass

class StartScreen(Screen):
    pass

class ChooseQuiz(Screen):
    def setOption(self, text):
        self.parent.option = text

class PlayScreen(Screen):
    quiz = ObjectProperty(None)

    def on_pre_enter(self):
        self.quiz.depackQuestionary(self.parent.option)
        self.quiz.setQuestion()

    def countScore(self):
        pass

class QuizApp(App):
    def build (self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name = "menu"))
        sm.add_widget(ChooseQuiz(name = "chooser"))
        sm.add_widget(PlayScreen(name = "play"))
        return sm

if __name__ == '__main__':
    QuizApp().run();
