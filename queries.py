from db.entities import *

def all_laptops(session):
    return (session.query(OfferEntity, ModelEntity, ProcessorEntity, GraphicsEntity, ScreenEntity)
                .filter(OfferEntity.modelId == ModelEntity.id)
                .filter(ModelEntity.processorId == ProcessorEntity.id)
                .filter(ModelEntity.graphicsId == GraphicsEntity.id)
                .filter(ModelEntity.screenId == ScreenEntity.id))