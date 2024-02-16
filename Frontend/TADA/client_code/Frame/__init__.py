from ._anvil_designer import FrameTemplate
from anvil import *
import anvil.server
import anvil.users
from ..whole_map import whole_map
from ..intersections import intersections
import anvil.js
from anvil.js.window import mapboxgl, MapboxGeocoder

#This is your startup form. It has a sidebar with navigation links and a content panel where page content will be added.
class Frame(FrameTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    Plot.templates.default = "rally"
    self.content_panel.add_component(whole_map())
    self.whole_map.background = app.theme_colors['Primary Container']


  def whole_map_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(whole_map())
    self.whole_map.background = app.theme_colors['Primary Container']
    self.intersections.background = "transparent"


  def intersections_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(intersections())
    self.intersections.background = app.theme_colors['Primary Container']
    self.whole_map.background = "transparent"
