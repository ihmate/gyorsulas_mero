def main():
	f = open("proba_adat_mate.txt", "a")
	for i in range(0, 90):
		f.write(str(i) + "\n")
		f.write(str(i) + "\n")
	for x in range(0,10):
		for i in range(90, 100):
			f.write(str(i) + "\n")
			f.write(str(i) + "\n")
		for i in reversed(range(50, 100)):
			f.write(str(i) + "\n")
			f.write(str(i) + "\n")
		for i in range(50, 90):
			f.write(str(i) + "\n")
			f.write(str(i) + "\n")
		
	f.close()

if __name__ == "__main__":
    main()