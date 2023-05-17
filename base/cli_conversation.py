import json
from tools.secret_squirrel import SecretSquirrel
from datetime import datetime


class CliConversation():

    def __init__(self, companion):
        self.creds = SecretSquirrel().stash
        self.companion = companion
        self.stop = False
        self.message_log = []
        self.conversation_chain = None


    def get_user_prompt(self):
        print("\n")
        prompt =  input("-> ")
        print("\n")
        return prompt
    

    def store_conversation(self):
        with open(f"logs/{datetime.strftime(datetime.now(),'%Y%m%d_%H_%M_%S')}.json", "w") as outfile:
            json.dump(self.message_log, outfile, indent=4)

        print("Conversation successfully stored")


    def end_conversation(self):
        msg = f"Goodbye."
        self.companion.say(msg)
        self.store_conversation()
        exit()


    def advance_conversation(self, prompt):
        self.message_log.append({
            "sender": self.companion.human_name,
            "content": prompt
        })
        response = self.conversation_chain.predict_and_parse(human_input=prompt)
        self.message_log.append({
            "sender": self.companion.name,
            "content": response
        })
        return response


    def conversation_loop(self):
        while not self.stop:
            prompt = self.get_user_prompt()

            if prompt.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
                self.stop = True
                break

            response = self.advance_conversation(prompt=prompt)
            self.companion.say(response)

        self.end_conversation()


    def start(self):
        self.conversation_loop()