#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import glob

# Delete previous PDF files
for file in glob.glob("Output/*.pdf"):
	os.remove(file)
for file in glob.glob("*.pdf"):
	os.remove(file)

subprocess.call(['pdflatex', 'back_black.tex'])
subprocess.call(['pdflatex', 'back_white.tex'])
subprocess.call(['pdflatex', 'front_white_background.tex'])
subprocess.call(['pdflatex', 'front_black_background.tex'])
subprocess.call(['pdflatex', 'front_black_pick2_background.tex'])
subprocess.call(['pdflatex', 'front_black_draw2pick3_background.tex'])

colors = ['white', 'black', 'black_pick2', 'black_draw2pick3']
for color in colors:
	file = open("Input/text_" + color + ".txt", 'r',  encoding='utf-8')
	finalString = ""
	i = 0
	for line in file:
		if i%9 == 0:
			finalString += "\\pageOfCards"
		finalString += "{" + line + "}"
		i += 1
	file.close()
	while i%9 > 0:
		finalString += "{}"
		i += 1
	outputFile = open('latexifiedText.tex', 'w',  encoding='utf-8')
	finalString = finalString.replace("\r", "")
	finalString = finalString.replace("\n", "")
	finalString = finalString.replace("%", "\%")
	finalString = finalString.replace("$", "\\$")
	for punctuation in (",", ".", ":", ";", "!", "?", ""):
		finalString = finalString.replace("___" + punctuation, " \\mbox{\\rule{2cm}{0.8pt}\\hrulefill\\ " + punctuation + " \\ \\newline} ")
	outputFile.write(finalString)
	outputFile.close()

	actualColor = color[:5]
	subprocess.call(['pdflatex', 'text_' + actualColor + '.tex'])
	os.remove('latexifiedText.tex')
	subprocess.call(['pdftk', "text_" + actualColor + ".pdf", "background", "front_" + color + "_background.pdf", "output", "front_" + color + ".pdf"])
	os.remove('text_' + actualColor + '.pdf')
os.rename('front_white_background.pdf', 'front_white_blank.pdf')
subprocess.call(['pdflatex', 'front_black_blank.tex'])
subprocess.call(['pdflatex', 'front_black_pick2_blank.tex'])
subprocess.call(['pdflatex', 'front_black_draw2pick3_blank.tex'])
os.remove('front_black_background.pdf')
os.remove('front_black_pick2_background.pdf')
os.remove('front_black_draw2pick3_background.pdf')

# Clean LaTeX files
extensions = ("*.aux", "*.bbl", "*.blg", "*.brf", "*.idx", "*.ilg", "*.ind", "*.lof", "*.log", "*.lol", "*.lot", "*.out", "*.toc", "*.synctex.gz")
for ext in extensions:
	for file in glob.glob(ext):
		os.remove(file)

# Move PDF files in Output folder
for file in glob.glob("*.pdf"):
    os.rename(file, "Output/" + file)