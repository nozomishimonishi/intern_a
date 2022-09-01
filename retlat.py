import geocoder

def retlat(zyusho):
    address = str(zyusho)
    ret = geocoder.osm(address, timeout=5.0)
    return [ret.latlng]

# retlat('埼玉県川越市脇田本町')