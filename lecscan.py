import re
import json
import pytesseract
from PIL import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image as KivyImage
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import platform
if platform.system() == 'Android':
    from android.permissions import request_permissions, Permission
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

Window.clearcolor = (1, 1, 1, 1)


class lecscan(App):
    def build(self):
        self.title = "Lecture Scanner"
        Window.size = (360, 640)

        # Create the ScreenManager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(CreateAccountScreen(name="create_account"))
        sm.add_widget(Scanner(name="scanner"))

        return sm


class CreateAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Add input fields for account creation
        self.username_input = TextInput(hint_text="Enter Username", size_hint=(1, 0.1))
        self.email_input = TextInput(hint_text="Enter Email", size_hint=(1, 0.1))
        self.password_input = TextInput(hint_text="Enter Password", password=True, size_hint=(1, 0.1))

        layout.add_widget(Label(text="Create an Account", size_hint=(1, 0.1)))
        layout.add_widget(self.username_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        # Add an error label
        self.error_label = Label(text="", color=[1, 0, 0, 1], size_hint=(1, 0.1))  # Red text for errors
        layout.add_widget(self.error_label)

        # Add a button to submit the form
        btn_submit = Button(text="Submit", size_hint=(1, 0.1), background_color=[0.2, 0.8, 0.2, 1])
        btn_submit.bind(on_press=self.submit_account)
        layout.add_widget(btn_submit)

        # Add a button to go back to the main screen
        btn_back = Button(text="Back", size_hint=(1, 0.1), background_color=[0.8, 0.2, 0.2, 1])
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def submit_account(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not is_valid_email(email):
            self.error_label.text = "Invalid email address. Please try again."
            return

        save_user_data(username, email, password)
        print(f"Account created for {username} with email {email}")

    def go_back(self, instance):
        self.manager.current = "main"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = KivyImage(source="lecscanlogo1.jpg")
        layout.add_widget(logo)

        # Add a welcome label
        layout.add_widget(Label(text="Welcome to Lecture Scanner", size_hint=(1, 0.1), color=[0, 0, 0, 1]))

        # Add a button to go to the Create Account screen
        btn_create_account = Button(text="Create Account", size_hint=(1, 0.1), background_color=[0.2, 0.8, 0.2, 1])
        btn_create_account.bind(on_press=self.go_to_create_account)
        layout.add_widget(btn_create_account)

        # Add a button to go to the Scanner screen
        btn_developer_mode = Button(text="Developer Mode", size_hint=(1, 0.1), background_color=[0, 0, 0, 0], color=[0, 0, 1, 1])
        btn_developer_mode.bind(on_press=self.go_to_scanner)
        layout.add_widget(btn_developer_mode)

        self.add_widget(layout)

    def go_to_create_account(self, instance):
        self.manager.current = "create_account"

    def go_to_scanner(self, instance):
        self.manager.current = "scanner"


class Scanner(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        try:
            # Add a Camera widget
            self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.8))
            layout.add_widget(self.camera)
        except Exception as e:
            layout.add_widget(Label(text=f"Camera not available: {e}", size_hint=(1, 0.8)))

        # Add a button to capture the image
        btn_capture = Button(text="Capture", size_hint=(1, 0.1), background_color=[0.2, 0.8, 0.2, 1])
        btn_capture.bind(on_press=self.capture_image)
        layout.add_widget(btn_capture)

        # Add a label to display the OCR result
        self.label_output = Label(text="Select an image to scan", size_hint=(1, 0.1))
        layout.add_widget(self.label_output)

        # Add a button to open the file chooser
        btn_choose_file = Button(text="Choose Image", size_hint=(1, 0.1), background_color=[0.2, 0.8, 0.2, 1])
        btn_choose_file.bind(on_press=self.open_file_chooser)
        layout.add_widget(btn_choose_file)

        # Add a back button to return to the main screen
        btn_back = Button(text="Back", size_hint=(1, 0.1), background_color=[0.8, 0.2, 0.2, 1])
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def open_file_chooser(self, instance):
        try:
            popup = Popup(title="Choose an Image", size_hint=(0.9, 0.9))
            filechooser = FileChooserIconView()
            filechooser.bind(on_submit=self.file_selected)
            popup.content = filechooser
            popup.open()
        except Exception as e:
            self.label_output.text = f"Error: {e}"

    def file_selected(self, instance, selection):
        if selection:
            self.scan_image(selection[0])

    def scan_image(self, image_path):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            self.label_output.text = text
        except Exception as e:
            self.label_output.text = f"Error: {e}"

    def capture_image(self, instance):
        try:
            # Save the current frame from the camera
            image_path = "captured_image.jpg"
            self.camera.export_to_png(image_path)

            # Process the image with Tesseract OCR
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)

            # Display the extracted text
            self.label_output.text = text
        except Exception as e:
            self.label_output.text = f"Error: {e}"
 
    def go_back(self, instance):
            # Navigate back to the main screen
            self.manager.current = "main"


def save_user_data(username, email, password):
    user_data = {"username": username, "email": email, "password": password}
    with open("users.json", "a") as file:
        file.write(json.dumps(user_data) + "\n")


def is_valid_email(email):
    # Regex pattern for validating email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


if __name__ == '__main__':
    try:
        lecscan().run()
    except Exception as e:
        print(f"An error occurred: {e}")
