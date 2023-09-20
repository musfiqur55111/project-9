from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from geopy.geocoders import Nominatim
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class MapViewApp(App):
    def build(self):
        # Create a layout to hold your name, left button, search box, search button, and map view
        root_layout = BoxLayout(orientation='vertical')

        # Create a layout for the name label at the top with a blue background
        name_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint=(1, None), height=70)
        
        # Create a blue background for the name label
        with name_layout.canvas.before:
            Color(0.3, 0.3, 0.8, 1)  # Background color (blue)
            self.name_background = Rectangle(pos=name_layout.pos, size=name_layout.size)
        
        name_label = Label(text="Musfiqur's World MapView App", size_hint=(1, 1), halign='center', font_size=46)
        name_layout.add_widget(name_label)
        
        # Bind the background size to the name layout size
        name_layout.bind(size=self.update_name_background_size)
        
        # Add the name layout to the root layout
        root_layout.add_widget(name_layout)

        # Create a layout to hold the search box and button
        search_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint=(1, None), height=70)
        self.text_input = TextInput(hint_text="Enter your country or city name", size_hint=(0.7, None), height=50)
        search_button = Button(text="Search", size_hint=(0.3, None), height=40)
        search_button.bind(on_release=self.on_search_button_press)

        search_layout.add_widget(self.text_input)
        search_layout.add_widget(search_button)

        # Add the search layout to the root layout
        root_layout.add_widget(search_layout)

        # Create a mapview with a higher initial zoom level
        self.mapview = MapView(zoom=10)

        # Add the map view to the root layout
        root_layout.add_widget(self.mapview)

        return root_layout

    def update_name_background_size(self, instance, value):
        # Update the background rectangle's size when the layout size changes
        self.name_background.size = instance.size

    def on_search_button_press(self, instance):
        # Get the user's input from the text input
        country_name = self.text_input.text

        # Use geolocator to convert the country name to latitude and longitude
        geolocator = Nominatim(user_agent="country_locator")
        location = geolocator.geocode(country_name)

        if location:
            # Update the map view's center and zoom level based on the coordinates of the selected country
            self.mapview.center_on(location.latitude, location.longitude)
            self.mapview.zoom = 6  # Set a higher zoom level when a country is selected

            # Add a marker for the capital of the selected country with a Kivy icon
            capital_marker = MapMarkerPopup(lat=location.latitude, lon=location.longitude)
            icon = Image(source='atlas://data/images/defaulttheme/checkbox_on')
            capital_marker.add_widget(icon)
            self.mapview.add_marker(capital_marker)

if __name__ == '__main__':
    MapViewApp().run()
