

class ClassTestClass(object):
    """Class Documentation"""
    class_variable = 'class_variable_content'
    CLASS_STATIC_VARIABLE = 'CLASS_STATIC_VARIABLE_CONTENT'

    def __init__(self, alpha, beta='beta_content'):
        self.theta = 'theta_content'

    def plain_method(self, alpha, beta='beta_content'):
        return None

    @staticmethod
    def static_method(self, alpha, beta='beta_content'):
        return None

    @classmethod
    def class_method(self, alpha, beta='beta_content'):
        return None
    
    @property
    def property_method(self, alpha, beta='beta_content'):
        return None
