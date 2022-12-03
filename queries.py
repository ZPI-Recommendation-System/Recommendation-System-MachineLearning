from db.entities import *

def all_laptops(session):
    return (session.query(ModelEntity, ProcessorEntity, GraphicsEntity, ScreenEntity)
                .filter(ModelEntity.processorId == ProcessorEntity.id)
                .filter(ModelEntity.graphicsId == GraphicsEntity.id)
                .filter(ModelEntity.screenId == ScreenEntity.id))