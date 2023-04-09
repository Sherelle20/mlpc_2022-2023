# -*- coding: utf-8 -*-
import pytesseract
import os, shutil, cv2
from django.shortcuts import render
from django.http import HttpResponse
import subprocess


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def home(request):
    
    var = False
    ctx = {}
    result = ""
    if request.method == 'POST':
        
        
        destination_directory = os.path.join(BASE_DIR, 'images')
        
        uploaded_file = request.FILES['myfile']
        
        print("uploaded_file",uploaded_file)

      
        with open(os.path.join(destination_directory, uploaded_file.name), 'wb') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)

        myfile = destination_directory +'/'+ str(uploaded_file)
        #print("dim myfile", get_shape(myfile))
        
        
        if myfile.endswith(('png', 'jpeg', 'jpg')):
            result = read_image(myfile)
        else:
            var = True
    
    request.session['ocr_result'] = result
    ctx = {'result': result, 'var':var}
    
 
    return render(request, 'yemba_ocr_tool/index.html', ctx)


def download_file(request):
   
    # get the OCR result from the session
    result = request.session.get('ocr_result', '')
    # Créer le dossier de sortie si nécessaire
    if not os.path.exists('documents'):
        os.makedirs('documents')
    # create a new text file with the OCR result
    filename = 'ocr_result.txt'
    with open(os.path.join('documents', filename), 'w') as f:
        f.write(result)

    # generate a download response for the text file
    with open(os.path.join('documents', filename), 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response



def read_image(img_path, lang='ybb-eng'):

    """
    try:
        command = "sudo tesseract {0} output_text --tessdata-dir /usr/share/tesseract-ocr/5/tessdata/ -l {1}".format(img_path, lang)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode()
    except Exception as e:
        print(e)
        return "[ERROR] Unable to process file: {0}".format(img_path)

    
    """
   
    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except Exception as e:
        print(e)
        #print(img_path)
        return "[ERROR] Unable to process file: {0}".format(img_path)
    

def get_shape(link):
    img = cv2.imread(link)
    dim = img.shape
    
    return dim