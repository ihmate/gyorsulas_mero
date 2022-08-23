def main():
	f = open("proba_adat2.txt", "a")
	for i in range(20, 230, 15):
		f.write(str(i) + "\n")
	for i in range(230, 50, 35):
		f.write(str(i) + "\n")
	f.close()

if __name__ == "__main__":
    main()