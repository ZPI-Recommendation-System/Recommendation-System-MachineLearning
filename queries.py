from db.entities import *
import sqlalchemy

def all_laptops(session):
    return (session.query(ModelEntity, ProcessorEntity, GraphicsEntity, ScreenEntity)
                .filter(ModelEntity.processorId == ProcessorEntity.id)
                .filter(ModelEntity.graphicsId == GraphicsEntity.id)
                .filter(ModelEntity.screenId == ScreenEntity.id))


def counts_connections(session):
    return (session.query(
        sqlalchemy.func.count(ModelEntity.id),
        ConnectionEntity.connectionName
    ).join(ConnectionEntity, ModelEntity.connections)
    .group_by(
        ConnectionEntity.connectionName
    ))


def counts_communications(session):
    return (session.query(
        sqlalchemy.func.count(ModelEntity.id),
        CommunicationEntity.communicationName
    ).join(CommunicationEntity, ModelEntity.communications)
    .group_by(
        CommunicationEntity.communicationName
    ))

def counts_controls(session):
    return (session.query(
        sqlalchemy.func.count(ModelEntity.id),
        ControlEntity.controlName
    ).join(ControlEntity, ModelEntity.controls)
    .group_by(
        ControlEntity.controlName
    ))

def counts_multimedia(session):
    return (session.query(
        sqlalchemy.func.count(ModelEntity.id),
        MultimediaEntity.multimediaName
    ).join(MultimediaEntity, ModelEntity.multimedia)
    .group_by(
        MultimediaEntity.multimediaName
    ))

def counts_drives(session):
    return (session.query(
        sqlalchemy.func.count(ModelEntity.id),
        DriveTypeEntity.driveType
    ).join(DriveTypeEntity, ModelEntity.drives)
    .group_by(
        DriveTypeEntity.driveType
    ))