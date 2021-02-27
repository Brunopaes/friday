# -*- coding: utf-8 -*-
import googlemaps
import helpers


def geocoding(location):
    """This function geocodes a string location.

    Parameters
    ----------
    location : str
        String location.

    Returns
    -------
    geocoded_location : str
        Lat, Long coordinates.

    """
    response = googlemaps.Client(helpers.read_json(
        'settings/maps_settings.json'
    ).get('api_key')).geocode(location)

    return 'latitude: {lat:.4f}\nlongitude: {lng:.4f}'.format(
        **response[0].get('geometry').get('location')
    )


def geodecoding(location):
    """This function inverse geocodes a string location.

    Parameters
    ----------
    location : iterator
        Lat, Long coordinates.

    Returns
    -------
    formatted_address : str
        Location.

    """
    response = googlemaps.Client(helpers.read_json(
        'settings/maps_settings.json'
    ).get('api_key')).reverse_geocode((float(location[0]), float(location[1])))

    return response[0].get('formatted_address')
