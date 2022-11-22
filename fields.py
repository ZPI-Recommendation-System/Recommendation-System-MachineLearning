NUMBER = {
    "ModelEntity": 
        ["ramAmount", "driveStorage", "weight", "ramNumberOfFreeSlots", "ramMaxAmount", "hddSpeed"], 
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