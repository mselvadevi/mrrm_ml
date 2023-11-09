import os
file_name = "3.pdf"
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
fd= open(file_name, "rb")
viewer = SimplePDFViewer(fd)
print("welcome")
print(viewer.metadata)
print(viewer.render())
print(viewer.canvas.strings)

for canvas in viewer:
	page_images = canvas.images
	page_forms = canvas.forms
	page_text = canvas.text_content
	page_inline_images = canvas.inline_images
	page_strings = canvas.strings
	print(page_images)
