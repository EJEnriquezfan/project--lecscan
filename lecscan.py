import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class lecscan(App):
    def build(self):
        self.title = "Lecture Scanner"

        layout = BoxLayout(orientation='vertical')

        self.btn_open = Button(text="Select Image", size_hint=(1, 0.1))
        self.btn_open.bind(on_press=self.open_file_chooser)

        self.label_output = Label(text="Scanning Lecture", size_hutn=(1, 0.1))

        layout.add_widget(self.btn_open)
        layout.add_widget(self.label_output)

        return layout
    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.process_image)
        popup = Popup(title="Select Image", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()


if __name__ == '__main__':
    lecscan().run()
