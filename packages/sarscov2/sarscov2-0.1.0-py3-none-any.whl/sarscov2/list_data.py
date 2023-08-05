from edc_constants.constants import OTHER, UNKNOWN, DEAD, NONE
from edc_list_data import PreloadData


list_data = {
    "sarscov2.coronakapinformationsources": [
        ("local_news", "Local news (papers, radio, television)"),
        ("social_media", "Social media (Facebook, WhatsApp, etc)"),
        ("family_friends", "Family, Friends and neighbours"),
        ("international_news", "International news (papers, radio, television)"),
        (OTHER, "Other, please specify ..."),
    ],
}

preload_data = PreloadData(list_data=list_data)
