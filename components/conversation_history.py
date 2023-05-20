from base.exchange import Exchange


class ConversationHistory():

    def __init__(self) -> None:
        self.exchanges = []


    def summary_export(self) -> str:
        return str(self.exchanges)
    

    def k_latest(self, k) -> str:
        return str(self.exchanges)
    

    def add_exchange(self, user_input=None, response=None) -> None:
        self.exchanges.append(Exchange(user_input=user_input, response=response))

    
    def save(self) -> None:
        print("stored.")