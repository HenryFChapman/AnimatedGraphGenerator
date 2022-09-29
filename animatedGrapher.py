
#Imports Necessary to Grab the Emojis
import requests
import re
import base64

#Pandas for Data Processing
import pandas as pd

#Matplotlib Imports for the Graphs
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import matplotlib.dates as mdates

#OS/Shutil to Create the Necessary Folders
import os
import shutil
import sys

#This bit of code finds and saves the emoji you want to embed in the graph
class EmojiConverter:

	#Initialize a class 
	def __init__(self):
		self.data = requests.get('https://unicode.org/emoji/charts/full-emoji-list.html').text
	
	#Converts the emoji to base64
	def to_base64_png(self, emoji, version=0):

		#Looking for just emojis in HTML
		html_search_string = r"<img alt='{}' class='imga' src='data:image/png;base64,([^']+)'>" #'
		matchlist = re.findall(html_search_string.format(emoji), self.data)
		return matchlist[version]

#This saves the emoji as the PNG
def saveEmoji(name):

	#Initialize the Emoji Converter Object
	e = EmojiConverter()
	#Convert it to Base64
	b64 = e.to_base64_png(name)

	#Decode It
	imgdata = base64.b64decode(b64)

	#Initialize File Name with the Emoji As the Name
	filename = name + '.png'  # I assume you have a way of picking unique filenames
	
	#Write the data to it
	with open(filename, 'wb') as f:
		f.write(imgdata)
	f.close()

def makeSetOfGraphs(emoji):

	#Read in data from Atlas
	data = pd.read_excel(sys.argv[1])
	
	#Save the New Emoji You Need
	saveEmoji(emoji)

	#Make the Folder To Put All The Graphs In
	if os.path.exists("Graphs"):
		shutil.rmtree("Graphs")
	os.mkdir("Graphs")

	#Loop Through DataFrame
	#ReDrawing a graph for each frame of data
	#For example, first graph is 0-1, second graph is 0-2, third graph is 0-3, ...
	for i in range(1, len(data.index)):
		
		#Grab the first i rows of data frame
		dataSegment = data.head(i).reset_index()

		#Creating Small Numbers (For More Readability)
		#Just Dividing by 1000
		dataSegment['Universe'] = dataSegment['Universe']/1000

		#Initialize Figure
		fig, ax = plt.subplots(figsize=(20, 8))

		#Get all your post volume data and dates as lists
		universe = dataSegment['Universe'].tolist()
		dates = dataSegment['Date'].tolist()

		#Plot the Data on a graph
		ax.plot(dates, universe, color='#22AAFF', lw=3, label='Post Volume');

		#Let's handle the emoji now!
		#Read the emoji you just saved as an image
		image = mpimg.imread(emoji + ".png",)
		
		#Embed Emoji where the last data point is.
		imagebox = OffsetImage(image, zoom=.75)
		ab = AnnotationBbox(imagebox, (dates[-1], universe[-1]), frameon=False)
		ax.add_artist(ab)

		#Initialize Y Label and set size for it
		ax.set_ylabel(sys.argv[1].split(" - ")[0] + " Post Volume (Thousands)", fontsize=25)
		
		ax.tick_params(axis='x', which='major', labelsize=10)

		#Format Dates Just As Years
		myFmt = mdates.DateFormatter('%Y')
		ax.xaxis.set_major_formatter(myFmt)

		ax.tick_params(axis='both', which='major', labelsize=30, colors='#005184')

		#Save Each Figure, then Close It Out
		plt.savefig("Graphs/" + str(i).zfill(3) + ".png", transparent = False, dpi = 150)
		plt.close()

makeSetOfGraphs(sys.argv[2])