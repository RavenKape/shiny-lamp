from __future__ import unicode_literals
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserListView
from kivy.utils.platform import platform
from kivy.logger import Logger
from kivy.clock import mainthread
import time

def is_android():
	return platform == 'android'

def check_camera_permission():
	if not is_android():
		return True
	from android.permissions import Permission, check_permission
	permission = Permission.CAMERA
	return check_permission(permission)
	
def check_request_camera_permission(callback=None):
    had_permission = check_camera_permission()
    Logger.info("CameraAndroid: CAMERA permission {%s}.", had_permission)
    if not had_permission:
        Logger.info("CameraAndroid: CAMERA permission was denied.")
        Logger.info("CameraAndroid: Requesting CAMERA permission.")
        from android.permissions import Permission, request_permissions
        permissions = [Permission.CAMERA]
        request_permissions(permissions, callback)
        had_permission = check_camera_permission()
        Logger.info("CameraAndroid: Returned CAMERA permission {%s}.", had_permission)
    else:
        Logger.info("CameraAndroid: Camera permission granted.")
    return had_permission

		
Builder.load_string("""
<RoundSquare@Button>:
    background_color: 0,0,0,0  
    color: 1,1,0,1
    size: 150,150
    font_size: 60
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    canvas.before:
        Color:
            rgba: [0.3, 2.7, 0.3, 1] if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [25,]
 
<MainPage>:
    canvas.before:
        Rectangle:
            source: 'plantimage.jpg'
            pos: self.pos
            size: self.size
    FloatLayout:
        RoundSquare:
            text: 'Auto Detect'
            on_release: root.manager.current = 'detect'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.80,'right':0.45}
            Image:
            	source: 'cameraicon.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Manual Input'
            on_release: root.manager.current = 'manual'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.80,'right':0.90}
            Image:
                source: 'paperwrite.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-325
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Help'
            on_release: root.manager.current = 'help'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.40,'right':0.45}
            Image:
                source: 'questionmark.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Exit'
            on_release: app.stop()
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.40,'right':0.90}
            Image:
                source: 'exitimage.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
            	
<DetectPage>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: cam
            resolution: (480,640)
            play: True
            size_hint: 1,1
            allow_Stretch: True
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: 'Main Page'
            size_hint: 1, None
            height: '48dp'
            on_release: root.manager.current = 'main'
                     	
<ManualPage>:
    id: imageviewer
    BoxLayout:
        orientation: 'vertical'
        Image: 
            id: my_image
            source: ""
        FileChooserListView:
            id: imagechooser
            on_selection: imageviewer.selected(imagechooser.selection)
        Button:
            text: 'Main Page'
            size_hint: 1, 0.20
            on_release: root.manager.current = 'main'
           
<HelpPage>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Help Page'
        Button:
            text: 'Main Page'
            size_hint: 1, 0.10
            on_release: root.manager.current = 'main'
            
""")


# Declare screens
 
class MainPage(Screen):
    pass

class DetectPage(Screen):
    def capture(self):
    	print('Captured')
         
class ManualPage(Screen):
    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
        except:
            pass

class HelpPage(Screen):
    pass
           
class MainApp(App):
    def build(self): 	
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(DetectPage(name='detect'))
        sm.add_widget(ManualPage(name='manual'))
        sm.add_widget(HelpPage(name='help'))
        return sm
 
MainApp().run()
