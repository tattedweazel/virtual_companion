


class Exchange():

    def __init__(self, user_input=None, response=None) -> None:
        self.user_input = user_input
        self.response = response


    def as_string(self) -> str:
        return f"Input: {self.user_input}\nResponse: {self.response}"
    

    def as_dict(self) -> dict:
        return {
            "Input": self.user_input,
            "Response": self.response
        }