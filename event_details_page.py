from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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
from datetime import datetime

# Device profile constants
DEVICE_PROFILES = {
    'small': {'width': 392, 'height': 759},  # Match the image proportions
    'medium': {'width': 1080, 'height': 2340},  # Common smartphone size
}

# For mobile devices, let the system set the window size
if platform not in ('android', 'ios'):
    Window.size = (DEVICE_PROFILES['small']['width'], DEVICE_PROFILES['small']['height'])

# Colors from the image
TEAL_COLOR = (26/255, 164/255, 159/255, 1)  # #1AA49F
WHITE_COLOR = (1, 1, 1, 1)
GRAY_COLOR = (0.9, 0.9, 0.9, 1)
LIGHT_GRAY_COLOR = (0.95, 0.95, 0.95, 1)
DARK_TEXT_COLOR = (0.2, 0.2, 0.2, 1)
LIGHT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)
BLUE_COLOR = (0/255, 122/255, 255/255, 1)  # Blue for selected date
PURPLE_COLOR = (81/255, 45/255, 168/255, 1)  # Purple for event title

# Path to assets
ASSETS_PATH = Path(__file__).parent / Path(r"build\assets\frame11")
NAVIGATION_ICONS_PATH = Path(__file__).parent / Path(r"navigation_icons")

# Create assets directory if it doesn't exist
if not os.path.exists(ASSETS_PATH):
    os.makedirs(ASSETS_PATH)

# Create navigation_icons directory if it doesn't exist
if not os.path.exists(NAVIGATION_ICONS_PATH):
    os.makedirs(NAVIGATION_ICONS_PATH)

class HeaderBar(BoxLayout):
    """Teal header bar with title"""
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
        
        # Center - Event Calendar title
        self.title = Label(
            text="Event Calendar",
            font_size=sp(22),
            color=WHITE_COLOR,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            bold=True
        )
        self.add_widget(self.title)
        
        # Right - Empty space (settings button removed)
        spacer = Widget(size_hint=(None, None), width=dp(50))
        self.add_widget(spacer)
    
    def _update_rect(self, instance, value):
        """Update background when size changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size

class EventDetailsContent(BoxLayout):
    """Fixed content area for event details with responsive layout"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(10), dp(15), dp(15)]
        self.spacing = dp(15)  # Increased spacing to prevent overlap
        
        # Back button at the top-left with teal color exactly like donation details page
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
        
        # Event image with proper sizing
        event_image_path = os.path.join(ASSETS_PATH, "image_2.png")
        self.event_image = Image(
            source=event_image_path if os.path.exists(event_image_path) else "",
            size_hint=(1, None),
            height=dp(200),  # Fixed height like donation page
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Round the corners of the image container
        with self.event_image.canvas.before:
            Color(1, 1, 1, 1)
            self.image_rect = RoundedRectangle(
                pos=self.event_image.pos,
                size=self.event_image.size,
                radius=[dp(10), dp(10), dp(10), dp(10)]
            )
        self.event_image.bind(pos=self._update_image_rect, size=self._update_image_rect)
        self.add_widget(self.event_image)
        
        # Add spacing between image and title
        self.add_widget(Widget(size_hint=(1, None), height=dp(5)))
        
        # Event title with proper positioning
        self.event_title = Label(
            text="Winter Sports Meet",
            font_size=sp(20),
            color=PURPLE_COLOR,
            halign='left',
            valign='middle',
            size_hint=(1, None),
            height=dp(50),
            bold=True,
            text_size=(Window.width - dp(40), None)
        )
        self.event_title.bind(width=lambda instance, width: 
                            setattr(instance, 'text_size', (width - dp(30), None)))
        self.add_widget(self.event_title)
        
        # Separator line
        self.separator = Widget(size_hint=(1, None), height=dp(1))
        with self.separator.canvas:
            Color(*LIGHT_TEXT_COLOR)
            Rectangle(pos=self.separator.pos, size=(Window.width - dp(30), dp(1)))
        self.separator.bind(pos=self._update_separator, size=self._update_separator)
        self.add_widget(self.separator)
        
        # Featured events section with proper spacing
        self.featured_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(150),  # Fixed height to prevent overlap
            spacing=dp(5)
        )
        
        self.featured_title = Label(
            text="Featured Events",
            font_size=sp(18),
            color=DARK_TEXT_COLOR,
            halign='left',
            size_hint=(1, None),
            height=dp(30),
            bold=True,
            text_size=(Window.width - dp(40), None)
        )
        self.featured_section.add_widget(self.featured_title)
        
        # Featured events in a vertical layout
        self.featured_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=dp(2)
        )
        
        featured_events = [
            "Badminton Tournament",
            "Volleyball Tournament", 
            "Track Events",
            "Basketball Tournament",
            "Marathon"
        ]
        
        for event in featured_events:
            event_label = Label(
                text=event,
                font_size=sp(14),  # Slightly smaller to fit better
                color=DARK_TEXT_COLOR,
                halign='left',
                valign='middle',
                size_hint=(1, None),
                height=dp(20),
                text_size=(Window.width - dp(40), None)
            )
            self.featured_layout.add_widget(event_label)
        
        self.featured_section.add_widget(self.featured_layout)
        self.add_widget(self.featured_section)
        
        # Date & Time section with proper spacing
        self.details_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(100),  # Fixed height to prevent overlap
            spacing=dp(5)
        )
        
        # Date row
        self.date_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        self.date_label = Label(
            text="Date",
            font_size=sp(16),
            color=PURPLE_COLOR,
            halign='left',
            valign='middle',
            size_hint_x=None,
            width=dp(100),
            bold=True,
            underline=True
        )
        self.date_row.add_widget(self.date_label)
        
        self.date_value = Label(
            text="21 December 2023",
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            halign='left',
            valign='middle',
            text_size=(Window.width - dp(130), None)
        )
        self.date_row.add_widget(self.date_value)
        self.details_section.add_widget(self.date_row)
        
        # Time row
        self.time_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        self.time_label = Label(
            text="Time",
            font_size=sp(16),
            color=PURPLE_COLOR,
            halign='left',
            valign='middle',
            size_hint_x=None,
            width=dp(100),
            bold=True,
            underline=True
        )
        self.time_row.add_widget(self.time_label)
        
        self.time_value = Label(
            text="9:30 AM Onwards",
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            halign='left',
            valign='middle',
            text_size=(Window.width - dp(130), None)
        )
        self.time_row.add_widget(self.time_value)
        self.details_section.add_widget(self.time_row)
        
        # Location row
        self.location_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        self.location_label = Label(
            text="Location",
            font_size=sp(16),
            color=PURPLE_COLOR,
            halign='left',
            valign='middle',
            size_hint_x=None,
            width=dp(100),
            bold=True,
            underline=True
        )
        self.location_row.add_widget(self.location_label)
        
        self.location_value = Label(
            text="Sports Ground",
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            halign='left',
            valign='middle',
            text_size=(Window.width - dp(130), None)
        )
        self.location_row.add_widget(self.location_value)
        self.details_section.add_widget(self.location_row)
        
        self.add_widget(self.details_section)
        
        # Add spacer to push everything up properly
        self.add_widget(Widget(size_hint=(1, 1)))
        
        # Bind window resize to update layout
        Window.bind(on_resize=self._adjust_layout)
    
    def on_back(self, instance):
        """Handle back button press - return to calendar page"""
        from kivy.app import App
        app = App.get_running_app()
        
        # Check if we're using a ScreenManager
        if hasattr(app.root, 'current') and hasattr(app.root, 'has_screen'):
            # We're using a ScreenManager - switch to the alumni directory screen
            if app.root.has_screen('alumni_directory'):
                app.root.current = 'alumni_directory'
            elif app.root.has_screen('event_calendar'):
                app.root.current = 'event_calendar'
            else:
                # Try to find the calendar screen by different names
                for screen_name in app.root.screen_names:
                    if 'calendar' in screen_name.lower() or 'event' in screen_name.lower() or 'alumni' in screen_name.lower():
                        app.root.current = screen_name
                        return
                
                # If no calendar screen found, go to the first screen
                if app.root.screen_names:
                    app.root.current = app.root.screen_names[0]
        else:
            # Fallback for non-ScreenManager apps
            try:
                from event_calendar_page import EventCalendarPage
                app.root.clear_widgets()
                app.root.add_widget(EventCalendarPage())
            except ImportError:
                print("Could not navigate back - event_calendar_page not found")

    def _adjust_layout(self, instance, width, height):
        """Adjust layout elements when window is resized"""
        # Update text size constraints
        self.event_title.text_size = (width - dp(40), None)
        self.date_value.text_size = (width - dp(130), None)
        self.time_value.text_size = (width - dp(130), None)
        self.location_value.text_size = (width - dp(130), None)
        
        # Update separator size
        with self.separator.canvas:
            self.separator.canvas.clear()
            Color(*LIGHT_TEXT_COLOR)
            Rectangle(pos=self.separator.pos, size=(width - dp(30), dp(1)))
    
    def _update_image_rect(self, instance, value):
        """Update image rounded rectangle when size changes"""
        self.image_rect.pos = instance.pos
        self.image_rect.size = instance.size
    
    def _update_separator(self, instance, value):
        """Update separator line when size/position changes"""
        with instance.canvas:
            instance.canvas.clear()
            Color(*LIGHT_TEXT_COLOR)
            Rectangle(pos=(instance.pos[0], instance.pos[1]), 
                    size=(Window.width - dp(30), dp(1)))

class EventDetailsPage(FloatLayout):
    """Main event details page layout"""
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
        
        # Add content with proper positioning (removed the old back button)
        self.content = EventDetailsContent(
            pos_hint={'x': 0, 'y': 0},
            size_hint=(1, 1 - self.header.height / Window.height)
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
            # Update content area size (no navigation bar anymore)
            header_ratio = self.header.height / self.height
            self.content.size_hint = (1, 1 - header_ratio)
    
    def _on_window_resize(self, instance, width, height):
        """Handle window resize by updating layout"""
        if height > 0:  # Avoid division by zero
            Clock.schedule_once(self._adjust_layout, 0.1)

class EventDetailsApp(App):
    """Main application class for testing"""
    def build(self):
        return EventDetailsPage()

if __name__ == "__main__":
    EventDetailsApp().run()
