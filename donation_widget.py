from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from pathlib import Path
import os

# Colors from the image
TEAL_COLOR = (26/255, 164/255, 159/255, 1)  # #1AA49F
WHITE_COLOR = (1, 1, 1, 1)
DARK_TEXT_COLOR = (0.2, 0.2, 0.2, 1)
LIGHT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)

class DonationWidget(BoxLayout):
    """Widget displaying a donation option exactly as shown in the image"""
    def __init__(self, image_source, title, on_donate_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(380)  # Total height to accommodate all elements including message
        self.padding = [dp(15), dp(15), dp(15), dp(15)]
        self.spacing = dp(10)
        
        # Store the callback
        self.on_donate_callback = on_donate_callback
        self.title_text = title
        self.image_source = image_source
        
        # Main container with white background and rounded corners
        self.container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(350),
            padding=[dp(0), dp(0), dp(0), dp(0)],
            spacing=dp(5)
        )
        
        # Add white background with rounded corners
        with self.container.canvas.before:
            Color(*WHITE_COLOR)
            self.bg = RoundedRectangle(
                pos=self.container.pos,
                size=self.container.size,
                radius=[dp(10), dp(10), dp(10), dp(10)]
            )
        self.container.bind(pos=self._update_bg, size=self._update_bg)
        
        # Image at the top (using exact proportions from your image)
        self.image = Image(
            source=image_source,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, None),
            height=dp(190)
        )
        self.container.add_widget(self.image)
        
        # Title with proper styling
        self.title = Label(
            text=title,
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            bold=True,
            halign='center',
            valign='center',
            size_hint=(1, None),
            height=dp(50)
        )
        self.container.add_widget(self.title)
        
        # Thank you message
        self.message = Label(
            text="Your help through this donation makes this possible — thank you so much for supporting the project!",
            font_size=sp(14),
            color=LIGHT_TEXT_COLOR,
            halign='center',
            valign='top',
            size_hint=(1, None),
            height=dp(60),
            text_size=(dp(280), None)
        )
        self.container.add_widget(self.message)
        
        # Button container for centering
        button_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(20), dp(0), dp(20), dp(10)]
        )
        
        # Donate button with teal background
        self.donate_button = Button(
            text="Donate",
            font_size=sp(16),
            background_normal='',
            background_color=TEAL_COLOR,
            color=WHITE_COLOR,
            size_hint=(None, None),
            size=(dp(120), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add rounded corners to button
        with self.donate_button.canvas.before:
            Color(*TEAL_COLOR)
            self.button_bg = RoundedRectangle(
                pos=self.donate_button.pos,
                size=self.donate_button.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.donate_button.bind(pos=self._update_button_bg, size=self._update_button_bg)
        self.donate_button.bind(on_press=self._on_donate)
        
        # Add left spacer, button, right spacer to center the button
        button_container.add_widget(Widget(size_hint=(0.5, 1)))
        button_container.add_widget(self.donate_button)
        button_container.add_widget(Widget(size_hint=(0.5, 1)))
        
        self.container.add_widget(button_container)
        
        # Add the container to the main layout
        self.add_widget(self.container)
    
    def _update_bg(self, instance, value):
        """Update background when size changes"""
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def _update_button_bg(self, instance, value):
        """Update button background when size changes"""
        self.button_bg.pos = instance.pos
        self.button_bg.size = instance.size
    
    def _on_donate(self, instance):
        """Handle donate button press"""
        if self.on_donate_callback:
            self.on_donate_callback(self.image_source, self.title_text)
        else:
            print(f"Donate button pressed for: {self.title_text}")


# Demo usage of the widget
if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.scrollview import ScrollView
    
    class DonationWidgetDemoApp(App):
        def build(self):
            scroll_view = ScrollView(do_scroll_x=False)
            container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing=dp(20),
                padding=[dp(10), dp(20), dp(10), dp(20)]
            )
            container.bind(minimum_height=container.setter('height'))
            
            # Path to assets
            assets_path = Path(__file__).parent / Path(r"build\assets\frame7")
            
            # Computer labs donation widget
            computer_labs_image = os.path.join(assets_path, "image_3.png")
            computer_labs_widget = DonationWidget(
                computer_labs_image,
                "Donate for Computer Labs",
                on_donate_callback=self.on_donate
            )
            container.add_widget(computer_labs_widget)
            
            # Infrastructure donation widget
            infrastructure_image = os.path.join(assets_path, "image_5.png")
            infrastructure_widget = DonationWidget(
                infrastructure_image,
                "Donate for Infrastructure",
                on_donate_callback=self.on_donate
            )
            container.add_widget(infrastructure_widget)
            
            scroll_view.add_widget(container)
            return scroll_view
        
        def on_donate(self, image_source, title):
            print(f"Donation for {title} requested")
            
    DonationWidgetDemoApp().run()
