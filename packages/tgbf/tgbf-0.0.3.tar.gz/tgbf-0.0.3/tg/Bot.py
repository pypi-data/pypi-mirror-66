from .Content import Message
from copy import copy
class Bot:
    """ 
    Entry Point Class
    """
    def __init__(self, registered_handlers: list = [], api_key: str = '', api_address: str = 'https://api.telegram.org/bot'):
        """ Init method
        Receives the inital data required for the object and determines if the class can send responses back.
        """
        self.handlers = registered_handlers
        self.api_key = api_key
        self.api_address = api_address
    
    def process(self, obj: dict) -> object:
        if 'update_id' not in obj:
            raise ValueError("Expected update object. 'update_id' not found.")
        # Clean-up any previous properties
        self.message_scope = None
        self.id = obj['update_id']
        for key in obj:
            if key != 'update_id':
                self.response_type = self.r_type = key
        # Message handling
        if any(scope in obj for scope in ['message', 'edited_message', 'channel_post', 'edited_channel_post']):
            self.message_scope = copy(self.r_type)
            self.response_type = self.r_type = 'message'
            self.response = self.r = Message(obj, self.message_scope)
        # Inline handling
        elif 'inline_query' in obj:
            pass
        elif 'chosen_inline_result' in obj:
            pass
        
        # Callback handling
        elif 'callback_query' in obj:
            pass
        
        # Shipping handling
        elif 'shipping_query' in obj:
            pass
        elif 'pre_checkout_query' in obj:
            pass
        
        # Poll handling
        elif 'poll' in obj:
            pass
        elif 'poll_answer' in obj:
            pass
        return self