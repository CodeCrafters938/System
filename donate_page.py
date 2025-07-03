from turtle import Screen
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView  # Add missing import
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.widget import Widget
from pathlib import Path
import os

# Import the new DonationWidget
from donation_widget import DonationWidget

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

# Path to assets
ASSETS_PATH = Path(__file__).parent / Path(r"build\assets\frame7")
NAVIGATION_ICONS_PATH = Path(__file__).parent / Path(r"navigation_icons")

# Create navigation_icons directory if it doesn't exist
if not os.path.exists(NAVIGATION_ICONS_PATH):
    os.makedirs(NAVIGATION_ICONS_PATH)

class HeaderBar(BoxLayout):
    """Teal header bar with school name and settings button"""
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
        
        # Right - Settings gear icon
        gear_path = os.path.join(ASSETS_PATH, "button_9.png")
        self.settings_btn = Button(
            background_normal=gear_path if os.path.exists(gear_path) else "",
            background_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        self.settings_btn.bind(on_press=self.on_settings)
        self.add_widget(self.settings_btn)
    
    def _update_rect(self, instance, value):
        """Update background when size changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_settings(self, instance):
        """Handle settings button press"""
        print("Settings button pressed")
        # Navigate to settings page
        App.get_running_app().show_settings_page()

class SearchBar(BoxLayout):
    """Search bar with input field and search button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(20), dp(10), dp(20), dp(10)]
        self.spacing = dp(10)
        
        # Search input field with border
        self.search_input = TextInput(
            hint_text="",
            multiline=False,
            background_normal='',
            background_active='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(0.3, 0.3, 0.3, 1),
            font_size=sp(16),
            padding=[dp(15), dp(10), dp(15), dp(10)],
            size_hint=(0.75, 1)
        )
        
        # Add border to search input
        with self.search_input.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray border
            self.search_border = RoundedRectangle(
                pos=self.search_input.pos,
                size=self.search_input.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.search_input.bind(pos=self._update_search_border, size=self._update_search_border)
        self.add_widget(self.search_input)
        
        # Search button
        self.search_button = Button(
            text="Search",
            font_size=sp(16),
            background_normal='',
            background_color=TEAL_COLOR,
            color=WHITE_COLOR,
            size_hint=(0.25, 1)
        )
        
        # Add rounded corners to search button
        with self.search_button.canvas.before:
            Color(*TEAL_COLOR)
            self.button_bg = RoundedRectangle(
                pos=self.search_button.pos,
                size=self.search_button.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.search_button.bind(pos=self._update_button_bg, size=self._update_button_bg)
        self.search_button.bind(on_press=self.on_search)
        self.add_widget(self.search_button)
    
    def _update_search_border(self, instance, value):
        """Update search input border when position or size changes"""
        self.search_border.pos = instance.pos
        self.search_border.size = instance.size
    
    def _update_button_bg(self, instance, value):
        """Update search button background when position or size changes"""
        self.button_bg.pos = instance.pos
        self.button_bg.size = instance.size
    
    def on_search(self, instance):
        """Handle search button press"""
        search_text = self.search_input.text
        print(f"Searching for: {search_text}")

class DonationCard(BoxLayout):
    """Card displaying a donation opportunity"""
    def __init__(self, image_path, title, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path
        self.title_text = title
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(245)  # Reduced height for more compact layout
        self.padding = [dp(10), dp(5), dp(10), dp(5)]  # Reduced vertical padding
        self.spacing = dp(5)  # Reduced spacing between elements
        
        # Card background with shadow effect
        with self.canvas.before:
            # White background with shadow effect
            Color(*WHITE_COLOR)
            self.rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size,
                radius=[dp(10), dp(10), dp(10), dp(10)]
            )
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Image at the top
        self.image = Image(
            source=image_path if os.path.exists(image_path) else "",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, None),
            height=dp(150)
        )
        self.add_widget(self.image)
        
        # Title below image with text wrapping (no spacer needed)
        self.title = Label(
            text=title,
            font_size=sp(16),
            color=(38/255, 30/255, 107/255, 1),  # Dark blue color from image
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=dp(35),  # Reduced height
            bold=True
        )
        # Enable text wrapping
        self.title.bind(width=lambda instance, width: 
                     setattr(instance, 'text_size', (width - dp(20), None)))
        self.add_widget(self.title)
        
        # Donate button at the bottom
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40),
            padding=[0, dp(0), 0, dp(5)]  # Added bottom padding to move button up
        )
        
        # Using a spacer on left to center button
        button_layout.add_widget(Widget(size_hint=(0.35, 1)))
        
        # Donate button
        self.donate_button = Button(
            text="Donate",
            font_size=sp(16),
            background_normal='',
            background_color=TEAL_COLOR,
            color=WHITE_COLOR,
            size_hint=(0.3, None),
            height=dp(40),
        )
        
        # Add rounded corners to donate button
        with self.donate_button.canvas.before:
            Color(*TEAL_COLOR)
            self.button_bg = RoundedRectangle(
                pos=self.donate_button.pos,
                size=self.donate_button.size,
                radius=[dp(10), dp(10), dp(10), dp(10)]
            )
        self.donate_button.bind(pos=self._update_button_bg, size=self._update_button_bg)
        self.donate_button.bind(on_press=self.on_donate)
        button_layout.add_widget(self.donate_button)
        
        # Using a spacer on right to center button
        button_layout.add_widget(Widget(size_hint=(0.35, 1)))
        
        self.add_widget(button_layout)
    
    def _update_rect(self, instance, value):
        """Update card background when position or size changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _update_button_bg(self, instance, value):
        """Update donate button background when position or size changes"""
        self.button_bg.pos = instance.pos
        self.button_bg.size = instance.size
    
    def on_donate(self, instance):
        """Handle donate button press"""
        print(f"Donation requested for: {self.title.text}")
        # Navigate to donation details page
        App.get_running_app().show_donation_details(self.image_path, self.title_text)

class DonationContent(BoxLayout):
    """Content area for donations page"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, dp(10), 0, dp(10)]  # Increased padding for better spacing
        self.spacing = dp(15)  # Increased spacing between widgets
        
        # Search bar at the top
        self.search_bar = SearchBar(size_hint=(1, None), height=dp(50))
        self.add_widget(self.search_bar)
        
        # Create a scroll view to contain donation widgets
        scroll_view = ScrollView(
            do_scroll_x=False,
            size_hint=(1, 1)
        )
        
        # Create vertical container for donation widgets
        donation_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        donation_container.bind(minimum_height=donation_container.setter('height'))
        
        # Computer labs donation widget
        computer_labs_image = os.path.join(ASSETS_PATH, "image_3.png")
        self.computer_labs_widget = DonationWidget(
            computer_labs_image,
            "Donate for Computer Labs",
            on_donate_callback=self.on_donate
        )
        donation_container.add_widget(self.computer_labs_widget)
        
        # Infrastructure donation widget
        infrastructure_image = os.path.join(ASSETS_PATH, "image_5.png")
        self.infrastructure_widget = DonationWidget(
            infrastructure_image,
            "Donate for Infrastructure",
            on_donate_callback=self.on_donate
        )
        donation_container.add_widget(self.infrastructure_widget)
        
        # Add container to scroll view
        scroll_view.add_widget(donation_container)
        
        # Add scroll view to main layout
        self.add_widget(scroll_view)
    
    def on_donate(self, image_source, title):
        """Handle donate button press"""
        print(f"Donation requested for: {title}")
        # Navigate to donation details page
        App.get_running_app().show_donation_details(image_source, title)

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

class DonatePage(FloatLayout):
    """Main donate page layout"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # White background
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add header
        self.header = HeaderBar(pos_hint={'top': 1})
        self.add_widget(self.header)
        
        # Add navigation bar at bottom
        self.nav = EmptyNavigationBar(pos_hint={'bottom': 1})
        self.add_widget(self.nav)
        
        # Add icons to navigation bar
        self._add_navigation_icons()
        
        # Add content with donation cards
        self.content = DonationContent(
            pos_hint={'x': 0, 'y': self.nav.height/self.height},
            size_hint=(1, 1 - (self.header.height + self.nav.height) / self.height)
        )
        self.add_widget(self.content)
        
        # Handle window resize
        Clock.schedule_once(self._adjust_layout, 0.1)
        Window.bind(on_resize=self._on_window_resize)
    
    def _add_navigation_icons(self):
        """Add icons to navigation bar slots"""
        # Add home icon to first slot
        home_icon_path = os.path.join(NAVIGATION_ICONS_PATH, "home_icon.png")
        if not os.path.exists(home_icon_path):
            home_icon_path = os.path.join(ASSETS_PATH, "home_icon.png")
        
        if os.path.exists(home_icon_path):
            self.nav.add_icon_to_slot(0, home_icon_path, "Home", icon_pos_y=0.3)
        else:
            self.nav.slots[0].add_widget(Label(text="Home", font_size=sp(14)))
        
        # Add donation icon to second slot
        donation_icon_path = os.path.join(NAVIGATION_ICONS_PATH, "donation_icon.png")
        if not os.path.exists(donation_icon_path):
            donation_icon_path = os.path.join(ASSETS_PATH, "donation_icon.png")
        
        if os.path.exists(donation_icon_path):
            self.nav.add_icon_to_slot(1, donation_icon_path, "Donation", icon_pos_y=0.3)
        else:
            self.nav.slots[1].add_widget(Label(text="Donation", font_size=sp(14)))
        
        # Add search icon to third slot
        search_icon_path = os.path.join(NAVIGATION_ICONS_PATH, "search_icon.png")
        if not os.path.exists(search_icon_path):
            search_icon_path = os.path.join(ASSETS_PATH, "search_icon.png")
        
        if os.path.exists(search_icon_path):
            self.nav.add_icon_to_slot(2, search_icon_path, "Search", icon_pos_y=0.3)
        else:
            self.nav.slots[2].add_widget(Label(text="Search", font_size=sp(14)))
        
        # Add calendar icon to fourth slot
        calendar_icon_path = os.path.join(NAVIGATION_ICONS_PATH, "calendar_icon.png")
        if not os.path.exists(calendar_icon_path):
            calendar_icon_path = os.path.join(ASSETS_PATH, "calendar_icon.png")
        
        if os.path.exists(calendar_icon_path):
            self.nav.add_icon_to_slot(3, calendar_icon_path, "Event Calendar", 
                                     icon_size=(dp(55), dp(55)),
                                     icon_pos_y=0.3)
        else:
            self.nav.slots[3].add_widget(Label(text="Event Calendar", font_size=sp(12)))
        
        # Add profile icon to fifth slot
        profile_icon_path = os.path.join(NAVIGATION_ICONS_PATH, "profile_icon.png")
        if not os.path.exists(profile_icon_path):
            profile_icon_path = os.path.join(ASSETS_PATH, "profile_icon.png")
        
        if os.path.exists(profile_icon_path):
            profile_icon_size = dp(25)
            self.nav.add_icon_to_slot(4, profile_icon_path, "Profile", 
                                     icon_size=(profile_icon_size, profile_icon_size),
                                     icon_pos_y=0.3)
        else:
            self.nav.slots[4].add_widget(Label(text="Profile", font_size=sp(13)))
    
    def _update_rect(self, instance, value):
        """Update background rectangle on size/position change"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _adjust_layout(self, dt):
        """Initial layout adjustment"""
        if self.height > 0:  # Avoid division by zero
            # Update content area position and size
            header_ratio = self.header.height / self.height
            nav_ratio = self.nav.height / self.height
            self.content.pos_hint = {'x': 0, 'y': nav_ratio, 'top': 1 - header_ratio}
            self.content.size_hint = (1, 1 - header_ratio - nav_ratio)
    
    def _on_window_resize(self, instance, width, height):
        """Handle window resize by updating layout"""
        if height > 0:  # Avoid division by zero
            Clock.schedule_once(self._adjust_layout, 0.1)
    
    def show_donation_details(self, image_path, title):
        """Show donation details page"""
        from donation_details_page import DonationDetailsPage
        details_page = DonationDetailsPage(image_path=image_path, title=title)
        self.parent.add_widget(details_page)
        self.parent.current = 'donation_details'

class DonatePageApp(App):
    """Main application class"""
    def build(self):
        from kivy.uix.screenmanager import ScreenManager, Screen
        
        # Create the screen manager
        sm = ScreenManager()
        
        # Create the login page first to ensure it exists
        try:
            from login_page import LoginPage
            login_screen = Screen(name='login')
            login_screen.add_widget(LoginPage())
            sm.add_widget(login_screen)
        except ImportError as e:
            print(f"Error importing LoginPage: {e}")
            # Create a simple placeholder login screen if import fails
            login_screen = Screen(name='login')
            box = BoxLayout(orientation='vertical', padding=[20, 20])
            box.add_widget(Label(text="Login Page\nCould not load actual login page.", 
                                 halign='center', valign='middle'))
            login_screen.add_widget(box)
            sm.add_widget(login_screen)
        
        # Create the donate page screen
        donate_screen = Screen(name='donate')
        donate_screen.add_widget(DonatePage())
        sm.add_widget(donate_screen)
        
        # Start with donate screen
        sm.current = 'donate'
        
        return sm
    
    def show_login_page(self):
        """Show login page"""
        print("Showing login page")
        try:
            # Get the screen manager
            sm = self.root
            
            # Check if login screen already exists
            if not sm.has_screen('login'):
                # Try to create the login screen
                try:
                    from login_page import LoginPage
                    login_screen = Screen(name='login')
                    login_screen.add_widget(LoginPage())
                    sm.add_widget(login_screen)
                except ImportError as e:
                    print(f"Error importing LoginPage: {e}")
                    # Create a simple placeholder login screen if import fails
                    login_screen = Screen(name='login')
                    box = BoxLayout(orientation='vertical', padding=[20, 20])
                    box.add_widget(Label(text="Login Page\nCould not load actual login page.", 
                                         halign='center', valign='middle'))
                    login_screen.add_widget(box)
                    sm.add_widget(login_screen)
            
            # Switch to the login screen
            sm.current = 'login'
        except Exception as e:
            print(f"Error showing login page: {e}")
    
    def show_donation_details(self, image_path, title):
        """Show donation details page"""
        from donation_details_page import DonationDetailsPage
        from kivy.uix.screenmanager import Screen
        
        # Get the screen manager
        sm = self.root
        
        # Remove the donation details screen if it exists
        if sm.has_screen('donation_details'):
            sm.remove_widget(sm.get_screen('donation_details'))
        
        # Create the donation details screen
        details_screen = Screen(name='donation_details')
        details_screen.add_widget(DonationDetailsPage(image_path=image_path, title=title))
        sm.add_widget(details_screen)
        
        # Switch to the donation details screen
        sm.current = 'donation_details'
    
    def show_donation_amount(self, image_path, title):
        """Show donation amount selection page"""
        from donation_amount_page import DonationAmountPage
        from kivy.uix.screenmanager import Screen
        
        # Get the screen manager
        sm = self.root
        
        # Remove the amount screen if it exists
        if sm.has_screen('donation_amount'):
            sm.remove_widget(sm.get_screen('donation_amount'))
        
        # Create the amount selection screen
        amount_screen = Screen(name='donation_amount')
        amount_screen.add_widget(DonationAmountPage(image_path=image_path, title=title))
        sm.add_widget(amount_screen)
        
        # Switch to the amount selection screen
        sm.current = 'donation_amount'
    
    def show_event_calendar(self):
        """Show event calendar page"""
        from event_calendar_page import EventCalendarPage
        from kivy.uix.screenmanager import Screen
        
        # Get the screen manager
        sm = self.root
        
        # Remove the event calendar screen if it exists
        if sm.has_screen('event_calendar'):
            sm.remove_widget(sm.get_screen('event_calendar'))
        
        # Create the event calendar screen
        calendar_screen = Screen(name='event_calendar')
        calendar_screen.add_widget(EventCalendarPage())
        sm.add_widget(calendar_screen)
        
        # Switch to the event calendar screen
        sm.current = 'event_calendar'
    
    def show_login_page(self):
        """Show login page"""
        from login_page import LoginPage
        from kivy.uix.screenmanager import Screen
        
        # Get the screen manager
        sm = self.root
        
        # Check if login screen already exists
        if not sm.has_screen('login'):
            # Create the login screen
            login_screen = Screen(name='login')
            login_screen.add_widget(LoginPage())
            sm.add_widget(login_screen)
        
        # Switch to the login screen
        sm.current = 'login'

    def show_settings_page(self):
        """Show settings page"""
        from settings_page import SettingsPage
        from kivy.uix.screenmanager import Screen
        
        # Get the screen manager
        sm = self.root
        
        # Remove the settings screen if it exists
        if sm.has_screen('settings'):
            sm.remove_widget(sm.get_screen('settings'))
        
        # Create the settings screen
        settings_screen = Screen(name='settings')
        settings_screen.add_widget(SettingsPage(on_signout=self.show_login_page))
        sm.add_widget(settings_screen)
        
        # Switch to the settings screen
        sm.current = 'settings'
    
    def go_back(self):
        """Go back to the donations page"""
        # Get the screen manager
        sm = self.root
        sm.current = 'donate'
    
    def go_back_to_details(self):
        """Go back to donation details from amount page"""
        # Get the screen manager
        sm = self.root
        if sm.has_screen('donation_details'):
            sm.current = 'donation_details'
        else:
            sm.current = 'donate'

if __name__ == "__main__":
    DonatePageApp().run()
