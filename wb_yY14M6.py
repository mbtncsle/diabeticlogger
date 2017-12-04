
def queen(i, solution):
	if i==len(solution)-1:
		# solution is completely configured. At the bottom.
		print(solution)
	else:
		# soluton is not completely configured.
		if promising(i, solution):
			for choice in range(len(solution)):
				if choice not in solution[0:i+1]:
					solution[i+1] = choice
					queen(i+1, solution)

#---------------------------------------------
def promising(i, solution):
	for j in range(0, i):
		if i - j == abs(solution[i] - solution[j]):
			return False
	return True
