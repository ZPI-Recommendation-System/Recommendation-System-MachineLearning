# coding: utf-8
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class BenchmarkEntity(Base):
    __tablename__ = 'benchmark_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('benchmark_entity_id_seq'::regclass)"))
    type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    benchmark = Column(Float(53), nullable=False)
    samples = Column(Integer, nullable=False)
    url = Column(String, nullable=False)


class CommunicationEntity(Base):
    __tablename__ = 'communication_entity'

    communicationName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_communications_communication_entity')


class ConnectionEntity(Base):
    __tablename__ = 'connection_entity'

    connectionName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_connections_connection_entity')


class ControlEntity(Base):
    __tablename__ = 'control_entity'

    controlName = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_controls_control_entity')


class DriveTypeEntity(Base):
    __tablename__ = 'drive_type_entity'

    driveType = Column(String, primary_key=True)

    model_entity = relationship('ModelEntity', secondary='model_entity_drives_drive_type_entity')


class GraphicsEntity(Base):
    __tablename__ = 'graphics_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('graphics_entity_id_seq'::regclass)"))
    graphicsCardModel = Column(String, nullable=False)
    graphicsCardType = Column(String)
    graphicsCardVRam = Column(String)
    benchmarkId = Column(ForeignKey('benchmark_entity.id'))

    benchmark_entity = relationship('BenchmarkEntity')


class ModelEntity(Base):
    __tablename__ = 'model_entity'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    type = Column(String)
    producentCode = Column(String)
    batterySizeWH = Column(Float(53))
    batterySizeMAH = Column(Float(53))
    batteryTime = Column(Float(53))
    color = Column(String)
    width = Column(Float(53))
    length = Column(Float(53))
    depth = Column(Float(53))
    weight = Column(Float(53))
    ramAmount = Column(Float(53), nullable=False)
    ramFrequency = Column(Integer)
    ramNumberOfSlots = Column(Integer)
    ramNumberOfFreeSlots = Column(Integer)
    ramType = Column(String)
    ramMaxAmount = Column(Integer)
    driveStorage = Column(Integer, nullable=False)
    driveType = Column(String)
    hddSpeed = Column(Integer)
    price = Column(Float(53), nullable=False)
    priceSource = Column(String, nullable=False, server_default=text("'unknown'::character varying"))
    processorId = Column(ForeignKey('processor_entity.id'))
    screenId = Column(ForeignKey('screen_entity.id'))
    graphicsId = Column(ForeignKey('graphics_entity.id'))

    graphics_entity = relationship('GraphicsEntity')
    processor_entity = relationship('ProcessorEntity')
    screen_entity = relationship('ScreenEntity')
    multimedia_entity = relationship('MultimediaEntity', secondary='model_entity_multimedia_multimedia_entity')
    model_img_entity = relationship('ModelImgEntity', secondary='model_entity_images_model_img_entity')


t_model_entity_communications_communication_entity = Table(
    'model_entity_communications_communication_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('communicationEntityCommunicationName', ForeignKey('communication_entity.communicationName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_connections_connection_entity = Table(
    'model_entity_connections_connection_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('connectionEntityConnectionName', ForeignKey('connection_entity.connectionName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_controls_control_entity = Table(
    'model_entity_controls_control_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('controlEntityControlName', ForeignKey('control_entity.controlName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_drives_drive_type_entity = Table(
    'model_entity_drives_drive_type_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('driveTypeEntityDriveType', ForeignKey('drive_type_entity.driveType', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_images_model_img_entity = Table(
    'model_entity_images_model_img_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('modelImgEntityId', ForeignKey('model_img_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_model_entity_multimedia_multimedia_entity = Table(
    'model_entity_multimedia_multimedia_entity', metadata,
    Column('modelEntityId', ForeignKey('model_entity.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('multimediaEntityMultimediaName', ForeignKey('multimedia_entity.multimediaName', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class ModelImgEntity(Base):
    __tablename__ = 'model_img_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('model_img_entity_id_seq'::regclass)"))
    url = Column(String, nullable=False)


class MultimediaEntity(Base):
    __tablename__ = 'multimedia_entity'

    multimediaName = Column(String, primary_key=True)


class ProcessorEntity(Base):
    __tablename__ = 'processor_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('processor_entity_id_seq'::regclass)"))
    model = Column(String, nullable=False)
    series = Column(String)
    cores = Column(Integer)
    frequency = Column(Float(53))
    benchmarkId = Column(ForeignKey('benchmark_entity.id'))

    benchmark_entity = relationship('BenchmarkEntity')


class ScreenEntity(Base):
    __tablename__ = 'screen_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('screen_entity_id_seq'::regclass)"))
    diagonalScreenInches = Column(Float(53), nullable=False)
    resolution = Column(String)
    screenFinish = Column(String)
    screenType = Column(String)
    refreshRate = Column(Integer)
    touchScreen = Column(Boolean)


class UserEntity(Base):
    __tablename__ = 'user_entity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_entity_id_seq'::regclass)"))
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
