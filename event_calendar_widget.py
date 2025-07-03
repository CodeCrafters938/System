from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget  # Add missing Widget import
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.clock import Clock
from pathlib import Path
import os
import calendar
from datetime import datetime, date

# Add import for event details page and Screen
from event_details_page import EventDetailsPage
from kivy.uix.screenmanager import Screen

# Colors from the image
TEAL_COLOR = (26/255, 164/255, 159/255, 1)  # #1AA49F
WHITE_COLOR = (1, 1, 1, 1)
GRAY_COLOR = (0.9, 0.9, 0.9, 1)
LIGHT_GRAY_COLOR = (0.95, 0.95, 0.95, 1)
DARK_TEXT_COLOR = (0.2, 0.2, 0.2, 1)
LIGHT_TEXT_COLOR = (0.5, 0.5, 0.5, 1)
BLUE_COLOR = (0/255, 122/255, 255/255, 1)  # Blue for selected date

# Path to assets
ASSETS_PATH = Path(__file__).parent / Path(r"build\assets\frame9")

class CalendarCell(Button):
    """A single day cell in the calendar grid"""
    def __init__(self, day, month, year, has_event=False, current_month=True, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.month = month
        self.year = year
        self.has_event = has_event
        
        # Text for the button is the day number
        self.text = str(day) if day > 0 else ""
        
        # Style settings
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.font_size = sp(16)
        self.color = DARK_TEXT_COLOR if current_month else LIGHT_TEXT_COLOR
        
        # Highlight dates with events
        if has_event and day > 0:
            with self.canvas.before:
                Color(*TEAL_COLOR, 0.2)  # Light teal background for dates with events
                self.highlight = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_highlight, size=self._update_highlight)
    
    def _update_highlight(self, instance, value):
        if hasattr(self, 'highlight'):
            self.highlight.pos = self.pos
            self.highlight.size = self.size
    
    def select(self):
        """Highlight this cell when selected"""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*BLUE_COLOR, 0.2)  # Light blue for selected date
            self.highlight = Rectangle(pos=self.pos, size=self.size)
        self.color = BLUE_COLOR
        
    def deselect(self):
        """Remove highlight when not selected"""
        self.canvas.before.clear()
        if self.has_event and self.day > 0:
            with self.canvas.before:
                Color(*TEAL_COLOR, 0.2)  # Restore light teal for dates with events
                self.highlight = Rectangle(pos=self.pos, size=self.size)
        self.color = DARK_TEXT_COLOR

class CalendarWidget(BoxLayout):
    """Widget displaying a monthly calendar"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(330)  # Calendar height based on image
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        self.spacing = dp(5)
        
        # Get current date
        today = datetime.now()
        # Initialize with December 2025 for Winter Sports Meet example
        self.current_year = 2025
        self.current_month = 12
        self.selected_day = 21
        self.selected_cell = None
        
        # Sample event dates for demonstration - updated to match image
        self.event_dates = {
            # Format: (year, month, day): event_count
            (2025, 12, 21): 1,  # Winter Sports Meet on December 21, 2025
        }
        
        # Month and year header with navigation buttons
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )
        
        # Previous month button
        self.prev_month_btn = Button(
            text="<",
            font_size=sp(18),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=DARK_TEXT_COLOR,
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        self.prev_month_btn.bind(on_press=self.on_prev_month)
        self.header.add_widget(self.prev_month_btn)
        
        # Month and year label
        self.month_label = Label(
            text=f"{calendar.month_name[self.current_month]} {self.current_year}",
            font_size=sp(18),
            color=DARK_TEXT_COLOR,
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        self.header.add_widget(self.month_label)
        
        # Next month button
        self.next_month_btn = Button(
            text=">",
            font_size=sp(18),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=DARK_TEXT_COLOR,
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        self.next_month_btn.bind(on_press=self.on_next_month)
        self.header.add_widget(self.next_month_btn)
        
        self.add_widget(self.header)
        
        # Weekday headers (Mo, Tu, We...)
        self.weekdays = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        
        weekday_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for day in weekday_names:
            label = Label(
                text=day,
                font_size=sp(14),
                color=LIGHT_TEXT_COLOR,
                size_hint_x=1/7
            )
            self.weekdays.add_widget(label)
        
        self.add_widget(self.weekdays)
        
        # Calendar grid (will be populated in build_calendar)
        self.calendar_grid = GridLayout(
            cols=7,
            spacing=(0, 0),
            size_hint=(1, None),
            height=dp(240)
        )
        self.add_widget(self.calendar_grid)
        
        # Build the initial calendar
        self.build_calendar()
    
    def build_calendar(self):
        """Build the calendar grid for the current month"""
        # Clear previous calendar
        self.calendar_grid.clear_widgets()
        self.selected_cell = None
        
        # Update month label
        self.month_label.text = f"{calendar.month_name[self.current_month]} {self.current_year}"
        
        # Get the matrix representation of the month
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Add day cells to the grid
        for week in cal:
            for day in week:
                if day == 0:
                    # Empty cell for padding days
                    cell = CalendarCell(0, self.current_month, self.current_year, current_month=False)
                else:
                    # Check if this date has any events
                    has_event = (self.current_year, self.current_month, day) in self.event_dates
                    
                    # Create the day cell
                    cell = CalendarCell(
                        day, 
                        self.current_month, 
                        self.current_year,
                        has_event=has_event
                    )
                    
                    # Bind click event
                    cell.bind(on_press=self.on_day_selected)
                    
                    # Select today's date initially
                    if day == self.selected_day and self.current_month == 12 and self.current_year == 2025:
                        cell.select()
                        self.selected_cell = cell
                
                self.calendar_grid.add_widget(cell)
    
    def on_day_selected(self, instance):
        """Handle selection of a day in the calendar"""
        # Deselect previous selection if any
        if self.selected_cell:
            self.selected_cell.deselect()
        
        # Select new cell
        instance.select()
        self.selected_cell = instance
        self.selected_day = instance.day
        
        # Update the event list (via a callback)
        if hasattr(self, 'on_date_selected') and self.on_date_selected:
            self.on_date_selected(instance.day, instance.month, instance.year)
    
    def on_prev_month(self, instance):
        """Go to previous month"""
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.build_calendar()
    
    def on_next_month(self, instance):
        """Go to next month"""
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.build_calendar()
    
    def set_date_selected_callback(self, callback):
        """Set the callback function for when a date is selected"""
        self.on_date_selected = callback

class EventCard(BoxLayout):
    """Card displaying an event from the calendar"""
    def __init__(self, title, is_selected=False, has_border=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        
        # Background with optional border
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
            
            # Add border if specified
            if has_border:
                Color(*BLUE_COLOR)
                self.border = Line(
                    rounded_rectangle=(
                        self.pos[0], self.pos[1],
                        self.size[0], self.size[1],
                        dp(5)
                    ),
                    width=dp(1)
                )
            
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        
        # Event title
        self.title = Label(
            text=title,
            font_size=sp(16),
            color=DARK_TEXT_COLOR,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(50),
            text_size=(self.width - dp(30), None)
        )
        self.title.bind(width=lambda instance, width: 
                       setattr(instance, 'text_size', (width - dp(30), None)))
        self.add_widget(self.title)
    
    def _update_canvas(self, instance, value):
        """Update background and border when size changes"""
        self.bg.pos = self.pos
        self.bg.size = self.size
        if hasattr(self, 'border'):
            self.border.rounded_rectangle = (
                self.pos[0], self.pos[1],
                self.size[0], self.size[1],
                dp(5)
            )
    
    def select(self):
        """Highlight this event when selected"""
        with self.canvas.before:
            Color(*BLUE_COLOR)
            self.border = Line(
                rounded_rectangle=(
                    self.pos[0], self.pos[1],
                    self.size[0], self.size[1],
                    dp(5)
                ),
                width=dp(1)
            )
    
    def deselect(self):
        """Remove highlight when not selected"""
        if hasattr(self, 'border'):
            self.canvas.before.remove(self.border)

class EventList(ScrollView):
    """Scrollable list of events"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = dp(240)  # Will be adjusted based on window size
        
        # Container for events
        self.event_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        self.event_layout.bind(minimum_height=self.event_layout.setter('height'))
        
        self.add_widget(self.event_layout)
        
        # Keep track of events and selected event
        self.events = []
        self.selected_event = None
        
        # Sample events - updated to match the image
        self.sample_events = {
            # Format: (year, month, day): [event_titles]
            (2025, 12, 21): ["Winter Sports Meet to be held on 20th August"],
        }
        
        # Load default events (December 21, 2025)
        self.update_events(21, 12, 2025)
    
    def update_events(self, day, month, year):
        """Update the event list for the selected date"""
        # Clear previous events
        self.event_layout.clear_widgets()
        self.events = []
        self.selected_event = None
        
        # Title for events section - fixed spelling and styling
        events_title = Label(
            text="Upcoming Events",
            font_size=sp(20),
            color=DARK_TEXT_COLOR,
            bold=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(40),
            text_size=(self.width - dp(20), None)
        )
        events_title.bind(width=lambda instance, width: 
                 setattr(instance, 'text_size', (width - dp(20), None)))
        
        self.event_layout.add_widget(events_title)
        
        # Check if there are events for this date
        date_key = (year, month, day)
        if date_key in self.sample_events:
            for event_title in self.sample_events[date_key]:
                # Check if this is the Winter Sports Meet event
                is_sports_meet = "Winter Sports Meet" in event_title
                
                event_card = EventCard(
                    event_title,
                    has_border=is_sports_meet,  # Add border to Winter Sports Meet
                    is_selected=is_sports_meet,  # Set as selected by default
                    size_hint_y=None,
                    height=dp(70)
                )
                event_card.bind(on_touch_down=lambda instance, touch, card=event_card: 
                               self.on_event_selected(card, touch))
                self.event_layout.add_widget(event_card)
                self.events.append(event_card)
                
                # If this is the Winter Sports Meet, set it as selected
                if is_sports_meet:
                    self.selected_event = event_card
                    # Enable attendance buttons
                    if hasattr(self, 'on_event_selected_callback') and self.on_event_selected_callback:
                        self.on_event_selected_callback(True)
        else:
            # No events for this date
            no_events = Label(
                text="No events scheduled for this date.",
                font_size=sp(16),
                color=LIGHT_TEXT_COLOR,
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=dp(100)
            )
            self.event_layout.add_widget(no_events)
        
        # Update layout height
        self.event_layout.height = sum(child.height for child in self.event_layout.children) + \
                                 self.event_layout.spacing * (len(self.event_layout.children) - 1) + \
                                 self.event_layout.padding[1] + self.event_layout.padding[3]
    
    def on_event_selected(self, event_card, touch):
        """Handle selection of an event"""
        if event_card.collide_point(*touch.pos):
            # Deselect previous selection
            if self.selected_event:
                self.selected_event.deselect()
            
            # Select new event
            event_card.select()
            self.selected_event = event_card
            
            # Navigate to event details page
            from kivy.app import App
            app = App.get_running_app()
            
            # Check if we're using a ScreenManager
            if hasattr(app.root, 'current') and hasattr(app.root, 'add_widget'):
                # We're using a ScreenManager - create a Screen wrapper
                if not app.root.has_screen('event_details'):
                    event_details_screen = Screen(name='event_details')
                    event_details_page = EventDetailsPage()
                    event_details_screen.add_widget(event_details_page)
                    app.root.add_widget(event_details_screen)
                
                # Switch to the event details screen
                app.root.current = 'event_details'
            else:
                # Fallback for non-ScreenManager apps
                app.root.clear_widgets()
                event_details = EventDetailsPage()
                app.root.add_widget(event_details)
            
            # Enable attendance buttons (if they exist)
            if hasattr(self, 'on_event_selected_callback') and self.on_event_selected_callback:
                self.on_event_selected_callback(True)
    
    def set_event_selected_callback(self, callback):
        """Set callback for when an event is selected"""
        self.on_event_selected_callback = callback

class AttendanceButtons(BoxLayout):
    """Buttons to respond to event attendance"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(20), dp(10), dp(20), dp(10)]
        self.spacing = dp(20)
        
        # Initially disabled until an event is selected
        self.enabled = False
        
        # Attend button - improved visibility
        self.attend_btn = Button(
            text="Attend",
            font_size=sp(18),
            background_normal='',
            background_color=TEAL_COLOR,
            color=WHITE_COLOR,
            size_hint_x=0.5,
            disabled=False,
            opacity=1.0
        )
        
        # Add rounded corners
        with self.attend_btn.canvas.before:
            Color(*TEAL_COLOR)
            self.attend_bg = RoundedRectangle(
                pos=self.attend_btn.pos,
                size=self.attend_btn.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.attend_btn.bind(pos=self._update_attend_bg, size=self._update_attend_bg)
        self.attend_btn.bind(on_press=self.on_attend)
        self.add_widget(self.attend_btn)
        
        # Not attending button - improved visibility
        self.not_attend_btn = Button(
            text="Not Attending",
            font_size=sp(18),
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            color=DARK_TEXT_COLOR,
            size_hint_x=0.5,
            disabled=False,
            opacity=1.0
        )
        
        # Add rounded corners
        with self.not_attend_btn.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.not_attend_bg = RoundedRectangle(
                pos=self.not_attend_btn.pos,
                size=self.not_attend_btn.size,
                radius=[dp(5), dp(5), dp(5), dp(5)]
            )
        self.not_attend_btn.bind(pos=self._update_not_attend_bg, size=self._update_not_attend_bg)
        self.not_attend_btn.bind(on_press=self.on_not_attend)
        self.add_widget(self.not_attend_btn)
    
    def _update_attend_bg(self, instance, value):
        """Update attend button background when size changes"""
        self.attend_bg.pos = instance.pos
        self.attend_bg.size = instance.size
    
    def _update_not_attend_bg(self, instance, value):
        """Update not attend button background when size changes"""
        self.not_attend_bg.pos = instance.pos
        self.not_attend_bg.size = instance.size
    
    def enable_buttons(self, enable=True):
        """Enable or disable attendance buttons"""
        self.enabled = enable
        # Always keep buttons visible for this example to match image
        self.attend_btn.disabled = False  
        self.not_attend_btn.disabled = False
        self.attend_btn.opacity = 1.0
        self.not_attend_btn.opacity = 1.0
    
    def on_attend(self, instance):
        """Handle attend button press"""
        print("User will attend the event")
        if hasattr(self, 'on_attend_callback') and self.on_attend_callback:
            self.on_attend_callback()
    
    def on_not_attend(self, instance):
        """Handle not attending button press"""
        print("User will not attend the event")
        if hasattr(self, 'on_not_attend_callback') and self.on_not_attend_callback:
            self.on_not_attend_callback()
    
    def set_callbacks(self, attend_callback=None, not_attend_callback=None):
        """Set callbacks for attendance buttons"""
        self.on_attend_callback = attend_callback
        self.on_not_attend_callback = not_attend_callback

class EventCalendarWidget(BoxLayout):
    """Complete event calendar widget combining all components"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(5), dp(20), dp(5), dp(5)]  # Reduced top padding from 250dp to 20dp
        self.spacing = dp(15)  # Reduced spacing from 35dp to 15dp
        
        # Background color
        with self.canvas.before:
            Color(*WHITE_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add a smaller spacer at the top
        spacer = Widget(size_hint_y=None, height=dp(20))  # Reduced from 280dp to 20dp
        self.add_widget(spacer)
        
        # Title label
        title = Label(
            text="Calendar", 
            font_size=sp(24),  # Slightly smaller font
            bold=True,
            color=DARK_TEXT_COLOR,
            size_hint_y=None,
            height=dp(40)  # Reduced from 60dp to 40dp
        )
        self.add_widget(title)
        
        # Add a smaller spacer for separation
        spacer2 = Widget(size_hint_y=None, height=dp(10))  # Reduced from 80dp to 10dp
        self.add_widget(spacer2)
        
        # Calendar widget - give it more space
        self.calendar = CalendarWidget(size_hint=(1, None), height=dp(350))  # Increased from 330dp to 350dp
        self.add_widget(self.calendar)
        
        # Add spacing before events list
        spacer3 = Widget(size_hint_y=None, height=dp(20))  # Add spacing between calendar and events
        self.add_widget(spacer3)
        
        # Event list - this will now be pushed down
        self.event_list = EventList(size_hint=(1, 1))
        self.add_widget(self.event_list)
        
        # NOTE: Attendance buttons removed as requested
        
        # Connect callbacks
        self.calendar.set_date_selected_callback(self.on_date_selected)
        self.event_list.set_event_selected_callback(self.on_event_selected)
        
        # We'll keep the callback methods for future use
    
    def _update_rect(self, instance, value):
        """Update background rectangle on size/position change"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_date_selected(self, day, month, year):
        """Handle date selection in calendar"""
        self.event_list.update_events(day, month, year)
        #self.attendance_buttons.enable_buttons(False)
        
        # Call user callback if set
        if hasattr(self, 'on_date_selected_callback') and self.on_date_selected_callback:
            self.on_date_selected_callback(day, month, year)
    
    def on_event_selected(self, selected):
        """Handle event selection"""
        # No longer need to enable/disable buttons since they've been removed
        
        # Call user callback if set
        if hasattr(self, 'on_event_selected_callback') and self.on_event_selected_callback:
            self.on_event_selected_callback(selected)
    
    def set_callbacks(self, date_selected=None, event_selected=None, attend=None, not_attend=None):
        """Set user callbacks for the widget events"""
        self.on_date_selected_callback = date_selected
        self.on_event_selected_callback = event_selected
        self.on_attend_callback = attend
        self.on_not_attend_callback = not_attend

# Example usage
class EventCalendarWidgetApp(App):
    """Test application to demonstrate the widget"""
    def build(self):
        widget = EventCalendarWidget()
        
        # You can set callbacks like this:
        widget.set_callbacks(
            date_selected=lambda day, month, year: print(f"Date selected: {day}/{month}/{year}"),
            event_selected=lambda selected: print(f"Event selected: {selected}"),
            attend=lambda: print("User clicked Attend"),
            not_attend=lambda: print("User clicked Not Attending")
        )
        
        return widget

if __name__ == "__main__":
    EventCalendarWidgetApp().run()
