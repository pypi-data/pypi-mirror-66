from django.conf import settings

_PICSUM_DEFAULTS = {
    'url':"https://picsum.photos/"
}


_PIXABAY_DEFAULTS = {
    'url':"https://pixabay.com/api/",

}

def get_picsum_setting(name,default =None):
    """
    Returns the settings from  settings.py 
    """
    PICSUM = {}
    PICSUM.update(_PICSUM_DEFAULTS)
    PICSUM.update(getattr(settings,'PICSUM_CONF',_PICSUM_DEFAULTS))
    return PICSUM.get(name,default)


def get_pixabay_setting(name,default= None):
    PIXABAY ={}
    PIXABAY.update(_PIXABAY_DEFAULTS)
    key= getattr(settings,'PIXABAY_KEY')
    if not key :
        raise Exception("Key not found bitches")
    _PIXABAY_DEFAULTS['key'] =key      
    PIXABAY.update(getattr(settings,"PIXABAY_CONF",_PIXABAY_DEFAULTS))
    return PIXABAY.get(name,default) 

