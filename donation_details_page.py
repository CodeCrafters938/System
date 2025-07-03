from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
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
    'small': {'width': 392, 'height': 759},  # Match the image proportions
    'medium': {'width': 1080, 'height': 2340},  # Common smartphone size
}

# For mobile devices, let the system set the window size
# Only set window size for desktop/development
if platform not in ('android', 'ios'):
    Window.size = (DEVICE_PROFILES['small']['width'], DEVICE_PROFILES['small']['height'])

# Colors from the image
TEAL_COLOR = (26/255, 164/255, 159/255, 1)  # #1AA49F
WHITE_COLOR = (1, 1, 1, 1)
GRAY_COLOR = (0.9, 0.9, 0.9, 1)
DARK_TEXT_COLOR = (0.2, 0.2, 0.2, 1)
LIGHT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)
BLUE_TEXT_COLOR = (0/255, 122/255, 255/255, 1)  # Blue color for links and titles

# Path to assets
ASSETS_PATH = Path(__file__).parent / Path(r"build\assets\frame7")
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
                height=dp(15),  # Reduced height to move up closer to icon
                halign='center',
                padding=(0, dp(-8))  # Increased negative padding to pull text up
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

class DonationDetailsContent(BoxLayout):
    """Content area for donation details page"""
    def __init__(self, image_path, title="Donate for Infrastructure", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(10), dp(15), dp(15)]
        self.spacing = dp(15)  # Increased spacing between elements
        
        # Back button at the top-left with teal color exactly like the image
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
        
        # Add a small spacer widget to create distance between image and title
        self.add_widget(Widget(size_hint=(1, None), height=dp(5)))
        
        # Donation title with teal color like in the image
        self.title = Label(
            text=title,
            font_size=sp(20),
            color=TEAL_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, None),
            height=dp(50),  # Increased height for better text display
            text_size=(self.width - dp(30), None),  # Allow text to wrap
            bold=True
        )
        # Ensure text_size updates when width changes for proper wrapping
        self.title.bind(width=lambda instance, width: 
                        setattr(instance, 'text_size', (width - dp(30), None)))
        self.add_widget(self.title)
        
        # Divider line
        with self.canvas:
            Color(*GRAY_COLOR)
            self.divider = Rectangle(
                pos=(self.x, self.y + self.height - dp(290)),
                size=(self.width, dp(1))
            )
        self.bind(pos=self._update_divider, size=self._update_divider)
        
        # Description text with light gray color as shown in image
        self.description = Label(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            font_size=sp(16),
            color=LIGHT_TEXT_COLOR,  # Gray color as shown in the image
            halign='left',
            valign='top',
            size_hint=(1, None),
            height=dp(120),
            padding=(dp(10), dp(10))
        )
        # Bind the text_size to the widget width for proper text wrapping
        self.description.bind(width=lambda instance, width: 
                             setattr(instance, 'text_size', (width - dp(20), None)))
        
        self.add_widget(self.description)
        
        # Spacer
        self.add_widget(Widget(size_hint=(1, 1)))
        
        # Total donation amount section
        total_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(60),
            padding=[0, dp(10), 0, dp(10)]
        )
        
        # "Total Donation" label
        total_label = Label(
            text="Total Donation",
            font_size=sp(16),
            color=LIGHT_TEXT_COLOR,  # Match the image with a lighter color
            halign='center',
            valign='bottom',
            size_hint=(1, None),
            height=dp(20)
        )
        total_box.add_widget(total_label)
        
        # Amount value with proper PHP symbol and formatting
        amount_label = Label(
            text="₱2,77,567.08",  # Matching exactly the format in the image
            font_size=sp(24),
            color=DARK_TEXT_COLOR,
            halign='center',
            valign='top',
            size_hint=(1, None),
            height=dp(30),
            bold=True
        )
        total_box.add_widget(amount_label)
        
        self.add_widget(total_box)
        
        # Donate Now button - full width green button like in image
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
        
        # Add rounded corners to the donate button like in the image
        with self.donate_button.canvas.before:
            Color(*TEAL_COLOR)
            self.button_bg = RoundedRectangle(
                pos=self.donate_button.pos,
                size=self.donate_button.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.donate_button.bind(pos=self._update_button_bg, size=self._update_button_bg)
        self.donate_button.bind(on_press=self.on_donate_now)
        self.add_widget(self.donate_button)
    
    def _update_divider(self, instance, value):
        """Update divider line when size changes"""
        if hasattr(self, 'divider'):
            self.divider.pos = (self.x, self.y + self.height - dp(290))
            self.divider.size = (self.width, dp(1))
    
    def _update_button_bg(self, instance, value):
        """Update donate button background when position or size changes"""
        if hasattr(self, 'button_bg'):
            self.button_bg.pos = instance.pos
            self.button_bg.size = instance.size
    
    def on_donate_now(self, instance):
        """Handle donate now button press"""
        print("Donate Now button pressed - navigating to amount selection")
        from kivy.app import App
        app = App.get_running_app()
        
        # Check if the app has the show_donation_amount method
        if hasattr(app, 'show_donation_amount'):
            app.show_donation_amount(self.donation_image.source, self.title.text)
        else:
            print("show_donation_amount method not found in app - using fallback")
            try:
                # Try to directly import and create the donation amount page
                from donation_amount_page import DonationAmountPage
                from kivy.uix.screenmanager import Screen
                
                # Check if we're in a screen manager context
                if hasattr(app.root, 'current') and hasattr(app.root, 'add_widget'):
                    # Create the donation amount screen
                    screen_name = 'donation_amount'
                    
                    # Remove the screen if it already exists
                    if hasattr(app.root, 'has_screen') and app.root.has_screen(screen_name):
                        app.root.remove_widget(app.root.get_screen(screen_name))
                    
                    # Add the donation amount screen
                    amount_screen = Screen(name=screen_name)
                    amount_screen.add_widget(DonationAmountPage(
                        image_path=self.donation_image.source, 
                        title=self.title.text
                    ))
                    app.root.add_widget(amount_screen)
                    
                    # Switch to the donation amount screen
                    app.root.current = screen_name
                else:
                    # Not in a screen manager context, try launcher approach
                    from kivy.app import App
                    from donation_amount_page import DonationAmountApp
                    
                    print("Launching standalone donation amount app")
                    amount_app = DonationAmountApp()
                    app.stop()  # Stop current app
                    amount_app.run()  # Run donation amount app
                    
            except ImportError:
                print("Error: donation_amount_page.py not found or could not be imported.")
            except Exception as e:
                print(f"Error navigating to donation amount page: {e}")
        
    def on_back(self, instance):
        """Handle back button press - go back to donation page"""
        print("Back button pressed - returning to donate page")
        from kivy.app import App
        app = App.get_running_app()
        
        # Check if we're using a ScreenManager
        if hasattr(app.root, 'current') and hasattr(app.root, 'has_screen'):
            # We're using a ScreenManager - switch to the alumni directory screen
            if app.root.has_screen('alumni_directory'):
                app.root.current = 'alumni_directory'
            else:
                # Try to find the main screen by different names
                for screen_name in app.root.screen_names:
                    if 'alumni' in screen_name.lower() or 'main' in screen_name.lower() or 'directory' in screen_name.lower():
                        app.root.current = screen_name
                        return
                
                # If no main screen found, go to the first screen
                if app.root.screen_names:
                    app.root.current = app.root.screen_names[0]
        else:
            # Fallback for apps that have the go_back method
            if hasattr(app, 'go_back'):
                app.go_back()
            else:
                print("Could not navigate back - no go_back method or ScreenManager found")

class DonationDetailsPage(FloatLayout):
    """Main donation details page layout"""
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
        self.content = DonationDetailsContent(
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

class DonationDetailsApp(App):
    """Main application class for testing"""
    def build(self):
        return DonationDetailsPage()
    
    def go_back(self):
        """Go back to the donations page"""
        print("Returning to donation page")
        if hasattr(self, 'root') and hasattr(self.root, 'current'):
            self.root.current = 'donate'
        else:
            # For standalone testing
            print("Would navigate back to donate page")
    
    def show_donation_amount(self, image_path, title):
        """Show donation amount selection page"""
        try:
            from donation_amount_page import DonationAmountPage
            from kivy.uix.screenmanager import ScreenManager, Screen
            
            # Check if we're using a screen manager
            if hasattr(self, 'root') and isinstance(self.root, ScreenManager):
                sm = self.root
                
                # Remove the donation amount screen if it exists
                if sm.has_screen('donation_amount'):
                    sm.remove_widget(sm.get_screen('donation_amount'))
                
                # Create the donation amount screen
                amount_screen = Screen(name='donation_amount')
                amount_screen.add_widget(DonationAmountPage(image_path, title))
                sm.add_widget(amount_screen)
                
                # Switch to the donation amount screen
                sm.current = 'donation_amount'
            else:
                # For standalone app where root is DonationDetailsPage
                # Replace the current page with the donation amount page
                amount_page = DonationAmountPage(image_path, title)
                
                # Preserve window size
                if self.root:
                    window_size = Window.size
                    self.root = amount_page
                    Window.size = window_size
                else:
                    self.root = amount_page
                    
            print(f"Navigating to amount selection for {title}")
            print(f"Image path: {image_path}")
        except ImportError:
            print("Error: donation_amount_page.py not found or DonationAmountPage class not defined.")
            print("Please create a donation_amount_page.py file with a DonationAmountPage class.")
