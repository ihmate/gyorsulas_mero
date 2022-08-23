def main():
	f = open("proba_adat.txt", "a")
	for i in range(200):
		f.write(str(i) + "\n")
	f.close()

if __name__ == "__main__":
    main()