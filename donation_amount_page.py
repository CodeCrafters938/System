from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.widget import Widget
from pathlib import Path
import os

# Device profile constants
DEVICE_PROFILES = {
    'small': {'width': 392, 'height': 759},
    'medium': {'width': 1080, 'height': 2340},
}

# For mobile devices, let the system set the window size
if platform not in ('android', 'ios'):
    Window.size = (DEVICE_PROFILES['small']['width'], DEVICE_PROFILES['small']['height'])

# Colors from the image
TEAL_COLOR = (26/255, 164/255, 159/255, 1)  # #1AA49F
WHITE_COLOR = (1, 1, 1, 1)
GRAY_COLOR = (0.9, 0.9, 0.9, 1)
DARK_TEXT_COLOR = (0.2, 0.2, 0.2, 1)
LIGHT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)

# Path to assets
ASSETS_PATH = Path(__file__).parent / Path(r"build\assets\frame9")
NAVIGATION_ICONS_PATH = Path(__file__).parent / Path(r"navigation_icons")

# Create navigation_icons directory if it doesn't exist
if not os.path.exists(NAVIGATION_ICONS_PATH):
    os.makedirs(NAVIGATION_ICONS_PATH)

class HeaderBar(BoxLayout):
    """Teal header bar with school name"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        
        # Background color
        with self.canvas.before:
            Color(*TEAL_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Left - School logo
        logo_path = os.path.join(ASSETS_PATH, "image_1.png")
        self.logo = Image(
            source=logo_path if os.path.exists(logo_path) else "",
            size_hint=(None, 1),
            width=dp(50),
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.logo)
        
        # Center - Donate title
        self.title = Label(
            text="Donate",
            font_size=sp(22),
            color=WHITE_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            bold=True
        )
        self.add_widget(self.title)
        
        # Right spacer to balance the logo
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        self.add_widget(spacer)
    
    def _update_rect(self, instance, value):
        """Update background when size changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size

class AmountButton(Button):
    """Button for selecting a donation amount"""
    def __init__(self, amount, **kwargs):
        self.amount_value = amount
        text = f"₱{amount}"
        super().__init__(text=text, **kwargs)
        self.font_size = sp(18)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)  # White background
        self.color = DARK_TEXT_COLOR
        
        # Add border to button - renamed border to border_rect to avoid conflicts
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray border
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.bind(pos=self._update_border, size=self._update_border)
    
    def _update_border(self, instance, value):
        """Update border when position or size changes"""
        self.border_rect.pos = instance.pos
        self.border_rect.size = instance.size
    
    def select(self):
        """Highlight this button when selected"""
        # Clear previous instructions first
        self.canvas.before.clear()
        
        # Add new instructions
        with self.canvas.before:
            Color(*TEAL_COLOR)
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.color = TEAL_COLOR
    
    def deselect(self):
        """Remove highlight when not selected"""
        # Clear previous instructions first
        self.canvas.before.clear()
        
        # Add new instructions
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray border
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.color = DARK_TEXT_COLOR

class EmptyNavigationBar(BoxLayout):
    """Navigation bar with 5 empty slots ready to be populated"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(5), dp(5), dp(5), dp(5)]
        
        # Background color
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(0.9, 0.9, 0.9, 1)  # Light gray top border
            self.border = Line(points=[0, 0, 0, 0], width=1)
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        
        # Store reference to slots
        self.slots = []
        
        # Create 5 empty slots
        for i in range(5):
            slot = BoxLayout(orientation='vertical', size_hint=(1, 1))
            self.add_widget(slot)
            self.slots.append(slot)
    
    def add_icon_to_slot(self, slot_index, icon_source, text, icon_size=None, icon_pos_y=0.5):
        """Add an icon and text to a specific slot"""
        if 0 <= slot_index < len(self.slots):
            # Clear any existing content in the slot
            self.slots[slot_index].clear_widgets()
            
            # Create vertical layout for the icon and text
            content_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
            
            # Default icon size
            if icon_size is None:
                icon_size = (dp(30), dp(30))
            
            # Add icon with adjustable vertical position
            icon = Image(
                source=icon_source,
                size_hint=(None, None),
                size=icon_size,
                pos_hint={'center_x': 0.5, 'center_y': icon_pos_y}
            )
            
            # Add icon container with increased height for more room
            icon_container = FloatLayout(size_hint=(1, None), height=dp(45))
            icon_container.add_widget(icon)
            
            # Add text with adjusted position
            text_label = Label(
                text=text,
                font_size=sp(12),
                size_hint=(1, None),
                height=dp(15),
                halign='center',
                padding=(0, dp(-8))
            )
            
            # Add widgets to content layout
            content_layout.add_widget(icon_container)
            content_layout.add_widget(text_label)
            
            # Add content layout to slot
            self.slots[slot_index].add_widget(content_layout)
    
    def _update_canvas(self, instance, value):
        """Update background and border when size changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.points = [
            self.x, self.y + self.height - 1, 
            self.x + self.width, self.y + self.height - 1
        ]

class DonationAmountContent(BoxLayout):
    """Content area for donation amount selection page"""
    def __init__(self, image_path, title, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(5), dp(15), dp(10)]
        self.spacing = dp(8)
        
        self.selected_amount = None
        self.custom_amount = None
        
        # Back button at the top-left with teal color
        self.back_btn = Button(
            text="< Back",
            font_size=sp(18),
            color=TEAL_COLOR,
            background_color=(0, 0, 0, 0),  # Transparent background
            size_hint=(None, None),
            size=(dp(80), dp(30)),
            pos_hint={'x': 0},
            halign='left'
        )
        self.back_btn.bind(on_press=self.on_back)
        
        back_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40)
        )
        back_container.add_widget(self.back_btn)
        back_container.add_widget(Widget())  # Spacer
        self.add_widget(back_container)
        
        # Donation image
        self.donation_image = Image(
            source=image_path if os.path.exists(image_path) else "",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, None),
            height=dp(200)
        )
        self.add_widget(self.donation_image)
        
        # Donation title with teal color
        self.title = Label(
            text=title,
            font_size=sp(20),
            color=TEAL_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, None),
            height=dp(40),
            text_size=(self.width - dp(30), None),
            bold=True
        )
        self.title.bind(width=lambda instance, width: 
                        setattr(instance, 'text_size', (width - dp(30), None)))
        self.add_widget(self.title)
        
        # Choose Amount label
        choose_label = Label(
            text="Choose Amount",
            font_size=sp(18),
            color=DARK_TEXT_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=dp(40),
            bold=True
        )
        self.add_widget(choose_label)
        
        # Amount buttons container
        amount_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )
        
        # Create the amount buttons
        self.amount_buttons = []
        amounts = [1000, 5000, 10000]
        for amount in amounts:
            btn = AmountButton(
                amount,
                size_hint=(1, None),
                height=dp(50),
            )
            btn.bind(on_press=self.on_amount_selected)
            amount_container.add_widget(btn)
            self.amount_buttons.append(btn)
        
        self.add_widget(amount_container)
        
        # Or label
        or_label = Label(
            text="or",
            font_size=sp(16),
            color=LIGHT_TEXT_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=dp(40)
        )
        self.add_widget(or_label)
        
        # Enter Price Manually label
        manual_label = Label(
            text="Enter Price Manually",
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=dp(30)
        )
        self.add_widget(manual_label)
        
        # Custom amount input
        self.custom_amount_input = TextInput(
            hint_text="₱ Enter amount",
            multiline=False,
            background_normal='',
            background_active='',
            background_color=(1, 1, 1, 1),
            foreground_color=DARK_TEXT_COLOR,
            cursor_color=DARK_TEXT_COLOR,
            font_size=sp(16),
            padding=[dp(15), dp(10), dp(15), dp(10)],
            size_hint=(1, None),
            height=dp(50),
            input_filter='float'
        )
        
        # Add border to input field
        with self.custom_amount_input.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray border
            self.input_border = RoundedRectangle(
                pos=self.custom_amount_input.pos,
                size=self.custom_amount_input.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.custom_amount_input.bind(pos=self._update_input_border, 
                                   size=self._update_input_border,
                                   text=self.on_text_change)
        
        # Wrap input in container for better spacing
        input_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(60),
            padding=[0, dp(5), 0, dp(5)]
        )
        input_container.add_widget(self.custom_amount_input)
        self.add_widget(input_container)
        
        # Spacer
        self.add_widget(Widget(size_hint=(1, 1)))
        
        # Donate Now button
        self.donate_button = Button(
            text="Donate Now",
            font_size=sp(18),
            background_normal='',
            background_color=TEAL_COLOR,
            color=WHITE_COLOR,
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        
        # Add rounded corners to the donate button
        with self.donate_button.canvas.before:
            Color(*TEAL_COLOR)
            self.button_bg = RoundedRectangle(
                pos=self.donate_button.pos,
                size=self.donate_button.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.donate_button.bind(pos=self._update_button_bg, 
                             size=self._update_button_bg,
                             on_press=self.on_donate_now)
        self.add_widget(self.donate_button)
    
    def _update_input_border(self, instance, value):
        """Update input border when position or size changes"""
        self.input_border.pos = instance.pos
        self.input_border.size = instance.size
    
    def _update_button_bg(self, instance, value):
        """Update donate button background when position or size changes"""
        if hasattr(self, 'button_bg'):
            self.button_bg.pos = instance.pos
            self.button_bg.size = instance.size
    
    def on_amount_selected(self, instance):
        """Handle amount button selection"""
        self.selected_amount = instance.amount_value
        self.custom_amount = None
        self.custom_amount_input.text = ""
        
        # Update button states
        for btn in self.amount_buttons:
            if btn == instance:
                btn.select()
            else:
                btn.deselect()
        
        print(f"Selected amount: ₱{self.selected_amount}")
    
    def on_text_change(self, instance, value):
        """Handle custom amount text input"""
        if value:
            try:
                self.custom_amount = float(value)
                self.selected_amount = None
                
                # Deselect all buttons
                for btn in self.amount_buttons:
                    btn.deselect()
                
                print(f"Custom amount: ₱{self.custom_amount}")
            except ValueError:
                self.custom_amount = None
                print("Invalid amount entered")
    
    def on_donate_now(self, instance):
        """Handle donate now button press"""
        amount = self.selected_amount or self.custom_amount
        if amount:
            print(f"Processing donation of ₱{amount}")
            # Here you would navigate to payment processing or confirmation page
        else:
            print("No amount selected")
    
    def on_back(self, instance):
        """Handle back button press"""
        from kivy.app import App
        app = App.get_running_app()
        
        # Try different navigation methods in order of preference
        if hasattr(app, 'go_back_to_details'):
            # If the app has this specific method, use it
            app.go_back_to_details()
        elif hasattr(app.root, 'current') and hasattr(app.root, 'has_screen'):
            # If using a screen manager, try to navigate directly
            if app.root.has_screen('donation_details'):
                app.root.current = 'donation_details'
                print("Returning to donation details page")
            else:
                # Try to find any main/donate screen
                for screen_name in app.root.screen_names:
                    if 'donation' in screen_name or 'donate' in screen_name:
                        if screen_name != app.root.current:  # Don't navigate to self
                            app.root.current = screen_name
                            print(f"Navigated to {screen_name}")
                            return
                
                # If no donation screen found, try to go back to main/alumni screen
                for screen_name in app.root.screen_names:
                    if 'main' in screen_name.lower() or 'alumni' in screen_name.lower():
                        app.root.current = screen_name
                        print(f"Returning to {screen_name}")
                        return
        elif hasattr(app, 'go_back'):
            # Generic go_back method
            app.go_back()
        else:
            print("Warning: Could not navigate back - no navigation method found")
            print("Available screens:", app.root.screen_names if hasattr(app.root, 'screen_names') else "None")
            print("Current app:", app.__class__.__name__)

class DonationAmountPage(FloatLayout):
    """Main donation amount selection page layout"""
    def __init__(self, image_path=None, title=None, **kwargs):
        super().__init__(**kwargs)
        
        # Store the image and title
        self.image_path = image_path or os.path.join(ASSETS_PATH, "image_3.png")
        self.title = title or "Donate for Infrastructure"
        
        # White background
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add header
        self.header = HeaderBar(pos_hint={'top': 1})
        self.add_widget(self.header)
        
        # Add content with donation details (now takes full remaining space)
        self.content = DonationAmountContent(
            self.image_path,
            self.title,
            pos_hint={'x': 0, 'y': 0},
            size_hint=(1, 1 - self.header.height / self.height)
        )
        self.add_widget(self.content)
        
        # Handle window resize
        Clock.schedule_once(self._adjust_layout, 0.1)
        Window.bind(on_resize=self._on_window_resize)
    
    def _update_rect(self, instance, value):
        """Update background rectangle on size/position change"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _adjust_layout(self, dt):
        """Initial layout adjustment"""
        if self.height > 0:  # Avoid division by zero
            # Update content area position and size (no navigation bar)
            header_ratio = self.header.height / self.height
            self.content.pos_hint = {'x': 0, 'y': 0}
            self.content.size_hint = (1, 1 - header_ratio)
    
    def _on_window_resize(self, instance, width, height):
        """Handle window resize by updating layout"""
        if height > 0:  # Avoid division by zero
            Clock.schedule_once(self._adjust_layout, 0.1)

class DonationAmountApp(App):
    """Main application class for testing"""
    def build(self):
        return DonationAmountPage()
    
    def go_back_to_details(self):
        """Go back to the donation details page"""
        print("Returning to donation details page")
        if hasattr(self, 'root') and hasattr(self.root, 'current'):
            self.root.current = 'donation_details'
        else:
            # For standalone testing
            print("Would navigate back to donation details page")
    
    def show_settings_page(self):
        """Show settings page"""
        try:
            # Try to import the settings page
            from settings_page import SettingsPage
            from kivy.uix.screenmanager import ScreenManager, Screen
            
            # Check if we're using a screen manager
            if hasattr(self, 'root') and isinstance(self.root, ScreenManager):
                sm = self.root
                
                # Remove the settings screen if it exists
                if sm.has_screen('settings'):
                    sm.remove_widget(sm.get_screen('settings'))
                
                # Create the settings screen
                settings_screen = Screen(name='settings')
                settings_screen.add_widget(SettingsPage())
                sm.add_widget(settings_screen)
                
                # Switch to the settings screen
                sm.current = 'settings'
            else:
                # For standalone app where root is DonationAmountPage
                # Replace the current page with the settings page
                settings_page = SettingsPage()
                
                # Preserve window size
                if self.root:
                    window_size = Window.size
                    self.root = settings_page
                    Window.size = window_size
                else:
                    self.root = settings_page
        except ImportError:
            print("Error: settings_page.py not found or SettingsPage class not defined.")
            print("Please create a settings_page.py file with a SettingsPage class.")

if __name__ == "__main__":
    DonationAmountApp().run()
