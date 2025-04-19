import re
import json
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from kivy.app import App, Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen


class lecscan(App):
    def build(self):
        self.title = "Lecture Scanner"

        layout = BoxLayout(orientation='vertical')
        return layout
    

    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.process_image)
        popup = Popup(title="Select Image", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def process_image(self, instance, selection, touch):
        if selection:
            image_path = selection[0]
            self.label_output.text = "Processing..."
            self.scan_image(image_path)

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

        # Handle account creation logic here
        print(f"Account created for {username} with email {email}")

    def go_back(self, instance):
        self.manager.current = "main"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = Image(source="lecscanlogo1.jpg")
        layout.add_widget(logo)

        # Add a welcome label
        layout.add_widget(Label(text="Welcome to Lecture Scanner", size_hint=(1, 0.1)))

        # Add a button to go to the Create Account screen
        btn_create_account = Button(text="Create Account", size_hint=(1, 0.1), background_color=[0.2, 0.8, 0.2, 1])
        btn_create_account.bind(on_press=self.go_to_create_account)
        layout.add_widget(btn_create_account)

        self.add_widget(layout)

    def go_to_create_account(self, instance):
        self.manager.current = "create_account"


class lecscan(App):
    def build(self):
        self.title = "Lecture Scanner"
        Window.size = (360, 640)

        # Create the ScreenManager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(CreateAccountScreen(name="create_account"))

        return sm

def save_user_data(username, email, password):
    user_data = {"username": username, "email": email, "password": password}
    with open("users.json", "a") as file:
        file.write(json.dumps(user_data) + "\n")

def submit_account(self, instance):
    username = self.username_input.text
    email = self.email_input.text
    password = self.password_input.text

    if not is_valid_email(email):
        self.error_label.text = "Invalid email address. Please try again."
        return

    save_user_data(username, email, password)
    print(f"Account created for {username} with email {email}")


def is_valid_email(email):
    # Regex pattern for validating email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


if __name__ == '__main__':

    Window.size = (360, 640)

    try:
        lecscan().run()
    except Exception as e:
        print(f"An error occurred: {e}")
