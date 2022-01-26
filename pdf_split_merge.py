from pdf2image import convert_from_path
import os
from PIL import Image

img = "pdf path"
pages = convert_from_path(img)


# split
for i, page in enumerate(pages):
    page.save(f"./models/pdf_temp/{pdf_name}_pdf%s.jpg" % i, "JPEG")

# merge
pdf_list = []
pdf_dir = os.listdir(f'data/masking/pdf/{filename.split(".")[0]}')
for i, pdf in enumerate(pdf_dir):
    if i == 0:
        image_main = Image.open(f'data/masking/pdf/{filename.split(".")[0]}/{pdf}').convert('RGB')
    else:
        pdf_list.append(Image.open(f'data/masking/pdf/{filename.split(".")[0]}/{pdf}').convert('RGB'))

image_main.save(f'data/masking/pdf/{filename}', save_all=True, append_images=pdf_list)