


class CliInterface():

    def __init__(self) -> None:
        self.user_name = input("Please enter your name: ")


    def get_user_input(self) -> str:
        return input(": ")
    

    def get_user_name(self) -> str:
        return self.user_name
    

    def get_user_label(self) -> str:
        return self.user_name + ": "
    

    def return_response(self, response="") -> None:
        print(response)
