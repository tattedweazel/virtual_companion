


class CliInterface():

    def __init__(self) -> None:
        self.user_name = input("Please enter your name: ")
        self.companion_name = input("Please enter the name of your companion: ")


    def get_user_input(self) -> str:
        return input(": ")
    

    def get_user_name(self) -> str:
        return self.user_name
    

    def get_companion_name(self) -> str:
        return self.companion_name
    

    def get_user_label(self) -> str:
        return self.user_name + ": "
    

    def return_response(self, response="") -> None:
        print(f"\n>> {response}\n")
