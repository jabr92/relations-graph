from __future__ import annotations

from datetime import datetime
from typing import List

from graphviz import Digraph
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class EntityType(Base):
    __tablename__ = 'entity_type'
    __id_map = {}

    id = Column(String(2), primary_key=True)
    color_code = Column(String(6), nullable=False)
    name = Column(String(56), nullable=False)

    @property
    def hex_code(self):
        return '#' + self.color_code

    @classmethod
    def get_all(cls, session) -> List[EntityType]:
        return session.query(cls).all()

    @classmethod
    def id_from_name(cls, session, name: str) -> str:
        if name in cls.__id_map:
            return cls.__id_map[name]
        type_id = session.query(cls.id).filter(cls.name == name).one().id
        cls.__id_map[name] = type_id
        return type_id


class EntityRelation(Base):
    __tablename__ = 'entity_relation'

    source_entity_id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
    source_entity: Entity = relationship('Entity', foreign_keys=[source_entity_id], backref=backref('relations_from'))
    target_entity_id = Column(Integer, ForeignKey('entity.id'), primary_key=True)
    target_entity: Entity = relationship('Entity', foreign_keys=[target_entity_id], backref=backref('relations_to'))
    relation = Column(String(64), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def add_to_graph(self, graph: Digraph, target_color: bool = False):
        color_source = self.target_entity if target_color else self.source_entity
        color = color_source.entity_type.hex_code
        weight = 1
        if self.source_entity.entity_type.name == 'Player':
            weight += 2
        if self.target_entity.entity_type.name == 'Player':
            weight += 2
        graph.edge(self.source_entity.full_name, self.target_entity.full_name,
                   label=self.relation_type,
                   dir='both' if self.mutual else 'forward',
                   penwidth='4' if self.mutual else '2',
                   weight=str(weight),
                   color=color
                   )

    @classmethod
    def all_active(cls, session) -> List[EntityRelation]:
        return session.query(cls).filter_by(active=True).all()


class Entity(Base):
    __tablename__ = 'entity'

    id = Column(Integer, primary_key=True)
    entity_type_code = Column(String(2), ForeignKey('entity_type.id'), nullable=False)
    entity_type: EntityType = relationship(EntityType, backref=backref('entity', lazy=True))
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=True)
    title = Column(String(64), nullable=True)
    status = Column(String(64), nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    relations_source = relationship(EntityRelation,
                                    foreign_keys=[EntityRelation.source_entity_id],
                                    backref=backref('entity_source', lazy='joined')
                                    )
    relations_target = relationship(EntityRelation,
                                    foreign_keys=[EntityRelation.target_entity_id],
                                    backref=backref('entity_target', lazy='joined')
                                    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def display_name(self):
        title_display = f"\nthe {self.title}" if self.title else ''
        status_display = f"\n({self.status})" if self.status else ''
        last_display = f" {self.last_name}" if self.last_name else ''
        return f"{self.first_name}{last_display}{title_display}{status_display}"

    def add_to_graph(self, dot: Digraph):
        dot.node(name=self.full_name, label=self.display_name, color=self.entity_type.hex_code)

    @classmethod
    def all_active(cls, session) -> List[Entity]:
        return session.query(cls).filter_by(active=True).all()

