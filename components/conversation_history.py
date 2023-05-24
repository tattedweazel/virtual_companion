import json
from datetime import datetime


class ConversationHistory():

    def __init__(self) -> None:
        self.exchanges = []


    def summary_export(self) -> str:
        export = ""
        for exchange in self.exchanges:
            export += exchange.as_string() + "\n"
        return export
    

    def k_latest(self, k=4, as_list=False) -> str:
        results = []
        for exchange in self.exchanges:
            results.append(exchange.as_string())
        if as_list:
            return results
        return "\n".join(results[-(k):])
    

    def add_exchange(self, exchange=None) -> None:
        self.exchanges.append(exchange)

    
    def save(self) -> None:
        exchanges = []
        for exchange in self.exchanges:
            exchanges.append(exchange.as_dict())
        with open(f"logs/{datetime.strftime(datetime.now(),'%Y%m%d_%H_%M_%S')}.json", "w") as outfile:
            json.dump(exchanges, outfile, indent=4)
        print("Conversation successfully stored")
       