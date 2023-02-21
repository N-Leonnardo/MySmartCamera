import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time 
import datetime

class CameraApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Camera App")
        self.root.geometry("840x840")

        # Create the camera selection dropdown
        self.camera_dropdown = tk.StringVar(self.root)
        self.camera_dropdown.set("Built-in Camera")
        self.camera_options = ["Built-in Camera", "External Camera 1", "External Camera 2"]
        self.camera_dropdown_menu = tk.OptionMenu(self.root, self.camera_dropdown, *self.camera_options)
        self.camera_dropdown_menu.pack(pady=10)

        # Create the camera preview label
        self.camera_label = tk.Label(self.root)
        self.camera_label.pack()

        # Create the start/stop button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_camera)
        self.start_button.pack(side="left", padx=10, pady=10)

        # Create the quit button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_app)
        self.quit_button.pack(side="left", padx=10, pady=10)

        # Creates Detect Face
        # self.faces_button = tk.Button(self.button_frame, text="Detect Faces", command=self.camera)
        # self.faces_button.pack(side="left", padx=5, pady=5) 

        # Initialize the camera and preview image
        self.cap = None
        self.preview_timer = None
        self.preview_image = None

        self.root.mainloop()

    def start_camera(self):
        # Disable the camera selection dropdown and start button
        self.camera_dropdown_menu.config(state="disabled")
        self.start_button.config(state="disabled")

        # Get the camera index based on the selected dropdown item
        if self.camera_dropdown.get() == "Built-in Camera":
            camera_index = 0
        elif self.camera_dropdown.get() == "External Camera 1":
            camera_index = 1
        elif self.camera_dropdown.get() == "External Camera 2":
            camera_index = 2
        else:
            camera_index = 0

        # Open the selected camera
        # self.cap = cv2.VideoCapture(camera_index)

        self.cap = cv2.VideoCapture(1)

        # Check if the camera was successfully opened
        if not self.cap.isOpened():
            tk.messagebox.showwarning("Camera Error", "Unable to open camera")
            self.stop_camera()
            return

        self.preview_timer = self.root.after(0, self.update_preview)


    def update_preview(self):
        # Capture a frame from the camera
        ret, frame = self.cap.read()

        self.camera(frame)
        # Check if a frame was successfully captured
        if not ret:
            tk.messagebox.showwarning("Camera Error", "Unable to capture frame")
            self.stop_camera()
            return

        # Convert the frame to a PIL Image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Convert the PIL Image to a PhotoImage and set it as the camera preview label image
        photo = ImageTk.PhotoImage(image)
        self.camera_label.config(image=photo)
        self.camera_label.image = photo

        # Schedule the next preview update
        self.preview_timer = self.root.after(50, self.update_preview)

    def stop_camera(self):
        # Stop the camera preview timer
        if self.preview_timer is not None:
            self.root.after_cancel(self.preview_timer)
            self.preview_timer = None

        # Release the camera and clear the preview image
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self.preview_image = None

        # Clear the camera preview label image
        self.camera_label.config(image="")

        # Enable the camera selection dropdown and start button
        self.camera_dropdown_menu.config(state="normal")
        self.start_button.config(state="normal")

    def quit_app(self):
        # Stop the camera if it is running
        if self.cap is not None:
            self.stop_camera()

        # Close the application window
        self.root.destroy()

    def camera(self, frame):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

        recording = False
        detection_stopped_time = None
        timer_started = False
        SECONDS_TO_RECORD_AFTER_DETECTION = 5

        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")


        while True:

            _, frame = self.cap.read()

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
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = CameraApp()