from datetime import datetime
class Message:
    def __init__(self, update_obj: dict, scope: str):
        obj = update_obj[scope]
        # Message Meta data
        self.message_id = self.id = obj['message_id']
        self.unix_date = obj['date']
        self.date = datetime.fromtimestamp(obj['date'])
        ## Message type
        self.general_type = 'unknown'
        common_types = ['text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'voice',
        'video_note', 'contact', 'location', 'venue', 'poll', 'dice', 'new_chat_members', 'left_chat_member',
        'new_chat_title', 'new_chat_photo', 'pinned_message', 'invoice', 'successful_payment']
        service_types = ['delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created']
        # Special types are determined manually: migration, passport
        for msg_type in common_types:
            if msg_type in obj:
                self.general_type = 'common'
                self.type = msg_type
        if self.general_type == 'unknown':
            for msg_type in service_types:
                if msg_type in obj:
                    self.general_type = 'service'
                    self.type = msg_type
        if self.general_type == 'unknown':
            self.type = 'unknown'
            pass # TODO implement custom types

        # Message sender
        self.sender = User(obj['from'])


class User:
    """ User object """
    def __init__(self, obj: dict):
        self.id = obj['id']
        self.is_bot = self.bot = bool(obj['is_bot'])
        self.first_name = obj['first_name']

        self.last_name = findOrEmpty(obj, 'last_name')
        self.full_name = self.name = self.first_name + findOrEmpty(obj, 'last_name', True)
        
        self.username = findOrEmpty(obj, 'username')
        self.language_code = self.locale = findOrEmpty(obj, 'language_code')

        self.can_join_groups = findOrNone(obj, 'can_join_groups')
        self.can_read_all_group_messages = findOrNone(obj, 'can_read_all_group_messages')
        self.supports_inline_queries = findOrNone(obj, 'supports_inline_queries')

class Chat:
    """ Chat object """
    def __init__(self, obj: dict):
        self.id = obj['id']
        self.type = obj['type']
        # Chat Name
        self.title = findOrEmpty(obj, 'title')
        self.username = findOrEmpty(obj, 'username')
        self.first_name = findOrEmpty(obj, 'first_name')
        self.last_name = findOrEmpty(obj, 'last_name')
        self.photo = findOrNone(obj, 'photo') # TODO: Process this once content class has it.
        self.description = findOrEmpty(obj, 'descriptipn')
        self.invite_link = findOrEmpty(obj, 'invite_link')
        self.pinned_message = findOrNone(obj, 'pinned_message')
        self.permissions = findOrNone(obj, 'permissions')
        self.slow_mode_delay = findOrNone(obj, 'slow_mode_delay')
        self.sticker_set_name = findOrEmpty(obj, 'sticker_set_name')
        self.can_set_sticker_set = findOrNone(obj, 'can_set_sticker_set')

        if self.type == 'private':
            self.name = self.title
        else:
            self.name = self.first_name + findOrEmpty(obj, 'last_name', True)

def findOrEmpty(obj: dict, param: str, padding: bool = False):
    """ Finds a string parameter in an dict, adds a space before the value if set """
    if param not in obj:
        return ''
    if padding:
        return ' ' + str(obj[param])
    return obj[param]
def findOrVar(obj: dict, param: str, var):
    if param not in obj:
        return var
    return obj[param]

def findOrNone(obj: dict, param:str):
    return findOrVar(obj, param, None)