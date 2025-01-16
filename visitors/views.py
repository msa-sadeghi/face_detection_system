import os
import face_recognition
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage

import cv2
import base64
import numpy as np
import json

import base64


import face_recognition
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Visitor

@csrf_exempt
def register_visitor(request):
    if request.method == 'POST':
        
        try:
            # دریافت داده‌های JSON
            
            data = json.loads(request.body)
            
            name = data.get('name')
            # contact = request.POST['contact']
            contact = "12345"
            image_data = data.get('image_data')
            print("*****************", name, image_data)
            if not name or not image_data:
                return JsonResponse({'status': 'error', 'message': 'Name or image data is missing.'})

            # پردازش تصویر
            image_data = image_data.split(',')[1]  # جدا کردن بخش base64
            image_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # استخراج encoding چهره
            face_encodings = face_recognition.face_encodings(image)

            if len(face_encodings) == 0:
                return JsonResponse({'status': 'error', 'message': 'No face detected in the image.'})

            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                encoding_str = ','.join(map(str, encoding))

            
            # ذخیره تصویر, 
            visitor_image_path = f'visitor_images/{name}.jpg'
            cv2.imwrite(f'media/{visitor_image_path}', image)

            # ذخیره در پایگاه داده
            Visitor.objects.create(
                name=name,
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



def identify_visitor(request):
    
    if request.method == 'POST':
        
        # دریافت تصویر به صورت base64
    
        data = json.loads(request.body)  # دریافت داده‌های JSON
        image_data = data.get('image_data')  # استخراج image_data
          # بررسی داده‌های POST
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # تبدیل تصویر به فرمت NumPy
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # استخراج encoding چهره
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            uploaded_encoding = face_encodings[0]

            # مقایسه با داده‌های پایگاه داده
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

