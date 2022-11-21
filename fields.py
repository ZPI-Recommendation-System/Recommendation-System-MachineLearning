NUMBER = {
    "ModelEntity": 
        ["ramAmount", "driveStorage", "weight", "ramNumberOfFreeSlots", "ramMaxAmount", "hddSpeed"], 
    "ScreenEntity": ["refreshRate", "diagonalScreenInches"],
    "ProcessorEntity": ["cores", "frequency"],
    ("ProcessorEntity", "benchmark_entity"): ["benchmark"],
    ("GraphicsEntity", "benchmark_entity"): ["benchmark"],
}
CATEGORICAL = {
    "ModelEntity": ["color", "ramType", "driveType"],
    "GraphicsEntity": ["graphicsCardVRam"],
    "ScreenEntity": ["screenFinish"], 
    "ScreenEntity": ["touchScreen"],
}