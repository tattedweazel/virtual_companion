from tools.el_speech_module import ELSpeechModule


class CliInterface():

    def __init__(self) -> None:
        self.voice = ELSpeechModule(el_model_id='u28dyDoKv8tV8iyBwvPx')
        self.user_name = input("Please enter your name: ")
        self.companion_name = input("Please enter the name of your companion: ")
        mute_input = input("Enable AI Voice? [ yes | no ]: ")
        self.voice_enabled = True if mute_input.lower() in ['yes', 'y'] else False


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
        if self.voice_enabled:
            self.voice.say(response)
