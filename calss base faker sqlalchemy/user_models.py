from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class UsrUserMerchant(Base):
    __tablename__ = 'usr_user_merchants'
    __table_args__ = (
        UniqueConstraint('user_id', 'merchant_id'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_user_merchants_id_seq'::regclass)"))
    user_id = Column(ForeignKey('usr_user.id'), nullable=False)
    merchant_id = Column(ForeignKey('usr_merchant.id'), nullable=False)

    merchant = relationship('UsrMerchant')
    user = relationship('UsrUser')

class UsrUserGroups(Base):
    __tablename__ = 'usr_user_groups'
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_user_groups_id_seq'::regclass)"))
    user_id = Column(ForeignKey('usr_user.id'), nullable=False)
    group_id = Column(ForeignKey('usr_group.id'), nullable=False)

    group = relationship('UsrGroup')
    user = relationship('UsrUser')

class UsrUser(Base):
    __tablename__ = 'usr_user'
    __table_args__ = (
        CheckConstraint('NOT ((mobile IS NULL) AND (username IS NULL))'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_user_id_seq'::regclass)"))
    kyc_id = Column(ForeignKey('usr_kyc.id'))
    merchant_id = Column(Integer)
    email = Column(String)
    mobile = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_pass = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    gender = Column(String)
    national_code = Column(String, unique=True)
    birth_date = Column(Date)
    profile_image = Column(String)
    last_login = Column(DateTime)
    identifier = Column(String, index=True)
    is_disabled = Column(Boolean)
    verified = Column(Boolean)
    verified_by = Column(String)
    verified_at = Column(DateTime)

    kyc = relationship('UsrKyc')


class UsrGroupScope(Base):
    __tablename__ = 'usr_group_scopes'
    __table_args__ = (
        UniqueConstraint('group_id', 'scope_id'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_group_scopes_id_seq'::regclass)"))
    group_id = Column(ForeignKey('usr_group.id'), nullable=False)
    scope_id = Column(ForeignKey('usr_scope.id'), nullable=False)

    group = relationship('UsrGroup')
    scope = relationship('UsrScope')


class UsrScope(Base):
    __tablename__ = 'usr_scope'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_scope_id_seq'::regclass)"))
    name = Column(String, unique=True)
    fa_name = Column(String)
    description = Column(String)
    module = Column(String)
    interface = Column(String)
    endpoint = Column(String)
    action = Column(String)



class UsrKyc(Base):
    __tablename__ = 'usr_kyc'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_kyc_id_seq'::regclass)"))
    sabte_ahval_inquired_at = Column(DateTime)
    sabte_ahval_track_no = Column(String)
    sabte_ahval_verified = Column(Boolean)
    shahkar_inquired_at = Column(DateTime)
    shahkar_verified = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)


class UsrMerchant(Base):
    __tablename__ = 'usr_merchant'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_merchant_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    name_fa = Column(String, nullable=False, unique=True)
    url = Column(String(1024))
    logo_address = Column(String(1024))
    logo_background_color = Column(String(128))


class UsrGroup(Base):
    __tablename__ = 'usr_group'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_group_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    fa_name = Column(String)
    description = Column(String)

class UsrSession(Base):
    __tablename__ = 'usr_session'
    __table_args__ = (
        UniqueConstraint('token', 'user_id'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_session_id_seq'::regclass)"))
    token = Column(String, index=True)

    user_id = Column(ForeignKey('usr_user.id'))
    expire_at = Column(DateTime)
    os = Column(String)
    os_version = Column(String)
    browser = Column(String)
    browser_version = Column(String)
    ip = Column(String)
    token_first_used_at = Column(DateTime)
    token_last_used_at = Column(DateTime)
    is_valid = Column(Boolean)



class UsrOtpSent(Base):
    __tablename__ = 'usr_otp_sent'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, server_default=text("nextval('usr_otp_sent_id_seq'::regclass)"))
    mobile = Column(String, nullable=False, index=True)
    otp = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime)
