from subprocess import Popen, PIPE

def gits_commit_tree(args):
	"""
	Function to visualize the past commit tree with highlights for each brach.
	"""
	print("Here is your Commit Tree")
	try:
		subprocess_command = list()
		subprocess_command.append("git")
		subprocess_command.append("log")
		subprocess_command.append("--pretty=format:\"%h %s %N\"")
		subprocess_command.append("--graph")
		process=Popen(subprocess_command, stdout=PIPE, stderr=PIPE)
		stdout,stderr=process.communicate()
		stdout=stdout.decode("utf-8")

		final=stdout.split("\n")
		final = list(filter(None, final)) 
		for f in final:
			print(f)

		if stderr.decode() != "" :
			print("Error Encountered! \n {}".format(stderr.decode()))
			
	except Exception as e:
		print("ERROR: gits status did not run correctly")
		print("ERROR: {}".format(str(e)))
		return False
	
	return True