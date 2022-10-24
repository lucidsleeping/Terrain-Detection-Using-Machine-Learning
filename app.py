from importlib.resources import read_binary
import re
from flask import *
import tensorflow as tf
import numpy as np
import os
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER

def mode(keywords):
    #offroad keys
    key1 = ['valley', 'thatch', 'dam', 'seashore', 'steel_arch_bridge', 'velvet', 'nematode', 'lemon', 'honeycomb', 'switch', 'valley', 'cliff', 'megalith', 'stone_wall', 'geyser', 'rapeseed', 'volcano', 'megalith', 'lakeside', 'geyser', 'red_fox', 'dhole', 'coyote', 'lynx', 'kit_fox', 'worm_fence', 'stone_wall', 'lakeside', 'maze', 'valley', 'rapeseed', 'sandbar', 'geyser', 'valley', 'seashore', 'overskirt', 'hoopskirt', 'cloak', 'volcano', 'gown', 'sandbar', 'seashore', 'Arabian_camel', 'geyser', 'lakeside', 'worm_fence', 'seashore', 'thatch', 'ear', 'lakeside', 'valley', 'cliff', 'volcano', 'megalith', 'alp', 'lakeside', 'alp', 'stone_wall', 'suspension_bridge', 'mountain_bike', 'cliff', 'Komodo_dragon', 'agama', 'cliff_dwelling', 'alp', 'alp', 'stone_wall', 'hay', 'volcano', 'worm_fence', 'worm_fence', 'barn', 'lakeside', 'megalith', 'rapeseed', 'hay', 'rapeseed', 'harvester', 'worm_fence', 'solar_dish', 'thresher', 'alp', 'monastery', 'gazelle', 'moving_van', 'cliff', 'promontory', 'valley', 'stone_wall', 'alp', 'beer_bottle', 'hay', 'wreck', 'mountain_bike', 'ear', 'fountain', 'geyser', 'baseball', 'spotlight', 'leatherback_turtle', 'thatch', 'alp', 'velvet', 'overskirt', 'isopod', 'golfcart', 'park_bench', 'mountain_tent', 'car_mirror', 'lumbermill', 'worm_fence', 'lakeside', 'electric_ray', 'valley', 'alp', 'volcano', 'hay', 'rapeseed', 'hourglass', 'geyser', 'mountain_tent', 'yurt', 'parachute', 'volcano', 'lakeside', 'rapeseed', 'steam_locomotive', 'harvester', 'car_mirror', 'traffic_light', 'cliff', 'valley', 'dam', 'worm_fence', 'seashore', 'valley', 'alp', 'cliff', 'seashore', 'volcano', 'worm_fence', 'maze', 'plow', 'harvester', 'head_cabbage', 'cliff', 'alp', 'hay', 'thresher', 'apiary', 'worm_fence', 'hartebeest', 'dam', 'lakeside', 'mountain_tent', 'alp', 'valley', 'maze', 'dam', 'lakeside', 'park_bench', 'ashcan', 'mountain_bike', 'mailbox', 'chainlink_fence', 'gown', 'geyser', 'sarong', 'hoopskirt', 'seashore', 'velvet', 'seashore', 'wood_rabbit', 'sidewinder', 'dingo', 'maze', 'stone_wall', 'worm_fence', 'chainlink_fence', 'megalith', 'maze', 'hay', 'valley', 'rapeseed', 'alp', 'geyser', 'alp', 'seashore', 'volcano', 'sandbar', 'cliff', 'valley', 'megalith', 'alp', 'promontory', 'harvester', 'snowplow', 'baboon', 'streetcar', 'tractor', 'velvet', 'prayer_rug', 'honeycomb', 'spaghetti_squash', 'leopard', 'curly-coated_retriever', 'Arabian_camel', 'African_elephant', 'tusker', 'black_grouse', 'volcano', 'geyser', 'dam', 'thatch', 'lumbermill', 'geyser', 'rapeseed', 'worm_fence', 'stone_wall', 'barn', 'sports_car', 'car_wheel', 'racer', 'convertible', 'tow_truck', 'hare', 'badger', 'tick', 'fox_squirrel', 'velvet', 'alp', 'seashore', 'stone_wall', 'valley', 'worm_fence', 'mountain_bike', 'maze', 'lakeside', 'patio', 'worm_fence', 'frilled_lizard', 'velvet', 'grey_whale', 'seashore', 'worm_fence', 'sandbar', 'worm_fence', 'hartebeest', 'thresher', 'Arabian_camel', 'maze', 'valley', 'suspension_bridge', 'stupa', 'viaduct', 'thresher', 'worm_fence', 'cheetah', 'Kerry_blue_terrier', 'chain_saw', 'stone_wall', 'worm_fence', 'maze', 'lakeside', 'chainlink_fence', 'thatch', 'hay', 'valley', 'dam', 'cliff', 'rapeseed', 'dam', 'alp', 'valley', 'worm_fence', 'snowplow', 'horse_cart', 'tractor', 'lumbermill', 'golfcart', 'lakeside', 'seashore', 'sandbar', 'rapeseed', 'hay', 'park_bench', 'lumbermill', 'valley', 'stone_wall', 'sarong', 'worm_fence', 'park_bench', 'valley', 'prayer_rug', 'maze', 'mountain_tent', 'paddlewheel', 'solar_dish', 'jinrikisha', 'dam', 'rapeseed', 'dam', 'valley', 'mountain_bike', 'hay', 'dam', 'broom', 'streetcar', 'volcano', 'thatch', 'velvet', 'nematode', 'corn', 'sandbar', 'mailbag', 'lakeside', 'maze', 'thatch', 'hay', 'sandbar', 'leatherback_turtle', 'geyser', 'badger', 'Angora', 'eggnog', 'stone_wall', 'maze', 'alp', 'worm_fence', 'valley', 'doormat', 'bath_towel', 'brass', 'manhole_cover', 'park_bench', 'sandbar', 'hartebeest', 'seashore', 'geyser', 'worm_fence', 'geyser', 'lakeside', 'sandbar', 'rapeseed', 'seashore', 'cliff', 'alp', 'geyser', 'volcano', 'agama', 'car_wheel', 'jeep', 'clog', 'barrow', 'cowboy_hat', 'valley', 'oxcart', 'mountain_bike', 'lakeside', 'jeep', 'worm_fence', 'stone_wall', 'lakeside', 'rapeseed', 'hay', 'wool', 'fountain', 'tennis_ball', 'breakwater', 'bannister', 'komondor', 'worm_fence', 'overskirt', 'sloth_bear', 'cloak', 'maze', 'seashore', 'sandbar', 'solar_dish', 'dam', 'stone_wall', 'chainlink_fence', 'maze', 'worm_fence', 'obelisk', 'cliff', 'maze', 'valley', 'promontory', 'stone_wall', 'shopping_cart', 'mountain_tent', 'street_sign', 'mailbox', 'plow', 'matchstick', 'spotlight', 'digital_clock', 'nematode', 'theater_curtain', 'valley', 'worm_fence', 'mountain_tent', 'volcano', 'alp', 'volcano', 'fountain', 'sandbar', 'yurt', 'cliff', 'volcano', 'geyser', 'thatch', 'dam', 'hay', 'jeep', 'snowplow', 'fire_engine', 'tow_truck', 'harvester', 'sandbar', 'volcano', 'rapeseed', 'worm_fence', 'geyser', 'cliff', 'megalith', 'valley', 'stone_wall', 'promontory', 'sports_car', 'car_wheel', 'racer', 'tow_truck', 'mountain_tent', 'trailer_truck', 'jeep', 'lawn_mower', 'minibus', 'racer', 'beacon', 'street_sign', 'flagpole', 'pole', 'stupa', 'alp', 'sandbar', 'maze', 'seashore', 'valley', 'lakeside', 'worm_fence', 'stone_wall', 'barn', 'maze', 'velvet', 'valley', 'wool', 'maze', 'poncho', 'hartebeest', 'worm_fence', 'safety_pin', 'cheetah', 'nematode', 'freight_car', 'rapeseed', 'steam_locomotive', 'worm_fence', 'harvester', 'thresher', 'komondor', 'chain', 'tricycle', 'sorrel', 'volcano', 'dam', 'thatch', 'worm_fence', 'overskirt', 'seashore', 'leatherback_turtle', 'hay', 'valley', 'volcano', 'worm_fence', 'horse_cart', 'lakeside', 'seashore', 'mountain_tent', 'cliff', 'sandbar', 'volcano', 'leatherback_turtle', 'breakwater', 'diamondback', 'sidewinder', 'safety_pin', 'horned_viper', 'gazelle', 'seashore', 'lakeside', 'valley', 'hay', 'mountain_bike', 'rapeseed', 'hay', 'harvester', 'sandbar', 'fountain', 'sandbar', 'seashore', 'leatherback_turtle', 'loggerhead', 'lakeside', 'dam', 'worm_fence', 'sarong', 'mountain_tent', 'frilled_lizard', 'lumbermill', 'ashcan', 'snowplow', 'plastic_bag', 'chain_saw', 'overskirt', 'hoopskirt', 'gown', 'volcano', 'thatch', 'sandbar', 'Arabian_camel', 'hay', 'megalith', 'sorrel', 'lakeside', 'valley', 'maze', 'alp', 'mountain_bike', 'jeep', 'racer', 'sandbar', 'bottlecap', 'leatherback_turtle', 'ox', 'water_buffalo', 'worm_fence', 'bison', 'freight_car', 'thatch', 'megalith', 'dam', 'alp', 'horse_cart', 'seashore', 'sandbar', 'geyser', 'valley', 'lakeside', 'electric_ray', 'platypus', 'common_newt', 'ant', 'nematode', 'seashore', 'sandbar', 'cliff', 'valley', 'promontory', 'overskirt', 'velvet', 'seashore', 'sarong', 'hoopskirt', 'valley', 'cliff', 'megalith', 'spider_web', 'komondor', 'megalith', 'cliff', 'alp', 'geyser', 'dam', 'plow', 'streetcar', 'trolleybus', 'street_sign', 'hay', 'maze', 'mountain_tent', 'park_bench', 'lakeside', 'chainlink_fence', 'barrel', 'mortar', 'volcano', 'cliff_dwelling', 'hay', 'volcano', 'hay', 'lakeside', 'aircraft_carrier', 'horse_cart', 'volcano', 'stone_wall', 'alp', 'megalith', 'worm_fence', 'geyser', 'worm_fence', 'alp', 'hatchet', 'ox', 'sandbar', 'seashore', 'lakeside', 'rapeseed', 'megalith', 'maze', 'cliff', 'valley', 'sandbar', 'alp', 'thresher', 'fox_squirrel', 'Irish_water_spaniel', 'baboon', 'worm_fence', 'broom', 'quilt', 'dam', 'overskirt', 'hen-of-the-woods', 'maze', 'valley', 'mountain_bike', 'sandbar', 'stone_wall', 'seashore', 'street_sign', 'sandbar', 'geyser', 'cliff', 'seashore', 'lakeside', 'sandbar', 'stone_wall', 'valley', 'worm_fence', 'soft-coated_wheaten_terrier', 'Sussex_spaniel', 'plow', 'wood_rabbit', 'jeep', 'harvester', 'snowplow', 'Arabian_camel', 'baboon', 'volcano', 'sandbar', 'valley', 'breakwater', 'diamondback']

    #onroad keys
    key2 = ['gown', 'bobsled', 'aircraft_carrier', 'stretcher', 'dome', 'passenger_car', 'pier', 'streetcar', 'steel_arch_bridge', 'bullet_train', 'umbrella', 'geyser', 'fountain', 'seashore', 'prayer_rug', 'suspension_bridge', 'mountain_tent', 'viaduct', 'wing', 'umbrella', 'cliff', 'volcano', 'alp', 'valley', 'car_mirror', 'crane', 'streetcar', 'submarine', 'drilling_platform', 'rubber_eraser', 'suspension_bridge', 'cloak', 'viaduct', 'jean', 'velvet', 'steel_arch_bridge', 'dam', 'seashore', 'aircraft_carrier', 'suspension_bridge', 'mountain_tent', 'geyser', 'alp', 'worm_fence', 'cloak', 'mountain_tent', 'church', 'cloak', 'worm_fence', 'canoe', 'monastery', 'worm_fence', 'alp', 'mobile_home', 'seashore', 'worm_fence', 'castle', 'church', 'palace', 'canoe', 'pier', 'suspension_bridge', 'radio_telescope', 'greenhouse', 'beacon', 'suspension_bridge', 'pier', 'streetcar', 'passenger_car', 'bullet_train', 'suspension_bridge', 'worm_fence', 'fountain', 'theater_curtain', 'maze', 'valley', 'cliff', 'suspension_bridge', 'dam', 'alp', 'seashore', 'lakeside', 'steel_arch_bridge', 'promontory', 'suspension_bridge', 'alp', 'valley', 'dam', 'volcano', 'mountain_tent', 'upright', 'spotlight', 'passenger_car', 'fountain', 'traffic_light', 'pier', 'dam', 'viaduct', 'steel_arch_bridge', 'suspension_bridge', 'mountain_tent', 'trailer_truck', 'seashore', 'volcano', 'plastic_bag', 'birdhouse', 'street_sign', 'space_shuttle', 'sundial', 'church', 'doormat', 'wallet', 'loudspeaker', 'mailbag', 'modem', 'cleaver', 'plane', 'hatchet', 'jersey', 'moving_van', 'drilling_platform', 'trailer_truck', 'submarine', 'crane', 'dock', 'pole', 'pier', 'crane', 'breakwater', 'flagpole', 'viaduct', 'suspension_bridge', 'steel_arch_bridge', 'trailer_truck', 'solar_dish', 'volcano', 'mountain_tent', 'wing', 'alp', 'hourglass', 'stage', 'submarine', 'pirate', 'sax', 'wreck', 'pier', 'streetcar', 'trailer_truck', 'passenger_car', 'bullet_train', 'fountain', 'suspension_bridge', 'rapeseed', 'obelisk', 'water_tower', 'dam', 'bullet_train', 'car_mirror', 'solar_dish', 'bobsled', 'seashore', 'mountain_tent', 'prayer_rug', 'maze', 'alp', 'dam', 'trailer_truck', 'bannister', 'upright', 'viaduct', 'trailer_truck', 'garbage_truck', 'snowplow', 'moving_van', 'tow_truck', 'suspension_bridge', 'pier', 'passenger_car', 'dam', 'mobile_home', 'beacon', 'stone_wall', 'triumphal_arch', 'mobile_home', 'street_sign', 'greenhouse', 'umbrella', 'freight_car', 'fountain', 'yurt', 'breakwater', 'volcano', 'stone_wall', 'greenhouse', 'maze', 'traffic_light', 'cab', 'streetcar', 'limousine', 'unicycle', 'dam', 'solar_dish', 'bobsled', 'canoe', 'passenger_car', 'trailer_truck', 'alp', 'radio_telescope', 'mountain_tent', 'solar_dish', 'street_sign', 'crash_helmet', 'football_helmet', 'parking_meter', 'soccer_ball', 'alp', 'valley', 'volcano', 'seashore', 'cliff', 'dam', 'sundial', 'suspension_bridge', 'patio', 'pier', 'iron', 'ocarina', 'rock_python', "potter's_wheel", 'sidewinder', 'sorrel', 'dam', 'steel_arch_bridge', 'breakwater', 'beacon', 'submarine', 'sax', 'steam_locomotive', 'electric_locomotive', 'bassoon', 'nematode', 'eel', 'vine_snake', 'thunder_snake', 'sidewinder', 'sandbar', 'seashore', 'container_ship', 'promontory', 'lakeside', 'trailer_truck', 'volcano', 'maypole', 'umbrella', 'mosquito_net', 'rapeseed', 'beacon', 'castle', 'trailer_truck', 'worm_fence', 'drilling_platform', 'space_shuttle', 'pirate', 'moving_van', 'container_ship', 'space_shuttle', 'street_sign', 'birdhouse', 'parallel_bars', 'matchstick', 'seat_belt', 'steel_arch_bridge', 'car_wheel', 'paddle', 'velvet', 'alp', 'valley', 'volcano', 'dam', 'cliff', 'dam', 'trailer_truck', 'viaduct', 'pier', 'car_wheel', 'unicycle', 'cliff', 'castle', 'suspension_bridge', 'promontory', 'steam_locomotive', 'freight_car', 'passenger_car', 'electric_locomotive', 'wing', 'worm_fence', 'patio', 'valley', 'maze', 'dam', 'pier', 'passenger_car', 'bannister', 'bullet_train', 'suspension_bridge', 'geyser', 'breakwater', 'castle', 'lakeside', 'steel_arch_bridge', 'dam', 'steel_arch_bridge', 'pier', 'viaduct', 'seashore', 'doormat', 'rubber_eraser', 'matchstick', 'wallet', 'rule', 'alp', 'valley', 'dam', 'cliff', 'seashore', 'traffic_light', 'spotlight', 'cab', 'streetcar', 'suspension_bridge', 'seashore', 'airliner', 'alp', 'promontory', 'wing', 'worm_fence', 'alp', 'lakeside', 'lumbermill', 'thresher', 'pole', 'flagpole', 'street_sign', 'lakeside', 'breakwater', 'passenger_car', 'freight_car', 'bullet_train', 'pier', 'electric_locomotive', 'street_sign', 'mailbox', 'dam', 'racer', 'park_bench', 'mountain_tent', 'rapeseed', 'worm_fence', 'pier', 'boathouse', 'bobsled', 'golfcart', 'patio', 'mountain_tent', 'solar_dish', 'acoustic_guitar', 'binder', 'corkscrew', 'book_jacket', 'lighter', 'mountain_tent', 'rapeseed', 'worm_fence', 'pier', 'boathouse', 'streetcar', 'bullet_train', 'passenger_car', 'trailer_truck', 'pier', 'doormat', 'wallet', 'oscilloscope', 'rule', 'loudspeaker', 'bullet_train', 'passenger_car', 'streetcar', 'submarine', 'electric_locomotive', 'rapeseed', 'trailer_truck', 'hay', 'volcano', 'umbrella', 'seashore', 'valley', 'promontory', 'volcano', 'cliff', 'pier', 'crane', 'flagpole', 'trailer_truck', 'passenger_car', 'alp', 'volcano', 'valley', 'vault', 'sleeping_bag', 'racket', 'passenger_car', 'mosquito_net', 'lacewing', 'damselfly', 'trailer_truck', 'volcano', 'umbrella', 'geyser', 'yurt', 'passenger_car', 'freight_car', 'bullet_train', 'electric_locomotive', 'theater_curtain', 'steel_arch_bridge', 'pier', 'seashore', 'dock', 'container_ship', 'seashore', 'promontory', 'cliff', 'planetarium', 'horse_cart', 'seashore', 'promontory', 'sandbar', 'dam', 'steel_arch_bridge', 'suspension_bridge', 'viaduct', 'trailer_truck', 'dam', 'umbrella', 'alp', 'valley', 'seashore', 'lakeside', 'volcano', 'analog_clock', 'hammer', 'rule', 'screw', 'modem', 'seashore', 'promontory', 'sandbar', 'lakeside', 'cliff', 'traffic_light', 'pier', 'scoreboard', 'bullet_train', 'trailer_truck', 'bobsled', 'bullet_train', 'bannister', 'dam', 'pier', 'rapeseed', 'volcano', 'umbrella', 'racer', 'breakwater', 'park_bench', 'bannister', 'jean', 'car_wheel', 'paintbrush', 'acoustic_guitar', 'traffic_light', 'joystick', 'hard_disc', 'flatworm', 'matchstick', 'spotlight', 'digital_clock', 'nematode', 'theater_curtain', 'patio', 'mosquito_net', 'suspension_bridge', 'worm_fence', 'park_bench', 'cliff', 'dam', 'worm_fence', 'valley', 'promontory', 'trailer_truck', 'mountain_tent', 'alp', 'canoe', 'pole', 'pole', 'maypole', 'trailer_truck', 'volcano', 'mountain_tent', 'theater_curtain', 'pier', 'passenger_car', 'velvet', 'pole', 'lakeside', 'suspension_bridge', 'worm_fence', 'geyser', 'viaduct', 'seashore', 'valley', 'promontory', 'alp', 'volcano', 'doormat', 'park_bench', 'wallet', 'rubber_eraser', 'buckle', 'traffic_light', 'cab', 'vault', 'palace', 'obelisk', 'flagpole', 'trimaran', 'airliner', 'pier', 'traffic_light', 'cash_machine', 'freight_car', 'balance_beam', 'file', 'limousine', 'hay', 'rapeseed', 'stone_wall', 'sandbar', 'volcano', 'worm_fence', 'French_loaf', 'theater_curtain', 'bannister', 'freight_car', 'dam', 'worm_fence', 'trailer_truck', 'lakeside', 'park_bench', 'canoe', 'gondola', 'worm_fence', 'killer_whale', 'ear', 'tripod', 'solar_dish', 'bannister', 'radio_telescope', 'flagpole', 'velvet', 'cloak', 'car_mirror', 'solar_dish', 'maypole', 'doormat', 'laptop', 'rule', 'analog_clock', 'screw', 'school_bus', 'freight_car', 'beacon', 'flagpole', 'rapeseed', 'hay', 'dam', 'canoe', 'maze', 'Dutch_oven', 'binder', 'envelope', 'wallet', 'letter_opener', 'handkerchief', 'dam', 'go-kart', 'limousine', 'bow', 'bobsled', 'streetcar', 'suspension_bridge', 'bullet_train', 'passenger_car', 'freight_car', 'steel_arch_bridge', 'viaduct', 'pier', 'dam', 'racer', 'trailer_truck', 'volcano', 'racer', 'seashore', 'worm_fence', 'pole', 'worm_fence', 'flagpole', 'Great_Pyrenees', 'pier', 'street_sign', 'trailer_truck', 'amphibian', 'racer', 'stone_wall', 'hook', 'whistle', 'sidewinder', 'nematode', 'combination_lock', 'flagpole', 'spotlight', 'worm_fence', 'fire_screen', 'pirate', 'velvet', 'nematode', 'binder', 'broom', 'wallet', 'car_mirror', 'velvet', 'cloak', 'grey_whale', 'grille', 'freight_car', 'passenger_car', 'electric_locomotive', 'dam', 'pier', 'pier', 'viaduct', 'dam', 'suspension_bridge', 'breakwater', 'trailer_truck', 'volcano', 'alp', 'unicycle', 'promontory', 'geyser', 'volcano', 'alp', 'mountain_tent', 'freight_car', 'fountain', 'geyser', 'umbrella', 'seashore', 'lakeside', 'trailer_truck', 'rapeseed', 'racer', 'go-kart', 'suspension_bridge', 'dam', 'steel_arch_bridge', 'viaduct', 'stretcher', 'aircraft_carrier', 'seashore', 'racer', 'sandbar', 'trailer_truck', 'lakeside', 'passenger_car', 'freight_car', 'dam', 'worm_fence', 'pier', 'worm_fence', 'theater_curtain', 'suspension_bridge', 'mountain_tent', 'fountain', 'theater_curtain', 'pier', 'suspension_bridge', 'passenger_car', 'fountain', 'school_bus', 'freight_car', 'passenger_car', 'pier', 'bobsled', 'bannister', 'tripod', 'radio_telescope', 'flagpole', 'crane', 'coil', 'running_shoe', 'French_horn', 'sundial', 'knot', 'fountain', 'lakeside', 'spotlight', 'obelisk', 'seashore', 'trailer_truck', 'alp', 'worm_fence', 'racer', 'bison', 'breakwater', 'dam', 'chainlink_fence', 'street_sign', 'lakeside', 'alp', 'valley', 'lakeside', 'dam', 'volcano', 'valley', 'alp', 'viaduct', 'mountain_tent', 'canoe', 'worm_fence', 'steel_arch_bridge', 'pole', 'street_sign', 'passenger_car', 'trailer_truck', 'garbage_truck', 'snowplow', 'minibus', 'tow_truck', 'cock', 'limpkin', 'ear', 'volcano', 'gown', 'street_sign', 'flagpole', 'picket_fence', 'worm_fence', 'viaduct', 'seashore', 'suspension_bridge', 'worm_fence', 'barrow', 'ear', 'street_sign', 'breakwater', 'brass', 'obelisk', 'promontory', 'trailer_truck', 'mountain_tent', 'volcano', 'passenger_car', 'solar_dish', 'wardrobe', 'upright', 'refrigerator', 'binder', 'chime', 'seashore', 'theater_curtain', 'hourglass', 'sarong', 'umbrella', 'coil', 'French_horn', 'nematode', 'bolo_tie', 'vine_snake', 'coil', 'theater_curtain', 'stage', 'paddlewheel', 'car_wheel', 'dam', 'handkerchief', 'crutch', 'canoe', 'worm_fence', 'obelisk', 'suspension_bridge', 'fountain', 'church', 'viaduct', 'church', 'rapeseed', 'cloak', 'mountain_tent', 'canoe', 'hatchet', 'letter_opener', 'cleaver', 'safety_pin', 'binder', 'maypole', 'trailer_truck', 'radio_telescope', 'pole', 'alp', 'valley', 'projectile', 'steel_arch_bridge', 'Japanese_spaniel', 'geyser', 'prayer_rug', 'megalith', 'worm_fence', 'stone_wall', 'Sussex_spaniel', 'umbrella', 'hay', 'rapeseed', 'pole', 'geyser', 'drilling_platform', 'streetcar', 'mobile_home', 'palace', 'liner', 'valley', 'alp', 'viaduct', 'stone_wall', 'lakeside', 'dock', 'container_ship', 'liner', 'streetcar', 'carousel', 'acoustic_guitar', 'electric_guitar', 'nematode', 'corkscrew', 'binder', 'lakeside', 'seashore', 'valley', 'alp', 'cliff', 'trailer_truck', 'alp', 'racer', 'hay', 'traffic_light', 'cliff', 'promontory', 'volcano', 'worm_fence', 'valley']
    
    orcount=0
    ofrcount=0
    for i in range(len(keywords[0])):
        if keywords[0][i][1] in key1:
            ofrcount+=1

        if keywords[0][i][1] in key2:
            orcount+=1

    if(ofrcount>=orcount):
        return 'OFFROAD'
    else:
        return 'ONROAD'


def detect(fname):
    #filename= '.\\uploads\\'+fname 
    filename= './uploads/'+fname #for mac 
    
    result = []
    try:
        img=image.load_img(filename,target_size=(224,224))
        mobile =tf.keras.applications.mobilenet.MobileNet()
        resized_img=image.img_to_array(img)
        final_image=np.expand_dims(resized_img,axis=0)
        final_image=tf.keras.applications.mobilenet.preprocess_input(final_image)
        pred=mobile.predict(final_image)
        result=imagenet_utils.decode_predictions(pred)
        print(result)
        res = mode(result)
        print(res)
        return res
    except:
        print('Error1')
        return -1


    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def uploadimg():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect('/')
        
        file1 = request.files['image']
        path = os.path.join(app.config['IMAGE_UPLOADS'], file1.filename)
        try:
            file1.save(path)
            out = []
            
            out = detect(file1.filename)

            if out!=-1:
                return render_template('result.html', results=out)
            else:
                return redirect('/')
        except:
            print('Error2')
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)