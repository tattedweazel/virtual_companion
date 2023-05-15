from companions.mel import Mel
from components.vectorstore_conversation import VectorstoreConversation


def main():
	human_name = input(" Enter your name, please: ")
	companion = Mel(id='Mel', mute=True, human_name=human_name)
	session = VectorstoreConversation(companion=companion)
	session.start()


if __name__ == '__main__':
	main()
