from abc import ABC, abstractmethod


class EducationBaseService(ABC):

    @abstractmethod
    def create_education_history(self):
        """ Abstract method to get all Educations """
        pass