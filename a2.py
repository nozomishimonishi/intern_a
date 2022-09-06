import img2pdf

def convert2pdf(output_pdf,input_png1,input_png2): #pngをpdfに変換する
    with open(output_pdf,"wb") as f:
        f.write(img2pdf.convert([input_png1, input_png2]))

def convert2pdf_1 (output_pdf,input_png1):#１枚だけ
    with open(output_pdf,"wb") as f:
        f.write(img2pdf.convert(input_png1))
