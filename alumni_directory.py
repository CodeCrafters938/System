from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.lang import Builder
from pathlib import Path
import os

# Add KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDIconButton

# Import the DonationWidget
from donation_widget import DonationWidget

# Import the BatchmatesWidget
from batchmates_widget import BatchmatesWidget

# Import the EventCalendarWidget for the calendar tab
from event_calendar_widget import EventCalendarWidget

# Import the ProfileCardWidget for the profile tab
from profile_card_widget import ProfileCardWidget
from kivy.animation import Animation  # Add animation import at the top

# Import the SettingsPage
from settings_page import SettingsPage

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

# KV string for the search field - updated hint text
search_field_kv = """
MDTextField:
    hint_text: "Search donation projects..."
    mode: "rectangle"
    multiline: False
    font_size: sp(16)
    size_hint: (1, None)
    height: dp(50)
    pos_hint: {"center_y": 0.5}
"""

class SearchBar(BoxLayout):
    """Search bar with input field that filters automatically"""
    def __init__(self, on_filter_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(20), dp(0), dp(20), dp(0)]  # Removed vertical padding
        
        # Store the filter callback
        self.on_filter_callback = on_filter_callback
        
        # Search input field using MDTextField
        self.search_input = Builder.load_string(search_field_kv)
        
        # Bind the text property to filter as the user types
        self.search_input.bind(text=self.on_text_changed)
        
        self.add_widget(self.search_input)
    
    def on_text_changed(self, instance, value):
        """Handle text changes in the search field"""
        # Call the provided filter callback if it exists
        if self.on_filter_callback:
            self.on_filter_callback(value)

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
        
        # Center - School name
        school_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.school_name = Label(
            text="Santisimo Rosario",
            font_size=sp(16),
            color=WHITE_COLOR,
            halign='left',
            valign='bottom',
            size_hint=(1, 0.5),
            text_size=(None, None),
            bold=True
        )
        self.school_subtext = Label(
            text="Integrated Highschool",
            font_size=sp(14),
            color=WHITE_COLOR,
            halign='left',
            valign='top',
            size_hint=(1, 0.5),
            text_size=(None, None)
        )
        school_layout.add_widget(self.school_name)
        school_layout.add_widget(self.school_subtext)
        self.add_widget(school_layout)
        
        # Right - Settings cog icon (invisible by default)
        self.settings_btn = MDIconButton(
            icon="cog",
            theme_icon_color="Custom",
            icon_color=WHITE_COLOR,
            size_hint=(None, None),
            size=(dp(24), dp(40)),  # Reduced width from 40dp to 24dp
            pos_hint={'center_y': 0.5},
            opacity=0,  # Start with invisible button
            disabled=True  # Start with disabled button
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
        
        # Navigate to the settings page via the app
        app = MDApp.get_running_app()
        if hasattr(app, 'show_settings_page'):
            app.show_settings_page()
        else:
            # Try direct navigation if method doesn't exist
            try:
                if hasattr(app.root, 'current'):
                    app.root.current = 'settings'
                    print("Navigated to settings page")
            except Exception as e:
                print(f"Could not navigate to settings: {e}")
    
    def show_settings_button(self, show=True):
        """Show or hide the settings button"""
        if show:
            # Make fully visible with animation
            from kivy.animation import Animation
            anim = Animation(opacity=1, duration=0.2)
            anim.start(self.settings_btn)
            self.settings_btn.disabled = False
        else:
            # Hide immediately
            self.settings_btn.opacity = 0
            self.settings_btn.disabled = True

class DirectoryContent(FloatLayout):
    """Content area for alumni directory - currently blank"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # White background
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Currently blank - will be populated with alumni listings later
        
    def _update_bg(self, instance, value):
        """Update background when size changes"""
        self.bg.pos = self.pos
        self.bg.size = self.size

class AlumniDirectoryPage(Screen):
    """Main alumni directory page layout"""
    # Track the currently active tab name
    current_tab = 'home'  # Default to home tab
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create a base layout
        self.base_layout = FloatLayout()
        self.add_widget(self.base_layout)
        
        # White background
        with self.base_layout.canvas.before:
            Color(*WHITE_COLOR)
            self.rect = Rectangle(pos=self.base_layout.pos, size=self.base_layout.size)
        self.base_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add header (without settings navigation callback)
        self.header = HeaderBar(pos_hint={'top': 1})
        self.base_layout.add_widget(self.header)
        
        # Calculate header height ratio more precisely to avoid compression
        header_height_ratio = self.header.height / Window.height
        
        # Create content area that will contain the MDBottomNavigation
        # Use absolute positioning to prevent compression
        self.content_layout = FloatLayout(
            pos_hint={'x': 0, 'y': 0, 'top': 1 - header_height_ratio},
            size_hint=(1, 1 - header_height_ratio)
        )
        
        # Create MDBottomNavigation
        self.bottom_nav = MDBottomNavigation()
        self.bottom_nav.bind(on_tab_switch=self.on_tab_switch)
        
        # Create Home tab
        home_tab = MDBottomNavigationItem(name='home', text='Home', icon='home')
        home_content = DirectoryContent(size_hint=(1, 1))
        home_tab.add_widget(home_content)
        self.bottom_nav.add_widget(home_tab)
        
        # Create Donation tab
        donation_tab = MDBottomNavigationItem(name='donation', text='Donation', icon='hand-heart')
        
        # Create vertical layout for donation content
        donation_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(0), dp(10), dp(0), dp(10)]
        )
        
        # Store donation widgets for filtering
        self.donation_widgets = {}
        
        # Add search bar at the top - use filter_donations as callback
        search_bar = SearchBar(
            size_hint=(1, None), 
            height=dp(50),
            on_filter_callback=self.filter_donations
        )
        donation_layout.add_widget(search_bar)
        
        # Create a scroll view for donation content
        donation_scroll = ScrollView(
            do_scroll_x=False,
            size_hint=(1, 1)
        )
        
        # Create container for donation widgets
        self.donation_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(20),
            padding=[dp(15), dp(10), dp(15), dp(10)]
        )
        self.donation_container.bind(minimum_height=self.donation_container.setter('height'))
        
        # Add donation widgets using Frame 7 assets
        computer_labs_image = os.path.join(ASSETS_PATH, "image_3.png")
        computer_labs_widget = DonationWidget(
            computer_labs_image,
            "Donate for Computer Labs",
            on_donate_callback=self.on_donate
        )
        self.donation_container.add_widget(computer_labs_widget)
        # Store for filtering
        self.donation_widgets["Computer Labs"] = computer_labs_widget
        
        infrastructure_image = os.path.join(ASSETS_PATH, "image_5.png")
        infrastructure_widget = DonationWidget(
            infrastructure_image,
            "Donate for Infrastructure",
            on_donate_callback=self.on_donate
        )
        self.donation_container.add_widget(infrastructure_widget)
        # Store for filtering
        self.donation_widgets["Infrastructure"] = infrastructure_widget
        
        # Add donation container to scroll view
        donation_scroll.add_widget(self.donation_container)
        
        # Add scroll view to donation layout
        donation_layout.add_widget(donation_scroll)
        
        # Add the donation layout to the donation tab
        donation_tab.add_widget(donation_layout)
        self.bottom_nav.add_widget(donation_tab)
        
        # Create Search tab
        search_tab = MDBottomNavigationItem(name='search', text='Search', icon='magnify')
        
        # Create a scroll view for the BatchmatesWidget
        search_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1),
            bar_width=0  # Hide scrollbar
        )
        
        # Add BatchmatesWidget with QR navigation callback
        search_scroll.add_widget(BatchmatesWidget(on_qr_press=self.on_qr_code_press))
        search_tab.add_widget(search_scroll)
        self.bottom_nav.add_widget(search_tab)
        
        # Create Calendar tab
        calendar_tab = MDBottomNavigationItem(name='events', text='Events', icon='calendar')
        calendar_content = EventCalendarWidget(size_hint=(1, 1))
        calendar_tab.add_widget(calendar_content)
        self.bottom_nav.add_widget(calendar_tab)
        
        # Create Profile tab
        profile_tab = MDBottomNavigationItem(name='profile', text='Profile', icon='account')
        
        # Create a scroll view for the profile content
        profile_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1)
        )
        
        # Add ProfileCardWidget to the profile tab
        profile_card = ProfileCardWidget()
        
        # Set up some sample profile data
        profile_card.update_profile(
            name="Alejandino, Ivan Ray",
            status="Alumni",
            batch="Batch 2015 - 2016",
            course="BSIT",
            address="123 Main Street, City",
            email="ivan.alejandino@example.com",
            contact="+123-456-7890"
        )
        
        profile_scroll.add_widget(profile_card)
        profile_tab.add_widget(profile_scroll)
        self.bottom_nav.add_widget(profile_tab)
        
        # After adding all tabs, make sure the MDBottomNavigation fills the content area
        self.content_layout.add_widget(self.bottom_nav)
        self.base_layout.add_widget(self.content_layout)
        
        # Bind to window size changes to keep layout adjusted
        Window.bind(on_resize=self._on_window_resize)
        
        # Schedule layout adjustment and tab setup
        Clock.schedule_once(self._adjust_layout, 0.1)
        Clock.schedule_once(self.initial_tab_setup, 0.5)
    
    def _adjust_layout(self, dt):
        """Adjust layout based on window size to prevent compression"""
        if Window.height > 0:  # Avoid division by zero
            # Recalculate header height ratio
            header_height_ratio = self.header.height / Window.height
            
            # Update content layout position and size
            self.content_layout.pos_hint = {'x': 0, 'y': 0, 'top': 1 - header_height_ratio}
            self.content_layout.size_hint = (1, 1 - header_height_ratio)
    
    def _on_window_resize(self, instance, width, height):
        """Handle window resizing events"""
        # Re-adjust layout when window size changes
        Clock.schedule_once(self._adjust_layout, 0.1)
    
    def initial_tab_setup(self, dt):
        """Set up the initial tab and button visibility"""
        print("Setting up initial tab and button visibility")
        # Check if profile tab is selected initially
        try:
            if hasattr(self.bottom_nav, 'selected'):
                tab_name = self.bottom_nav.selected
                print(f"Initial tab: {tab_name}")
                # Set settings button visibility based on current tab
                self.header.show_settings_button(tab_name == 'profile')
        except Exception as e:
            print(f"Error in initial_tab_setup: {e}")
    
    def navigate_to_search_tab(self):
        """Switch to the Search tab to display BatchmatesWidget"""
        # Switch to the search tab in MDBottomNavigation
        self.bottom_nav.switch_tab('search')
        print("Navigating to the search tab to find batchmates")
    
    def on_donate(self, image_source, title):
        """Handle donate button press"""
        print(f"Donation requested for: {title}")
        # Navigate to donation details page
        app = MDApp.get_running_app()
        if hasattr(app, 'show_donation_details'):
            app.show_donation_details(image_source, title)
        else:
            # If the method doesn't exist in the app, import and create the details page
            try:
                from donation_details_page import DonationDetailsPage
                from kivy.uix.screenmanager import Screen
                
                # Get the screen manager
                sm = app.root
                
                # Remove the donation details screen if it exists
                if sm.has_screen('donation_details'):
                    sm.remove_widget(sm.get_screen('donation_details'))
                
                # Create the donation details screen
                details_screen = Screen(name='donation_details')
                details_screen.add_widget(DonationDetailsPage(image_path=image_source, title=title))
                sm.add_widget(details_screen)
                
                # Switch to the donation details screen
                sm.current = 'donation_details'
            except ImportError:
                print("Could not load donation_details_page.py")

    def on_qr_code_press(self, instance):
        """Handle QR code button press in batchmates widget"""
        print("QR code pressed - navigating to QR scanner")
        # You can implement navigation to a QR scanner screen here
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Handle tab switching with MDBottomNavigation signature"""
        print(f"Tab switched to: {tab_text} (name: {instance_tab.name})")
        
        # Update current tab when user switches tabs
        if hasattr(instance_tab, 'name'):
            AlumniDirectoryPage.current_tab = instance_tab.name
        
        # Show settings button only when on profile tab
        is_profile = instance_tab.name == 'profile'
        print(f"Is profile tab? {is_profile}")
        self.header.show_settings_button(is_profile)
    
    def on_pre_enter(self):
        """Called when screen is about to become visible"""
        # Restore the previous tab when returning to this screen
        if hasattr(self, 'bottom_nav'):
            # Schedule tab switch for the next frame to ensure proper rendering
            Clock.schedule_once(lambda dt: self.set_active_tab(AlumniDirectoryPage.current_tab), 0)
    
    def set_active_tab(self, tab_name):
        """Set the active tab by name - called after returning from settings"""
        if hasattr(self, 'bottom_nav') and tab_name:
            try:
                self.bottom_nav.switch_tab(tab_name)
                print(f"Restored tab: {tab_name}")
            except:
                print(f"Could not switch to tab: {tab_name}")
    
    def filter_donations(self, search_text):
        """Filter donation widgets based on search text"""
        search_text = search_text.lower()
        
        # Show all donations if search text is empty
        if not search_text:
            for widget in self.donation_widgets.values():
                widget.opacity = 1
                widget.height = widget.normal_height if hasattr(widget, 'normal_height') else dp(380)
                widget.disabled = False
            return
        
        # Check each donation widget for matches
        for key, widget in self.donation_widgets.items():
            # Store normal height if not already stored
            if not hasattr(widget, 'normal_height'):
                widget.normal_height = widget.height
            
            # Check if search text is in the donation title
            if search_text in key.lower():
                # Show matching widget
                widget.opacity = 1
                widget.height = widget.normal_height
                widget.disabled = False
            else:
                # Hide non-matching widget
                widget.opacity = 0
                widget.height = 0
                widget.disabled = True
    
    def _update_rect(self, instance, value):
        """Update background rectangle on size/position change"""
        self.rect.pos = self.pos
        self.rect.size = self.size

# Import the LoginScreen from the main app
try:
    from login_page import LoginScreen
    from signup_page import SignupScreen  # Add signup screen import
except ImportError:
    # Define a simple LoginScreen if import fails
    class LoginScreen(Screen):
        """Simple login screen for standalone mode"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
            
            # Header
            header = Label(
                text="Santisimo Rosario Integrated Highschool",
                font_size=sp(20),
                color=TEAL_COLOR,
                size_hint_y=None,
                height=dp(50),
                bold=True
            )
            layout.add_widget(header)
            
            # Login button to return to alumni directory
            login_btn = Button(
                text="Login",
                size_hint=(None, None),
                size=(dp(200), dp(50)),
                pos_hint={'center_x': 0.5},
                background_normal='',
                background_color=TEAL_COLOR,
                color=WHITE_COLOR
            )
            login_btn.bind(on_press=lambda x: setattr(self.parent, 'current', 'alumni_directory'))
            layout.add_widget(Widget(size_hint_y=1))  # Spacer
            layout.add_widget(login_btn)
            layout.add_widget(Widget(size_hint_y=1))  # Spacer
            
            self.add_widget(layout)
    
    # Define a simple SignupScreen if import fails
    class SignupScreen(Screen):
        """Simple signup screen for standalone mode"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
            
            # Header
            header = Label(
                text="Create Account",
                font_size=sp(24),
                color=TEAL_COLOR,
                size_hint_y=None,
                height=dp(50),
                bold=True
            )
            layout.add_widget(header)
            
            # Form fields (simplified for demo)
            name_input = TextInput(
                hint_text="Full Name",
                size_hint_y=None,
                height=dp(40),
                multiline=False
            )
            layout.add_widget(name_input)
            
            email_input = TextInput(
                hint_text="Email Address",
                size_hint_y=None,
                height=dp(40),
                multiline=False
            )
            layout.add_widget(email_input)
            
            password_input = TextInput(
                hint_text="Password",
                size_hint_y=None,
                height=dp(40),
                multiline=False,
                password=True
            )
            layout.add_widget(password_input)
            
            # Signup button
            signup_btn = Button(
                text="Sign Up",
                size_hint=(None, None),
                size=(dp(200), dp(50)),
                pos_hint={'center_x': 0.5},
                background_normal='',
                background_color=TEAL_COLOR,
                color=WHITE_COLOR
            )
            signup_btn.bind(on_press=lambda x: setattr(self.parent, 'current', 'alumni_directory'))
            
            # Back to login button
            back_btn = Button(
                text="Back to Login",
                size_hint=(None, None),
                size=(dp(150), dp(40)),
                pos_hint={'center_x': 0.5},
                background_normal='',
                background_color=(0.7, 0.7, 0.7, 1),
                color=WHITE_COLOR
            )
            back_btn.bind(on_press=lambda x: setattr(self.parent, 'current', 'login'))
            
            layout.add_widget(Widget(size_hint_y=0.5))  # Spacer
            layout.add_widget(signup_btn)
            layout.add_widget(back_btn)
            layout.add_widget(Widget(size_hint_y=1))  # Spacer
            
            self.add_widget(layout)

class AlumniDirectoryApp(MDApp):
    """Main application class"""
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        
        # Add the login screen first
        sm.add_widget(LoginScreen(name='login'))
        
        # Add the signup screen
        sm.add_widget(SignupScreen(name='signup'))
        
        # Add the alumni directory screen
        sm.add_widget(AlumniDirectoryPage(name='alumni_directory'))
        
        # Add the settings screen
        sm.add_widget(SettingsPage(name='settings'))
        
        return sm
    
    def show_signup_screen(self):
        """Navigate to the signup screen"""
        # Get the screen manager
        sm = self.root
        
        # Navigate to signup page
        if sm.has_screen('signup'):
            sm.current = 'signup'
            print("Navigated to signup screen")
        else:
            print("Signup screen not found")
    
    def show_login_screen(self):
        """Navigate to the login screen"""
        # Get the screen manager
        sm = self.root
        
        # Navigate to login page
        if sm.has_screen('login'):
            sm.current = 'login'
            print("Navigated to login screen")
        else:
            print("Login screen not found")
    
    def show_donation_details(self, image_source, title):
        """Show the donation details page"""
        try:
            from donation_details_page import DonationDetailsPage
            
            # Get the screen manager
            sm = self.root
            
            # Remove the donation details screen if it exists
            if sm.has_screen('donation_details'):
                sm.remove_widget(sm.get_screen('donation_details'))
            
            # Create the donation details screen
            details_screen = Screen(name='donation_details')
            details_screen.add_widget(DonationDetailsPage(image_path=image_source, title=title))
            sm.add_widget(details_screen)
            
            # Switch to the donation details screen
            sm.current = 'donation_details'
        except ImportError:
            print("Could not load donation_details_page.py")
    
    def go_back(self):
        """Go back to the alumni directory page from donation details"""
        # Get the screen manager
        sm = self.root
        
        # Navigate back to alumni directory page
        sm.current = 'alumni_directory'
        print("Returned to alumni directory page")
    
    def go_back_to_details(self):
        """Go back from donation amount page to donation details page"""
        # Get the screen manager
        sm = self.root
        
        # Check if donation_details screen exists
        if sm.has_screen('donation_details'):
            # Navigate back to donation details page
            sm.current = 'donation_details'
            print("Returned to donation details page")
        else:
            # Fallback to alumni directory if details page doesn't exist
            sm.current = 'alumni_directory'
            print("Donation details page not found, returned to alumni directory")
    
    def show_donation_amount(self, image_source, title):
        """Show the donation amount input screen/dialog"""
        try:
            # Import the donation amount page if it exists
            try:
                from donation_amount_page import DonationAmountPage
                
                # Get the screen manager
                sm = self.root
                
                # Remove the previous screen if it exists
                if sm.has_screen('donation_amount'):
                    sm.remove_widget(sm.get_screen('donation_amount'))
                
                # Create and add the donation amount screen
                amount_screen = Screen(name='donation_amount')
                amount_screen.add_widget(DonationAmountPage(image_path=image_source, title=title))
                sm.add_widget(amount_screen)
                
                # Switch to the donation amount screen
                sm.current = 'donation_amount'
            except ImportError:
                # Fallback: Create a simple dialog if the page doesn't exist
                print(f"Donation amount requested for: {title}")
                # You might want to add a simple dialog here in the future
                
        except Exception as e:
            print(f"Error showing donation amount page: {e}")
    
    def show_settings_page(self):
        """Show the settings page"""
        # Get the screen manager
        sm = self.root
        
        # Navigate to settings page
        if sm.has_screen('settings'):
            sm.current = 'settings'
            print("Navigated to settings page")
        else:
            print("Settings screen not found")
    
if __name__ == "__main__":
    AlumniDirectoryApp().run()
