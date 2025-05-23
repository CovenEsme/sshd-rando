import re

VALID_STAGE_PATCH_TYPES = (
    "layeroverride",
    "objadd",
    "objdelete",
    "objpatch",
    "objmove",
    "arcnadd",
    "pathadd",
)

STAGE_OBJECT_NAMES = [
    "OBJS",
    "OBJ ",
    "SOBS",
    "SOBJ",
    "STAS",
    "STAG",
    "SNDT",
    "DOOR",
]

DEFAULT_SOBJ = {
    "params1": 0,
    "params2": 0,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "sizex": 0,
    "sizey": 0,
    "sizez": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "id": 0,
    "name": "",
}

DEFAULT_OBJ = {
    "params1": 0,
    "params2": 0,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "id": 0,
    "name": "",
}

DEFAULT_SCEN = {
    "name": "",
    "room": 0,
    "layer": 0,
    "entrance": 0,
    "night": 0,
    "byte5": 0,
    "flag6": 0,
    "zero": 0,
    "saveprompt": 0,
}

DEFAULT_PLY = {
    "storyflag": 0,
    "play_cutscene": -1,
    "byte4": -1,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "entrance_id": 6,
}

DEFAULT_AREA = {
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "sizex": 0,
    "sizey": 0,
    "sizez": 0,
    "angle": 0,
    "area_link": -1,
    "unk3": 0,
    "dummy": b"\xff\xff\xff",
}

DEFAULT_PATH = {
    "unk1": -1,
    "unk2": -1,
    "pnt_start_idx": 0,
    "pnt_total_count": 0,
    "unk3": b"\xff\xff\xff\xff\x00\xff",
}

DEFAULT_PNT = {
    "posx": 0.0,
    "posy": 0.0,
    "posz": 0.0,
    "unk": b"\xff\xff\xff\xff",
}

DEFAULT_FLOW = {
    "type": "type1",
    "subType": -1,
    "param1": 0,
    "param2": 0,
    "param3": 0,
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_GIVE_ITEM_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # item id
    "param3": 9,  # give item command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_ITEM_FLAG_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # item id
    "param3": 53,  # set item flag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_STORYFLAG_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # storyflag id
    "param3": 0,
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_SCENEFLAG_FLOW = {
    "type": "type3",
    "subType": 1,
    "param1": -1,  # sceneflag id
    "param2": -1,  # scene index
    "param3": 2,  # give sceneflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_TEMPFLAG_FLOW = {
    "type": "type3",
    "subType": 1,
    "param1": -1,  # tempflag id
    "param2": -1,  # scene index
    "param3": 28,  # give tempflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_ZONEFLAG_FLOW = {
    "type": "type3",
    "subType": 1,
    "param1": -1,  # zoneflag id
    "param2": -1,  # scene index
    "param3": 4,  # give zoneflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_UNSET_ZONEFLAG_FLOW = {
    "type": "type3",
    "subType": 1,
    "param1": -1,  # zoneflag id
    "param2": -1,  # scene index
    "param3": 5,  # remove zoneflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_ATTENTION_MARK_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": 1,
    "param3": 31,
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_CHECK_STORYFLAG_FLOW = {
    "type": "switch",
    "subType": 6,
    "param1": 0,
    "param2": -1,  # storyflag
    "param3": 3,  # check storyflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_CHECK_SCENEFLAG_FLOW = {
    "type": "switch",
    "subType": 6,
    "param1": 0,
    "param2": -1,  # sceneflag
    "param3": 6,  # check sceneflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

FLOW_ADD_VARIATIONS = (
    "flowadd",
    "giveitem",
    "setitemflag",
    "setstoryflag",
    "setsceneflag",
    "settempflag",
    "setzoneflag",
    "unsetzoneflag",
    "attentionmark",
)
SWITCH_ADD_VARIATIONS = ("switchadd", "checkstoryflag", "checksceneflag")

PARAM1_ALIASES = (
    "setsceneflag",
    "settempflag",
    "setzoneflag",
    "unsetzoneflag",
)
PARAM2_ALIASES = (
    "itemid",
    "setstoryflag",
    "sceneindex",
    "checkstoryflag",
    "checksceneflag",
)

DEFAULT_FLOW_TYPE_LOOKUP = {
    "flowadd": DEFAULT_FLOW,
    "giveitem": DEFAULT_GIVE_ITEM_FLOW,
    "setitemflag": DEFAULT_SET_ITEM_FLAG_FLOW,
    "setstoryflag": DEFAULT_SET_STORYFLAG_FLOW,
    "setsceneflag": DEFAULT_SET_SCENEFLAG_FLOW,
    "settempflag": DEFAULT_SET_TEMPFLAG_FLOW,
    "setzoneflag": DEFAULT_SET_ZONEFLAG_FLOW,
    "unsetzoneflag": DEFAULT_UNSET_ZONEFLAG_FLOW,
    "attentionmark": DEFAULT_ATTENTION_MARK_FLOW,
    "switchadd": DEFAULT_FLOW,
    "checkstoryflag": DEFAULT_CHECK_STORYFLAG_FLOW,
    "checksceneflag": DEFAULT_CHECK_SCENEFLAG_FLOW,
}

STAGE_FILE_REGEX = re.compile("(.+)_stg_l([0-9]+).arc.LZ")
EVENT_FILE_REGEX = re.compile("([0-9])-[A-Za-z]+.arc")
ROOM_ARC_REGEX = re.compile(r"/rarc/(?P<stage>.+)_r(?P<roomID>[0-9]+).arc")
OARC_ARC_REGEX = re.compile(r"/oarc/(?P<name>.+\.arc)")
TEXT_ARC_REGEX = re.compile(
    r"(.+(/|\\))*(?P<lang>(en|es|fr))_US(/|\\)(?P<name>.+\.arc)"
)

STAGE_PATCH_PATH_REGEX = re.compile(
    r"stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objectName>[a-zA-Z]+)(/(?P<objectID>[^/]+))?"
)
EVENT_PATCH_PATH_REGEX = re.compile(r"event/(?P<eventFile>[^/]+)/(?P<eventID>[^/]+)")
OARC_ADD_PATH_REGEX = re.compile(
    r"oarc/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[^/]+)"
)
SHOP_PATCH_PATH_REGEX = re.compile(r"ShpSmpl/(?P<index>[0-9]+)")

LANGUAGE_NAME_TO_FILE_ID = {
    "chinese": "zh_CN",
    "dutch": "nl_NL",
    "english_gb": "en_GB",
    "english_us": "en_US",
    "french_fr": "fr_FR",
    "french_us": "fr_US",
    "german": "de_DE",
    "italian": "it_IT",
    "japanese": "ja_JP",
    "korean": "ko_KR",
    "russian": "ru_RU",
    "spanish_es": "es_ES",
    "spanish_us": "es_US",
    "taiwanese": "zh_TW",
}

# Non-layer 0 stages that appear in entrance_shuffle_data.yaml
STAGE_FILES_TO_ALWAYS_PATCH = {
    "F001r": (3,),
    "F300_4": (2,),
    "D301": (1,),
    "S000": (2,),
    "S100": (2,),
    "S200": (2,),
    "S300": (2,),
    "F211": (1,),
    "F302": (2,),
}
