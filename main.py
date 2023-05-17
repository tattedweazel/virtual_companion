from companions.mel import Mel
from conversations.kg_conversation import KGConversation


def main():
	human_name = input(" Enter your name, please: ")
	companion = Mel(id='Mel', mute=True, human_name=human_name)
	# if this is your first time running, set both first_time and clear_store to True - this will get the vectorstore set up right
	# once vectorstore is set up, change these both to False to keep memory between sessions. 
	session = KGConversation(companion=companion)
	session.start()


if __name__ == '__main__':
	main()
