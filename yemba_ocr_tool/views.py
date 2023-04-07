# -*- coding: utf-8 -*-
import pytesseract
import os, shutil
from django.shortcuts import render
from django.http import HttpResponse

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

        myfile = 'images/'+ str(uploaded_file)
        
        
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
    Performs OCR on a single image

    :img_path: str, path to the image file
    :lang: str, language to be used while conversion (optional, default is english)

    Returns
    :text: str, converted text from image
    """
    


    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)

