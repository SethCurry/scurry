from mycroft import MycroftSkill, intent_file_handler


class Muninn(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('muninn.intent')
    def handle_muninn(self, message):
        self.speak_dialog('muninn')


def create_skill():
    return Muninn()

