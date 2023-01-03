L = [1, 2, 3, 3, 4, 5, 5]

for i in range(1, len(L) - 1):
	if L[i] == L[i - 1]:
		L.pop(L[i])

print(L)