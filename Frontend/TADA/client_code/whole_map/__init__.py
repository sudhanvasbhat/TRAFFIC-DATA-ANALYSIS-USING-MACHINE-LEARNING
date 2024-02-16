from ._anvil_designer import whole_mapTemplate
from anvil import *
import anvil.server
from anvil import GoogleMap, HtmlPanel
import anvil.js
from anvil.js.window import mapboxgl, MapboxGeocoder
from .. import Global

class whole_map(whole_mapTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)


  def go_click(self, **event_args):


    if self.date_picker_1.date is None:
      anvil.alert("Please select the date!!")
    else :
      junction_traffic = anvil.server.call('run_prediction',self.date_picker_1.date)
      # junction_traffic = anvil.server.call('run_prediction',"test")
      print("The junction traffic is - {0}".format(junction_traffic))
      for key, value in Global.junction_location.items():
        id_layer = f'color-layer-{key}'
        id_source = f'color-source-{key}'
        self.mapbox.removeLayer(id_layer)
        if key == "A006":
          outer_circle = 'black'
          info = "underground junction"
        else:
          outer_circle = 'white'
          info = "surface junction"
        circle_colour = Global.colour[junction_traffic[key]]
        self.add_circle(value, circle_colour,outer_circle,id_layer, id_source,key,info)
      # self.map_1.map_data.add(GoogleMap.Data.Feature(
      #   geometry=GoogleMap.Data.Point(
      #     GoogleMap.LatLng(49.8735034, 8.6504286))))
      # self.map_1.map_data.style = GoogleMap.Data.StyleOptions(
      #   icon=GoogleMap.Symbol(
      #     path=GoogleMap.SymbolPath.CIRCLE,
      #     scale=30,
      #     fill_color='red',
      #     fill_opacity=0.3,
      #     stroke_opacity=1,
      #     stroke_weight=1
      #     )
      #   )
# Add circles with traffic colour for each junction







  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    mapboxgl.accessToken = Global.token_id
    #put the map in the spacer
    self.mapbox = mapboxgl.Map({'container': anvil.js.get_dom_node(self.spacer_1),
                                'style': 'mapbox://styles/mapbox/streets-v11', #use the standard Mapbox style
                                'center': [8.651119, 49.872398],
                                'zoom': 1})
    self.mapbox.on('style.load', lambda e: self.on_map_style_load())
    self.mapbox.easeTo({'center': [8.651119, 49.872398], 'zoom': 15, 'duration': 1000})

  def on_map_style_load(self):
    for key, value in Global.junction_location.items():
      self.add_notification_layer(value, key)
  def add_circle(self, location, inner_circle, outer_circle,id_layer, id_source,junction_name,info):
    if not (self.mapbox.getSource(id_source)):
      self.mapbox.addSource(id_source, {
          'type': 'geojson',
          'data': {
              'type': 'FeatureCollection',
              'features': [{
                  'type': 'Feature',
                  'geometry': {
                      'type': 'Point',
                      'coordinates': location
                  }
              }]
          }
      })
    else:
      self.mapbox.getSource(id_source).setData( {
                'type': 'Feature',
                'geometry': {
                        'type': 'Point',
                        'coordinates': location
                    }
        })

    self.mapbox.addLayer({
            'id': id_layer,
            'type': 'circle',
            'source': id_source,
            'paint': {
                'circle-radius': 10,
                'circle-color': inner_circle,
                'circle-stroke-color': outer_circle,
                'circle-stroke-width': 2
            }
        })
    popup = mapboxgl.Popup({'closeButton': False, 'closeOnClick': False})
    self.mapbox.on('mouseenter', id_layer, lambda e: popup.setLngLat(location).setHTML(
                 f'<div style="margin: -15px; padding: 5px; text-align: center; border-radius: 10px; border: 1px solid #000; background-color: #C0C6BA  !important;  filter: brightness(120%);color: black !important;">Junction Name: {junction_name}<br>{info}</div>').addTo(self.mapbox))
    self.mapbox.on('mouseleave', id_layer, lambda e: popup.remove())

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
