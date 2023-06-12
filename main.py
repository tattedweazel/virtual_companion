#from conversations.component_conversation import ComponentConversation
from conversations.comment_analyzer import CommentAnalyzer


def main():
	## Component Conversation
	#session = ComponentConversation(verbose=True)
	#session.start()
	######

	## Comment Analyzer
	lp_ca = CommentAnalyzer('source/lp_outlast_trials.json') # Any json file with is a list of json objects composed like: {"comment": "this is the comment"}
	rt_ca = CommentAnalyzer('source/rt_podcast_final.json')
	print("Hang tight...\n")
	lp_ca.start()
	print("Like, this seriously takes a minute...\n")
	rt_ca.start()
	print("Let's Play: Outlast Trials\n")
	print(lp_ca._final_summary)
	print("\n\nRT Podcast: Gus' final episode\n")
	print(rt_ca._final_summary)
	######




	
	


if __name__ == '__main__':
	main()
