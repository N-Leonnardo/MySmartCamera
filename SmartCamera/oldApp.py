import cv2
import time 
import datetime


def camera():
    cap = cv2.VideoCapture(1)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

    recording = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5

    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")


    while True:
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        bodies = body_cascade.detectMultiScale(gray, 1.3, 3)

        for (x,y,width, heigth) in faces:
            cv2.rectangle(frame, (x,y), (x + width, y + heigth), (255,0,0), 3)

        for (x,y,width, heigth) in bodies:
            cv2.rectangle(frame, (x,y), (x + width, y + heigth), (0,255,0), 3)


        if len(faces) + len(bodies) >  0:
            if recording:
                timer_started = False
            else:
                recording - True        
                recording = True
                currTime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(f"{currTime}.mp4", fourcc, 20, frame_size)
                print("REC")
        elif recording:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    recording = False
                    timer_started = False
                    out.release()
                    print("end Rec")
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if(recording):
            out.write(frame)

        cv2.imshow("Camera", frame)



        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()
