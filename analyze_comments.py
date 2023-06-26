from conversations.comment_analyzer import CommentAnalyzer


def main():


	ca_1 = CommentAnalyzer('source/cancel_results.json')
	ca_2 = CommentAnalyzer('source/cancel_results.json')
	ca_3 = CommentAnalyzer('source/cancel_results.json')
	print("Getting First Summary...\n")
	ca_1.start()
	print("Getting Second Summary...\n")
	ca_2.start()
	print("Getting Third Summary...\n")
	ca_3.start()
	print("\n\nSummaries\n")
	print("Alice says:")
	print(f"{ca_1._final_summary}\n\n")
	print("Bob says:")
	print(f"{ca_2._final_summary}\n\n")
	print("Charlie says:")
	print(f"{ca_3._final_summary}\n\n")
	######




	
	


if __name__ == '__main__':
	main()
