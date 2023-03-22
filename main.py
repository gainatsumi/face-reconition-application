#Thêm thư viện tkinter
import tkinter as tk
#thêm module từ thư viện tkinter
from tkinter import filedialog as fd
#thêm module từ thư viẹn PIL
from PIL import ImageTk, Image
#thêm thư viện cv2 
import cv2

#thêm module predic gồm hàm predic_function và to_class
from source.predic import predic
#them module detect_face gôm hàm get_position, crop_face
from source.detect_face import detect_face


#Tạo một cửa sổ mới
window = tk.Tk()

#Tạo biến chứa đường dẫn
path= ""

#Tạo biến chỉ vị trí face trong array face
k = 0

#tạo array chứa face tìm được
faces = []
faces_array = []

#Hàm reset: dùng để reset lại tất cả thuộc tính khi thay đổi ảnh input
def reset():
    global path, k, faces, gender_label, face_label
    path= ""
    k = 0
    faces = []
    gender_label.configure(text = "Gender: ")
    face_label.configure(text ="Face: "  + str(len(faces))) 

#hàm use_camera: dùng để mở camera bằng thư viện openCV
def use_camera():
    global path
    reset()

    #khơi động camera
    cap = cv2.VideoCapture(0)

    #vòng lặp viết frame liên tục của camera
    while True:
        #lấy từng frame từ cam
        ret, frame = cap.read()

        #show frame
        cv2.imshow('camera', frame) 

        #nhấn q để tắt camera       
        if cv2.waitKey(1) == ord('q'):

            #lưu frame cuối cùng vào thư mục "Camera/image.jpg"
            cv2.imwrite("Image/image.jpg", frame)

            #hủy của sổ camera
            cv2.destroyWindow("camera")
            break

    #đặt lại đường dẫn đến bức ảnh vừa chụp
    path = "Image/image.jpg"

    #hiện ảnh trên app theo đường dẫn đã chụp
    display_picture(path)

#hàm use_file: từ thư viện tkinter lấy module filedialog để hỏi người dùng lấy ảnh từ file 
def use_file():
    global path
    
    #reset biến
    reset()
    
    #lấy đường dẫn theo người dùng chỉ
    path = fd.askopenfilename()

    if (path == ""):
        path = "Image/error.jpg"

    #hiện ảnh theo đường dẫn vauwf lấy
    display_picture(path)

#hàm display_picture: hiện ảnh trên app
def display_picture(path):
    global faces, faces_array, df

    #lấy ảnh theo đường dẫn
    image = Image.open(path)

    #resize lại ảnh để phù hợp kích thước app
    if (image.width > 350):
        dim =  [350, round(image.height*(350/image.width))]
    elif(image.height > 500):
        dim =  [round(image.width*(500/image.height)), 500]
    else:
        dim = [image.width, image.height]

    resized = image.resize(dim)
    
    # convert ảnh sang dạng phù hợp tkinter
    tk_image = ImageTk.PhotoImage(resized)

    # hiện ảnh trên 1 label
    image_label.configure(image=tk_image)
    image_label.image = tk_image  
    faces_array =  []
    #lấy tập face sau khi detect face
    faces = df.detect(path)
    path = "Image/image.jpg"

    #hiện từng face đã tìm thấy
    display_face()

    #hiện số lượng face có thể tìm thấy được
    if(len(faces) <= 0):
        face_label.configure(text ="can found any face") 
    else:
        face_label.configure(text ="Face: "  + str(len(faces))) 


#hàm next_face: gán button ">" chọn face tiếp theo trong trường hợp tìm đc nhiều face
def next_face():
    global k, faces
    print(k)
    if k < len(faces) - 1:
        k +=1
    else:
        k = 0
    display_face()

#hàm next_face: gán button "<" chọn face trước đó trong trường hợp tìm đc nhiều face
def prev_face():
    global k, faces
    print(k)
    if k > 0:
        k -=1
    else:
        k = len(faces) - 1
    display_face()

def  rotate_l():
    global path
    image = cv2.imread(path)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    path = "Image/image.jpg"
    cv2.imwrite("Camera/image.jpg", image)
    display_picture(path)

def rotate_r():
    global path
    image = cv2.imread(path)
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    path = "Image/image.jpg"
    cv2.imwrite("Camera/image.jpg", image)
    display_picture(path)
    

#hàm predic_gender: dự đoán giới tính
def predic_gender():
    global  path, gender_label, faces, k, pr, df
    #check nếu tập faces bị rỗng hay không
    if(len(faces) > 0):
        #lấy tọa độ face
        x, y, w, h = faces[k]

        #lấy nguyên face
        img = df.crop_face(x, y, w, h, path)

        #check nếu face bị rỗng
        if (img is not None):

            #dùng module để dự đoán
            prediced = pr.to_class(img)

            #lấy class đã được dự đoán
            predic_class = str(prediced[0])

            #in dự đoán ra code
            gender_label.configure(text = "Gender: " + predic_class)            
        else:
            #nếu không tìn thấy mặt thoát hàm
            return
    else:
        #nếu faces rỗng thì in thông báo
        face_label.configure(text ="can found any face") 


#hàm display_face: dùng để in khuôn mặt ra vị trí riêng
def display_face():
    global path, faces, k

    #check nếu tập faces bị rỗng hay không
    if (len(faces) > 0):
        #mở ảnh
        img = Image.open(path)
        #lấy vị trí face
        x, y, w, h = faces[k]
        #cắt ảnh
        img = img.crop([x, y, x+w, y+h])
        #resize ảnh về 96, 96 
        img= img.resize((128, 128), Image.ANTIALIAS)
        #gán ảnh
        face_image = ImageTk.PhotoImage(img)
        
        # display ảnh trên label
        image_face_label.configure(image=face_image)
        image_face_label.image = face_image  


if __name__ == '__main__':
    df = detect_face()
    pr = predic()

    #Thêm tiêu đề cho cửa sổ
    window.title('detect gender app')

    #Đặt kích thước của cửa sổ
    window.geometry('510x500')
    #hạn chế thay đổi kích thước cửa sổ app
    window.resizable(width=False, height=False)

    #label ảnh chính
    image_label = tk.Label(window)
    image_label.place(x=150, y = 20)

    #label ảnh face
    image_face_label = tk.Label(window)
    image_face_label.place(x = 5, y = 230)

    #label text dự đoán gender
    gender_label = tk.Label(window, text = "Gender: ")
    gender_label.place(x=5, y = 170)

    #label text số face tìm được
    face_label = tk.Label(window, text = "Face: ")
    face_label.place(x=5, y = 140)

    #nút bật camera
    camera_button = tk.Button(window, text = "Open camera", command=use_camera)
    camera_button.place(x=5, y = 50)

    #nút lấy ảnh từ file
    path_button = tk.Button(window, text = "Open file", command=use_file)
    path_button.place(x=5, y = 20)

    #nút dự đoán face được chọn
    predic_button = tk.Button(window, text = "Predic", command=predic_gender)
    predic_button.place(x=5, y = 110)

    #nút chuyển face trái và phải
    left_button = tk.Button(window, text = "<", command = next_face)
    left_button.place(x = 5, y = 200)

    right_button = tk.Button(window, text = ">", command = prev_face)
    right_button.place(x = 30, y = 200)

    #nút chuyển face trái và phải
    rotate_l_button = tk.Button(window, text = "<", command = rotate_l)
    rotate_r_button = tk.Button(window, text = ">", command = rotate_r)
    rotate_l_button.place(x = 5, y = 80)
    rotate_r_button.place(x = 30, y = 80)












#Lặp vô tận để hiển thị cửa sổ
window.mainloop()
