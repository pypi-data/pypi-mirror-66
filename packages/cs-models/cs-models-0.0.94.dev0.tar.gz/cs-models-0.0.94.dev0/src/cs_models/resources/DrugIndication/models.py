from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
)

from datetime import datetime

from ...database import Base


class DrugIndicationModel(Base):
    __tablename__ = 'drug_indications'

    id = Column(Integer, primary_key=True)
    appl_no = Column(String(128), nullable=False)
    appl_type = Column(String(128), nullable=False)
    indication_text = Column(Text)
    indications = Column(Text)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint(
            'appl_no',
            'appl_type',
        ),
    )
