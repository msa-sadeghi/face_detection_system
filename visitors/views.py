import os
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import cv2
import base64
import numpy as np
import json

import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Visitor

# @csrf_exempt
@login_required
def register_visitor(request):
    if request.method == 'POST':
        
        try:
            # receive JSON data
            
            data = json.loads(request.body)
            
            name = data.get('name')
            family = data.get('family')
            nationalCode = data.get('nationalCode')
            company = data.get('company')
            contact = data.get('contact')
            image_data = data.get('image_data')
            
            if not name or not image_data:
                return JsonResponse({'status': 'error', 'message': 'Name or image data is missing.'})

            # image processing
            image_data = image_data.split(',')[1]  # جدا کردن بخش base64
            image_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # extract face encodings
            face_encodings = face_recognition.face_encodings(image)

            if len(face_encodings) == 0:
                return JsonResponse({'status': 'error', 'message': 'No face detected in the image.'})

            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                encoding_str = ','.join(map(str, encoding))

            
            # save image 
            visitor_image_path = f'visitor_images/{name}.jpg'
            cv2.imwrite(f'media/{visitor_image_path}', image)

            # save in database
            Visitor.objects.create(
                name=name,
                family = family,
                nationalCode = nationalCode,
                company = company,
                contact = contact,
                photo=visitor_image_path,
                face_encoding=encoding_str
            )

        #     return JsonResponse({'status': 'success', 'message': 'Visitor registered successfully!'})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({'status': 'error', 'message': 'An error occurred while registering the visitor.'})

    # return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    return render(request, 'register.html')


@login_required
def identify_visitor(request):
    if not request.user.is_authenticated:
        return redirect("user:login")
    if request.method == 'POST':
        
        # receive data in base 64 format
    
        data = json.loads(request.body)  # receive JSON data
        image_data = data.get('image_data')  # extract image_data
          # verify post data
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # convert image to numpy
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # extract face encoding
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            uploaded_encoding = face_encodings[0]

            # compare with database data
            visitors = Visitor.objects.all()
            for visitor in visitors:
                saved_encoding = list(map(float, visitor.face_encoding.split(',')))
                matches = face_recognition.compare_faces([saved_encoding], uploaded_encoding)

                if matches[0]:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Visitor identified!',
                        'data': {
                            'name': visitor.name,
                            'contact': visitor.contact
                        }
                    })

            return JsonResponse({'status': 'error', 'message': 'Visitor not recognized.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'No face detected. Please try again.'})

    return render(request, 'identify.html')

