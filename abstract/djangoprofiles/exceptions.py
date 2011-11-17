#-*- coding: utf-8 -*-


class MissingAttribute(Exception):
    """
    This exception is thrown when a given mandatory attribute is missing.
    """
    
    def __init__(self, msg):
        """
        """
        
        # In case it's fired, you're Escher
        assert msg
        
        self.msg = msg
        
    def __str__(self):
        return "'%s' attribute is missing" % self.msg
        
