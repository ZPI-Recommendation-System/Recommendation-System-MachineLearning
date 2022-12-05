NUMBER = {
    "ModelEntity": 
        ["ramAmount", "driveStorage", 
        "weight", 
        # "ramNumberOfFreeSlots", "ramMaxAmount", 
        "hddSpeed"], 
    "ScreenEntity": ["refreshRate", "diagonalScreenInches"],
    "ProcessorEntity": ["cores", "frequency"],
    ("ProcessorEntity", "benchmark_entity"): ["benchmark"],
    ("GraphicsEntity", "benchmark_entity"): ["benchmark"],
    "GraphicsEntity": ["graphicsCardVRam"],
}
CATEGORICAL = {
    "ModelEntity": ["ramType", "driveType"],
    "ScreenEntity": ["screenFinish"], 
    # touch screen is False for all laptops for some reason
    # "ScreenEntity": ["touchScreen"],
}
CATEGORICAL_MULTI = {
    # "ModelEntity": {
    #     "connections":[
    #         # fields that are just different variants (e.g. USB),
    #         # don't map directly into price (e.g. inne) 
    #         # or have small counts were removed
    #         "RJ-45",
    #         "Thunderbolt",
    #         "D-Sub (VGA)",
    #         "mini DisplayPort",
    #         "złącze dokowania",
    #         "DisplayPort",
    #         "slot na kartę SIM",
    #     ], 
    #     "communications":[
    #         # same as above 
    #         "LAN 10/100/1000 Mbps",
    #         "LAN 10/100 Mbps",
    #         "modem 4G (LTE)",
    #         "Intel Wireless Display (WiDi)",
    #         "NFC (Near Field Communication)",
    #     ], 
    #     # these aren't really meaningful 
    #     #"controls":True, 
    #     #"multimedia":True, 
    #     #"drives":True
    # },
}