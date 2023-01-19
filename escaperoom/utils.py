from enum import IntEnum

class LevelTypes(IntEnum):

    EASY = 1
    MEDIUM = 2
    HARD = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class QuestionChoices(IntEnum):

    TEXTBOX = 1
    MCQ = 2


    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]