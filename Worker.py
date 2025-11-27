from pathlib import Path
import os

class Worker:

	def __init__(self):
		self.all_dir = set()
		self.all_files = set()

	def run(self, path):

		self.all_dir.add(path)
		print("Worker with path", path, " start !")
		
		while True:
			if (len(self.all_dir) == 0):
				break
			copy_dir = self.all_dir
			self.all_dir = []
			for dir in copy_dir:
				for element in dir.iterdir():
					if element.is_dir():
						self.all_dir.add(element)
					else:
						self.all_files.add(element)
		
		return self.all_files
			
			