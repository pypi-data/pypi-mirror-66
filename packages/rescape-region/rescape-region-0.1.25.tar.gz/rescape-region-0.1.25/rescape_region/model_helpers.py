from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rescape_python_helpers import ewkt_from_feature
from rescape_python_helpers.geospatial.geometry_helpers import ewkt_from_feature_collection


def geos_feature_geometry_default():
    """
    The default geometry is a polygon of the earth's extent
    :return:
    """
    return ewkt_from_feature(
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon", "coordinates": [[[-85, -180], [85, -180], [85, 180], [-85, 180], [-85, -180]]]
            }
        }
    )


def geos_feature_collection_geometry_default():
    """
        Default FeatureCollection as ewkt representing the entire world
    :return:
    """
    return ewkt_from_feature_collection(
        feature_collection_default()
    )


def feature_collection_default():
    return {
        'type': 'FeatureCollection',
        'features': [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon", "coordinates": [[[-85, -180], [85, -180], [85, 180], [-85, 180], [-85, -180]]]
            }
        }]
    }


def region_data_default():
    return dict(locations=dict(params=[dict(
        country="ENTER A COUNTRY OR REMOVE THIS KEY/VALUE",
        state="ENTER A STATE/PROVINCE ABBREVIATION OR REMOVE THIS KEY/VALUE",
        city="ENTER A CITY OR REMOVE THIS KEY/VALUE",
        neighborhood="ENTER A NEIGHBORHOOD OR REMOVE THIS KEY/VALUE",
        blockname="ENTER A BLOCKNAME OR REMOVE THIS KEY/VALUE"
    )]))


def project_data_default():
    return dict()


def user_state_data_default():
    return dict(
        userRegions=[]
    )


def group_state_data_default():
    return dict()


def get_region_model():
    """
    Uses the same technique as get_user_model() to get the current region model from settings
    :return:
    """
    try:
        return apps.get_model(settings.REGION_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("REGION_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "REGION_MODEL refers to model '%s' that has not been installed" % settings.REGION_MODEL
        )

def get_project_model():
    """
    Uses the same technique as get_user_model() to get the current project model from settings
    :return:
    """
    try:
        return apps.get_model(settings.PROJECT_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PROJECT_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "PROJECT_USER_MODEL refers to model '%s' that has not been installed" % settings.PROJECT_MODEL
        )

def get_location_model():
    """
    Uses the same technique as get_user_model() to get the current location model from settings
    :return:
    """
    try:
        return apps.get_model(settings.LOCATION_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("LOCATION_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "LOCATION_MODEL refers to model '%s' that has not been installed" % settings.LOCATION_MODEL
        )
