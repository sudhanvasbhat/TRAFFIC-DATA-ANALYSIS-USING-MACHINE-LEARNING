from ._anvil_designer import intersectionsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.js
from anvil.js.window import mapboxgl, MapboxGeocoder
from .. import Global

class intersections(intersectionsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    for junction, location in Global.junction_location.items():
      self.from_junction.items.append(junction)
    self.from_junction.items = self.from_junction.items
    self.to_junction.items = self.from_junction.items



  def go_click(self, **event_args):
    # add code to reset the map
    if self.date_picker_1.date is None or self.to_junction.selected_value is None or self.from_junction.selected_value is None :
      anvil.alert("Please enter all parameters !!")
    else :
      from_loc = Global.junction_location[self.from_junction.selected_value]
      to_loc = Global.junction_location[self.to_junction.selected_value]

      self.mapbox.removeLayer('colour-line-layer')
      self.mapbox.removeLayer('colour-line-layer1')
      self.mapbox.removeLayer('colour-line-layer2')
      self.mapbox.removeLayer('start-marker')
      junction_traffic = anvil.server.call('run_prediction',self.date_picker_1.date)
      from_junction_colour = junction_traffic.get(self.from_junction.selected_value)
      to_junction_colour = junction_traffic.get(self.to_junction.selected_value)

      if from_junction_colour == to_junction_colour:
        self.mapbox.on('style.load',self.add_single_colour_line_between_coordinates(from_junction_colour))
      else:
        self.mapbox.on('style.load',self.add_multi_colour_line_between_coordinates(from_junction_colour,to_junction_colour))

  def on_map_style_load(self):
    for key, value in Global.junction_location.items():
      self.add_notification_layer(value, key)

  def add_notification_layer(self, location, junction_name):
    notification_layer_id = f'notification-layer-{junction_name}'
    modified_location = [location[0], location[1] - 0.0001]
    self.mapbox.addLayer({
        'id': notification_layer_id,
        'type': 'symbol',
        'source': {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': modified_location
                    },
                    'properties': {
                        'junction_name': junction_name,
                    }
                }]
            }
        },
        'layout': {
            'text-field': ['concat',
                           '   ',
                           ['get', 'junction_name']],
            'text-font': ['DIN Offc Pro Bold', 'Arial Unicode MS Bold'],
            'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
            'text-radial-offset': 0.5,
            'text-justify': 'auto',
            'text-size': 12
        },
        'paint': {
            'text-color': 'black'
        }
    })
  def from_junction_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_from_junction = self.from_junction.selected_value
    self.to_junction.items = []
    for junction, location in Global.junction_location.items():
      if junction != selected_from_junction:
        self.to_junction.items.append(junction)
    self.to_junction.items = self.to_junction.items


  # def to_junction_change(self, **event_args):
  #   """This method is called when an item is selected"""
  #   selected_from_junction = self.from_junction.selected_value
  #   selected_to_junction = self.to_junction.selected_value


  #   self.from_junction.items = []
  #   for junction, location in Global.junction_location.items():
  #     if junction != selected_to_junction:
  #       self.from_junction.items.append(junction)
  #   self.from_junction.items = self.from_junction.items
  #   self.from_junction.selected_value = selected_from_junction

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    mapboxgl.accessToken = Global.token_id
    #put the map in the spacer
    self.mapbox = mapboxgl.Map({'container': anvil.js.get_dom_node(self.spacer_1),
                                'style': 'mapbox://styles/mapbox/streets-v11', #use the standard Mapbox style
                                'center': [8.651119, 49.872398],
                                'zoom': 15})
    # Add easeTo to smoothly zoom in

    self.marker = None
    self.mapbox.on('style.load', lambda e: self.on_map_style_load())

  def add_single_colour_line_between_coordinates(self,selected_colour):

    response = self.get_route()
    route_geometry = response['routes'][0]['geometry']
    if not self.mapbox.getSource('colour-line'):
      self.mapbox.addSource('colour-line', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': route_geometry
            }
        })

    # Add a layer to style the line (red color)
      self.mapbox.addLayer({
        'id': 'colour-line-layer',
        'type': 'line',
        'source': 'colour-line',
        'layout': {'line-join': 'round', 'line-cap': 'round'},
        'paint': {'line-color': Global.colour[selected_colour], 'line-width': 5}
      })
    else:
        # Update the data of the existing source
      self.mapbox.getSource('colour-line').setData({
            'type': 'Feature',
            'geometry': route_geometry
        })
      self.mapbox.addLayer({
        'id': 'colour-line-layer',
        'type': 'line',
        'source': 'colour-line',
        'layout': {'line-join': 'round', 'line-cap': 'round'},
        'paint': {'line-color': Global.colour[selected_colour], 'line-width': 5}
      })

  def add_multi_colour_line_between_coordinates(self,from_colour,to_colour):

    response = self.get_route()
    route_geometry = response['routes'][0]['geometry']
    midpoint_index = len(route_geometry['coordinates']) // 2
    if len(route_geometry['coordinates']) == 2:
      midpoint_longitude = (route_geometry['coordinates'][0][0] + route_geometry['coordinates'][1][0]) / 2
      midpoint_latitude = (route_geometry['coordinates'][0][1] + route_geometry['coordinates'][1][1]) / 2
      midpoint_coord = (midpoint_longitude, midpoint_latitude)
      first_half_geometry = {
        'type': 'LineString',
        'coordinates': [route_geometry['coordinates'][0],midpoint_coord]
      }
      second_half_geometry = {
        'type': 'LineString',
        'coordinates': [midpoint_coord, route_geometry['coordinates'][1]]
      }
    else:
      first_half_geometry = {
        'type': 'LineString',
        'coordinates': route_geometry['coordinates'][:midpoint_index + 1]
      }
      second_half_geometry = {
        'type': 'LineString',
        'coordinates':  route_geometry['coordinates'][midpoint_index:]
      }

    if not (self.mapbox.getSource('colour-line1')) or not (self.mapbox.getSource('colour-line2')):
      self.mapbox.addSource('colour-line1', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': first_half_geometry
            }
        })
      self.mapbox.addSource('colour-line2', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': second_half_geometry
            }
        })
    else:
      self.mapbox.getSource('colour-line1').setData( {
                'type': 'Feature',
                'geometry': first_half_geometry
        })
      self.mapbox.getSource('colour-line2').setData({
                'type': 'Feature',
                'geometry': second_half_geometry
        })
    self.mapbox.addLayer({
        'id': 'colour-line-layer1',
        'type': 'line',
        'source': 'colour-line1',
        'layout': {'line-join': 'round', 'line-cap': 'round'},
        'paint': {'line-color': Global.colour[from_colour], 'line-width': 5}
    })

    #Add a layer to style the second half of the line in green
    self.mapbox.addLayer({
        'id': 'colour-line-layer2',
        'type': 'line',
        'source': 'colour-line2',
        'layout': {'line-join': 'round', 'line-cap': 'round'},
        'paint': {'line-color': Global.colour[to_colour], 'line-width': 5}
    })

  def get_route(self):


    start_coordinates = Global.junction_location[self.from_junction.selected_value]
    end_coordinates = Global.junction_location[self.to_junction.selected_value]
    if not (self.mapbox.getSource('starting_marker')):
      self.mapbox.addSource('starting_marker',{ 'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': start_coordinates
                    },
                   'properties': {
                        'junction_name': self.from_junction.selected_value  # Replace with the actual junction name
                    }
                }]
            }
      })
    else:
      self.mapbox.getSource('starting_marker').setData( {
                'type': 'Feature',
                'geometry': {
                        'type': 'Point',
                        'coordinates': start_coordinates
                    }
        })
    self.mapbox.addLayer({
        'id': 'start-marker',
        'type': 'circle',
        'source': 'starting_marker',
        'paint': {
            'circle-radius': 10,
            'circle-color': Global.elements_colours['start'],
            'circle-stroke-color': Global.elements_colours['start_outer'],
            'circle-stroke-width': 1
        }
    })
    popup = mapboxgl.Popup({'closeButton': False, 'closeOnClick': False})
    self.mapbox.on('mouseenter', 'start-marker', lambda e: popup.setLngLat(e['features'][0]['geometry']['coordinates']).setHTML(f'<div style="margin: -15px; padding: 5px; text-align: center; border-radius: 10px; border: 1px solid #000; background-color: #C0C6BA  !important;  filter: brightness(120%);color: black !important;">Junction Name:{self.from_junction.selected_value}</div>').addTo(self.mapbox))
    self.mapbox.on('mouseleave', 'start-marker', lambda e: popup.remove())
    if self.marker:
      self.marker.remove()
    self.marker = mapboxgl.Marker({'color': Global.elements_colours["end"]})
    self.marker.setLngLat(end_coordinates).addTo(self.mapbox)
    # Add click event to show popup with junction name
    popup = mapboxgl.Popup({'closeButton': False, 'closeOnClick': False})

    def handle_click(e):
      popup.setLngLat(end_coordinates).setHTML(
          f'<div style="margin: -15px; padding: 5px; text-align: center; border-radius: 10px; border: 1px solid #000; background-color: #C0C6BA  !important;  filter: brightness(120%);color: black !important;">Junction Name: {self.to_junction.selected_value}</div>').addTo(self.mapbox)
    def handle_click_leave(e):
      popup.setLngLat(end_coordinates).remove()
    self.marker.getElement().addEventListener('mouseenter', handle_click)
    self.marker.getElement().addEventListener('mouseleave', handle_click_leave)
     # Request directions from Mapbox Directions API bn
    response = anvil.http.request(
        f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coordinates[0]},{start_coordinates[1]};{end_coordinates[0]},{end_coordinates[1]}?geometries=geojson&access_token={Global.token_id}",
        json=True
    )
    focus_longitude = (start_coordinates[0] + end_coordinates[0]) / 2
    focus_latitude = (start_coordinates[1] + end_coordinates[1]) / 2
    focus_latitude = focus_latitude - 0.003 
    self.mapbox.setCenter([focus_longitude,focus_latitude])
    self.mapbox.setZoom(14.5)
    return(response)

    # response = requests.get(url)
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     raise Exception("Error fetching route data")
