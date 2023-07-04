import os
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
import xlwt as xlwt
from django.contrib import messages
from django.core.paginator import Paginator
import ssl
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.shortcuts import render
from email.message import EmailMessage
from .models import Camera, Warning
import playsound
import threading
from django.db.models import Q
import numpy as np
import tensorflow as tf



# cnn_model = tf.keras.models.load_model('G:/django/demo/realcam/fire_detection_model.h5')
def preprocess_image(image):
    # Resize image to match the input size of the CNN model
    resized_image = cv2.resize(image, (224, 224))
    # Normalize pixel values to the range [0, 1]
    normalized_image = resized_image / 255.0
    # Expand dimensions to create a batch of size 1 (required by the CNN model)
    preprocessed_image = np.expand_dims(normalized_image, axis=0)
    return preprocessed_image

# def predict_fire(image):
#     # prediction = cnn_model.predict(image)
#     # return prediction[0][0]

def detect_fire_red(frame,camera_id):
    max_emails = 10  # giới hạn số lượng email gửi đi
    sent_emails = 0
    runOnce = False
    v_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    v_ycbcr = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

    y = v_ycbcr[:, :, 0]
    cr = v_ycbcr[:, :, 1]
    cb = v_ycbcr[:, :, 2]

    # Áp dụng ngưỡng cho YCbCr
    ycrcb_mask_cr = cv2.threshold(cr, 135, 255, cv2.THRESH_BINARY)[1]
    ycrcb_mask_y = cv2.threshold(y, 180, 255, cv2.THRESH_BINARY)[1]
    ycrcb_mask_cb_cr = cv2.bitwise_and(ycrcb_mask_cr, cv2.threshold(cb, 156, 255, cv2.THRESH_BINARY)[1])
    ycrcb_mask = cv2.bitwise_and(ycrcb_mask_y, ycrcb_mask_cb_cr)

    # Áp dụng ngưỡng cho HSV
    hsv_mask = cv2.inRange(v_hsv, (0, 150, 150), (30, 255, 255))

    # Kết hợp kết quả từ YCbCr và HSV
    fire_mask_red = cv2.bitwise_or(ycrcb_mask, hsv_mask)

   # Áp dụng morphology để tách lửa ra khỏi nhiễu và các vật thể khác
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fire_mask_red = cv2.morphologyEx(fire_mask_red, cv2.MORPH_OPEN, kernel)
    fire_mask_red = cv2.morphologyEx(fire_mask_red, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(fire_mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        area = cv2.contourArea(contour)
        if area > 500:

            # total_pixel_fire += area
            x, y, w, h = cv2.boundingRect(contour)
            region = frame
            # Tiền xử lý ảnh trước khi đưa vào mô hình CNN
            preprocessed_image = preprocess_image(region)
            # Dự đoán xem vùng chứa lửa có chứa lửa hay không bằng mô hình CNN
            # prediction = predict_fire(preprocessed_image)
            # if prediction > 0.2:  # Adjust the threshold as needed
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # if cv2.mean(fire_mask_red[y:y + h, x:x + w])[0] > 100:
            cv2.putText(frame, "Fire!", (250, 120), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)


            # threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread



            if runOnce == False:
                    camera = Camera.objects.get(id=camera_id)
                    users = User.objects.get(id=camera.user.id)

                    current_time = datetime.now().strftime("%c")
                    warning = Warning(location=camera, user=users, time=current_time)
                    warning.save()

                    count = 1
                    while os.path.exists(rf'G:\django\demo\media\warning_images\image_{count}.jpg'):
                        count += 1
                    frame_with_fire = frame  # Khung hình chứa cháy
                    image_filename = rf"G:\django\demo\media\warning_images\image_{count}.jpg"
                    cv2.imwrite(image_filename, frame_with_fire)
                    warning.image = image_filename
                    warning.save()

                    threading.Thread(target=send_mail_function(email_receiver= users.email, subject = 'FIRE WAS DETECT!!',body = 'A fire has been detected at ' +str(camera.name) +' at ' +str(current_time), image_path=warning.image.path)).start()  # To call alarm thread
                    runOnce = True
                    sent_emails +=1
                    if sent_emails >= max_emails:
                        break


#canh bao bang am thanh
def play_alarm_sound_function():
    playsound.playsound(r'G:\django\demo\realcam\fire_alarm.mp3',True)



def send_mail_function(email_receiver,subject, body,image_path):
    # camera = Camera.objects.get(id=camera_id)
    # user = User.objects.get(id=camera.user.id)

    user = User.objects.filter(email=email_receiver).first()
    email_sender = 'toan85173@st.vimaru.edu.vn'
    email_password = 'sewyndgbcijsfhfq'
    # email_receiver = 'toanminhp06@gmail.com'
    # email_receiver = user.email

    # body = 'A fire has been detected at your location'

    em = MIMEMultipart()
    # em = EmailMessage()
    em['From'] = email_sender
    em['To'] = user.email
    em['Subject'] = subject
    # em.set_content(body)

    context = ssl.create_default_context()

    with open(image_path, 'rb') as fp:
        img = MIMEImage(fp.read())

        # Đặt loại MIME của hình ảnh
    img.add_header('Content-Disposition', 'attachment', filename='warning_image.jpg')
    img.add_header('Content-Type', 'image/jpeg')  # Thay 'image/jpeg' bằng loại MIME tương ứng của hình ảnh
    em.attach(img)

    # Thêm nội dung email
    em.attach(MIMEText(body))
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

@login_required(login_url="/login/")
def warning(request):
    warning_form = Warning.objects.filter(user = request.user)
    paginator = Paginator(warning_form, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'realcam/warning_list.html',{'warning_form':page_obj})



def warnings_search(request):
    if request.method == 'GET':
        query = request.GET.get('q','')
        sort_param = request.GET.get('sort')
        warnings = Warning.objects.filter(user=request.user)
        if query:
            warnings = warnings.filter(
                Q(user__email__icontains=query) |
                Q(time__icontains=query) |
                Q(location__name__icontains=query)
            )
        if sort_param == 'date':
            warnings = warnings.order_by('-time')

        paginator = Paginator(warnings,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'warning_form': page_obj
        }
        return render(request, 'realcam/warning_list.html', context)

def delete_warning(request, warning_id):
    if request.method == 'POST':
        warning = Warning.objects.filter(id=warning_id)
        if warning:
            warning.delete()
            return redirect('realcam:warning')
        else:
            return render(request, 'error.html', {'message': 'Camera not found'})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})

def export_warnings_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Warning.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Warning')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Email Receive', 'Date', 'Location']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    warnings = Warning.objects.filter(user=request.user)
    for warning in warnings:
        row_num += 1
        email = warning.user.email
        time = warning.time.strftime('%Y-%m-%d %H:%M:%S')
        location = warning.location.name
        row = [email, time, location]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response

@login_required(login_url="/login/")
def index(request):
    camera_form = Camera.objects.filter(user = request.user)
    return render(request, 'realcam/video.html',{'camera_form':camera_form})

@login_required(login_url="/login/")
def add_video(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        user_id = request.user.id
        camera = Camera(name=name, url=url, user_id=user_id)
        camera.save()
        return redirect('realcam:index')
    return render(request, 'realcam/add_video.html')




def delete_camera(request, camera_id):
    if request.method == 'POST':
        camera = Camera.objects.filter(id=camera_id)
        if camera:
            camera.delete()
            return redirect('realcam:index')
        else:
            return render(request, 'error.html', {'message': 'Camera not found'})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})


def video_feed(camera_id):

    camera = Camera.objects.get(id=camera_id)
    user = User.objects.get(id=camera.user_id)


    if camera.url == '0':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(f'{camera.url}')
    # cap = cv2.VideoCapture(r"C:\Users\Admin\Desktop\fire_detection_hsv2\test he thong\chaycay2.mp4")

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        detect_fire_red(frame,camera_id)




        ret, jpeg = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@gzip.gzip_page
def live_camera(request, camera_id):

    return StreamingHttpResponse(video_feed(camera_id), content_type="multipart/x-mixed-replace;boundary=frame")





