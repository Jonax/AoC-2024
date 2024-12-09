import gzip
import os
import requests
import sys
from bs4 import BeautifulSoup
from datetime import date, datetime

def GetYearProgress(session, year):
	response = requests.get(
		f"https://adventofcode.com/{year}/", 
		headers = {"Cookie": f"session={session}"}
	)

	assert response.status_code == 200

	html = BeautifulSoup(response.text, "html.parser")

	days = {d:-1 for d in range(1, 26)}

	calendar = html.find("pre", class_ = "calendar")
	for i, activeDay in enumerate(calendar.find_all("a"), 1):
		classes = activeDay.get("class")
		if "calendar-verycomplete" in classes:
			assert activeDay.get("aria-label") == f"Day {i}, two stars"
			days[i] = 2
		elif "calendar-complete" in classes:
			assert activeDay.get("aria-label") == f"Day {i}, one star"
			days[i] = 1
		else:
			days[i] = 0

	return days

def DownloadDayInput(session, year, day):
	inputPath = f"inputs/day{day:02}_input.txt"

	inputDir = os.path.dirname(inputPath)
	if any(inputDir) and not os.path.isdir(inputDir):
		os.makedirs(inputDir)

	response = requests.get(
		f"https://adventofcode.com/{2024}/day/{day}/input", 
		headers = {"Cookie": f"session={session}"},
		stream = True)
	assert response.status_code == 200

	contents = response.raw.read()
	if response.headers.get("Content-Encoding") == "gzip":
		contents = gzip.decompress(contents)

	with open(inputPath, "w") as outFile:
		outFile.write(contents.decode("utf-8").strip())

if __name__ == "__main__":
	assert len(sys.argv) == 2

	year = date.today().year
	try:
		year = int(sys.argv[1])

		if not (2015 <= year <= date.today().year):
			raise Exception(f"Year out of range: {year}")
	except ValueError:
		raise Exception(f"Unrecognised year: {year}")

	if not os.path.isfile("tools/.session"):
		raise Exception("Session should be available separately before using this script.")

	session = None
	with open("tools/.session") as inFile:
		session = inFile.read().strip()
	assert session != None

	numNewFiles = 0
	for day, state in GetYearProgress(session, year).items():
		if state == -1:
			continue

		inputPath = f"inputs/day{day:02}_input.txt"
		inputDownloaded = os.path.isfile(inputPath)
		inputStatus = inputDownloaded and "Input is present" or "Input needs downloading"

		dayStatus = "Ready"
		if state == 1:
			dayStatus = "Part 1 Complete"
		elif state == 2:
			dayStatus = "Day Complete"
		else:
			assert state == 0

		print(f"[Day {day}] {dayStatus}, {inputStatus}")
		if not inputDownloaded:
			DownloadDayInput(session, year, day)
			numNewFiles += 1

	if numNewFiles != 0:
		sys.exit(numNewFiles)
