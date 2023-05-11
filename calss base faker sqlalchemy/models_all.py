# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CrdUser(Base):
    __tablename__ = 'crd_user'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('crd_user_id_seq'::regclass)"))
    user_id = Column(Integer, nullable=False, unique=True)
    is_locked = Column(Boolean)


class ExtBotonConsumeError(Base):
    __tablename__ = 'ext_boton_consume_error'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ext_boton_consume_error_id_seq'::regclass)"))
    queue = Column(String, index=True)
    body = Column(String)
    error = Column(String)
    status = Column(String, index=True)


class ExtBotonDeposit(Base):
    __tablename__ = 'ext_boton_deposit'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, server_default=text("nextval('ext_boton_deposit_id_seq'::regclass)"))
    coin = Column(String)
    network = Column(String, nullable=False)
    amount = Column(String)
    decimals = Column(Integer)
    confirmation = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    tx_id = Column(String, nullable=False)
    memo = Column(String)
    wallet_address = Column(String)
    system_status = Column(String, nullable=False)


class FncBankPayment(Base):
    __tablename__ = 'fnc_bank_payment'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_bank_payment_id_seq'::regclass)"))
    bank_payment_id = Column(ForeignKey('fnc_bank_payment.id'))
    type = Column(String)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    wage = Column(Integer)
    description = Column(Text)
    expired_at = Column(DateTime)
    status = Column(String)
    success_pgw_id = Column(ForeignKey('fnc_payment_gateway.id'))

    bank_payment = relationship('FncBankPayment', remote_side=[id])
    success_pgw = relationship('FncPaymentGateway', primaryjoin='FncBankPayment.success_pgw_id == FncPaymentGateway.id')


class FncBankProfile(Base):
    __tablename__ = 'fnc_bank_profile'
    __table_args__ = (
        UniqueConstraint('merchant_id', 'is_default'),
        Index('merchant_default_account', 'merchant_id', 'is_default')
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_bank_profile_id_seq'::regclass)"))
    user_id = Column(Integer)
    merchant_id = Column(Integer)
    is_default = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    bank_name = Column(String)
    account_no = Column(String)
    iban = Column(String)
    card_no = Column(String)



class FncBankTransaction(Base):
    __tablename__ = 'fnc_bank_transactions'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_bank_transactions_id_seq'::regclass)"))


class FncDebtUser(Base):
    __tablename__ = 'fnc_debt_user'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_debt_user_id_seq'::regclass)"))
    user_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    due_date = Column(Date)
    input_type = Column(String)
    input_unique_id = Column(Integer)
    order_id = Column(Integer, nullable=False)


class FncPaymentGateway(Base):
    __tablename__ = 'fnc_payment_gateway'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_payment_gateway_id_seq'::regclass)"))
    type = Column(String, nullable=False)
    payment_gateway_id = Column(ForeignKey('fnc_payment_gateway.id'))
    bank_payment_id = Column(ForeignKey('fnc_bank_payment.id'))
    amount = Column(Integer, nullable=False)
    wage = Column(Integer)
    gateway_name = Column(String)
    description = Column(Text)
    status = Column(String)
    ref_num = Column(String, index=True)
    expired_at = Column(DateTime)
    psp_purchase_id = Column(String)
    psp_switching_url = Column(String(1024))
    callback_status = Column(String)
    psp_status = Column(String)
    psp_trace_no = Column(String)
    payer_ip = Column(String)
    psp_ref_num = Column(String)
    psp_rrn = Column(String)
    payer_masked_card_num = Column(String)
    psp_name = Column(String)
    reversed_at = Column(DateTime)
    reverse_status = Column(String)
    refund_batch_id = Column(String)
    refund_transfer_id = Column(String)

    bank_payment = relationship('FncBankPayment', primaryjoin='FncPaymentGateway.bank_payment_id == FncBankPayment.id')
    payment_gateway = relationship('FncPaymentGateway', remote_side=[id])


class FncRefund(Base):
    __tablename__ = 'fnc_refund'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_refund_id_seq'::regclass)"))
    uuid = Column(String, unique=True)
    order_id = Column(Integer, nullable=False, unique=True)
    order_uuid = Column(String, nullable=False, unique=True)
    order_user_id = Column(Integer, nullable=False)
    merchant_id = Column(Integer, nullable=False, index=True)
    merchant_user_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    refund_by_debt = Column(Integer)
    refund_by_rial = Column(Integer)


class NtfProvider(Base):
    __tablename__ = 'ntf_provider'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ntf_provider_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    line_number = Column(String, nullable=False)
    position_number = Column(Integer, nullable=False, unique=True)


class NtfTemplate(Base):
    __tablename__ = 'ntf_template'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ntf_template_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    text = Column(String, nullable=False)
    title = Column(String, nullable=False)


class OrdCommission(Base):
    __tablename__ = 'ord_commission'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ord_commission_id_seq'::regclass)"))
    merchant_id = Column(Integer, nullable=False)
    category = Column(String, nullable=False, index=True)
    pgw_commission_constant = Column(Integer, nullable=False)
    pgw_commission_rate = Column(Float(53), nullable=False)
    pgw_fee_constant = Column(Integer)
    pgw_fee_rate = Column(Float(53))
    credit_commission_constant = Column(Integer, nullable=False)
    credit_commission_rate = Column(Float(53), nullable=False)
    credit_limit = Column(Integer, nullable=False)
    decrease_fee_on_pay_gw_settle = Column(Boolean)
    decrease_commission_on_refund = Column(Boolean)


class OrdPay(Base):
    __tablename__ = 'ord_pay'
    __table_args__ = (
        UniqueConstraint('merchant_order_id', 'merchant_id'),
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    title = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ord_pay_id_seq'::regclass)"))
    identifier = Column(String, nullable=False)
    user_id = Column(Integer)
    type = Column(String, nullable=False)
    amount = Column(Float(53), nullable=False)
    status = Column(String)
    action = Column(String)
    paid_at = Column(DateTime)
    merchant_order_id = Column(String, nullable=False)
    merchant_id = Column(Integer, nullable=False)
    merchant_user_id = Column(String, nullable=False, index=True)
    merchant_redirect_url = Column(String, nullable=False)
    settle_id = Column(Integer)
    commission_id = Column(Integer, nullable=False)


class SoCoin(Base):
    __tablename__ = 'so_coin'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('so_coin_id_seq'::regclass)"))
    name = Column(String, unique=True)
    fa_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    wallex_symbol = Column(String)
    ltv = Column(Float(53))
    price_in_rial = Column(Float(53))
    price_in_usdt = Column(Float(53))
    logo_address = Column(String(1024))
    networks = Column(JSON)


class SoRule(Base):
    __tablename__ = 'so_rule'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('so_rule_id_seq'::regclass)"))
    version = Column(String, nullable=False)
    rules = Column(String(2048), nullable=False)


class UasCryptoTransaction(Base):
    __tablename__ = 'uas_crypto_transaction'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    type = Column(String, nullable=False)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    amount = Column(Float(53), nullable=False)
    user_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('uas_crypto_transaction_id_seq'::regclass)"))
    coin_name = Column(String, nullable=False)


class UasFiatTransaction(Base):
    __tablename__ = 'uas_fiat_transaction'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    type = Column(String, nullable=False)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    amount = Column(Float(53), nullable=False)
    user_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('uas_fiat_transaction_id_seq'::regclass)"))


class UasWalletAddres(Base):
    __tablename__ = 'uas_wallet_address'
    __table_args__ = (
        UniqueConstraint('national_code', 'coin_name', 'network_name', 'memo'),
        Index('uas_wallet_address_index', 'national_code', 'coin_name', 'network_name')
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('uas_wallet_address_id_seq'::regclass)"))
    user_id = Column(Integer)
    national_code = Column(String, nullable=False)
    coin_name = Column(String, nullable=False)
    network_name = Column(String, nullable=False)
    address = Column(String, nullable=False, unique=True)
    memo = Column(String)


class UasWallexTransaction(Base):
    __tablename__ = 'uas_wallex_transaction'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    type = Column(String, nullable=False)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    amount = Column(Float(53), nullable=False)
    user_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('uas_wallex_transaction_id_seq'::regclass)"))
    coin_name = Column(String, nullable=False)


class UsrGroup(Base):
    __tablename__ = 'usr_group'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('usr_group_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    fa_name = Column(String)
    description = Column(String)


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
    user_id = Column(Integer, index=True)
    expire_at = Column(DateTime)
    os = Column(String)
    os_version = Column(String)
    browser = Column(String)
    browser_version = Column(String)
    ip = Column(String)
    token_first_used_at = Column(DateTime)
    token_last_used_at = Column(DateTime)
    is_valid = Column(Boolean)


class WlxLogin(Base):
    __tablename__ = 'wlx_login'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, server_default=text("nextval('wlx_login_id_seq'::regclass)"))
    order_uuid = Column(String)
    state = Column(String, index=True)
    wallex_login_url = Column(String(1024))
    code = Column(String, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    expire_in = Column(String)
    wallex_user_id = Column(String)
    kyc_level = Column(Integer)
    user_id = Column(Integer)
    wallpay_error = Column(String)
    used_at = Column(DateTime)


class WlxPayIn(Base):
    __tablename__ = 'wlx_pay_in'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, server_default=text("nextval('wlx_pay_in_id_seq'::regclass)"))
    token = Column(String, index=True)
    status = Column(String, nullable=False)
    uuid = Column(String, index=True)
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    assets = Column(JSON, nullable=False)
    redirect_url = Column(String)
    callback_url = Column(String)
    wallex_user_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    state = Column(String)


class CrdCalculator(Base):
    __tablename__ = 'crd_calculator'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('crd_calculator_id_seq'::regclass)"))
    credit_id = Column(ForeignKey('crd_user.id'), nullable=False)
    input_type = Column(String)
    input_unique_id = Column(Integer)
    non_free_credit = Column(BigInteger, nullable=False)
    used_non_free_credit = Column(BigInteger, nullable=False)
    free_credit = Column(Integer, nullable=False)
    used_free_credit = Column(Integer, nullable=False)
    asset_json = Column(JSON)
    cs = Column(Float(53), nullable=False)

    credit = relationship('CrdUser')


class FncTransfer(Base):
    __tablename__ = 'fnc_transfer'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_transfer_id_seq'::regclass)"))
    bank_profile_id = Column(ForeignKey('fnc_bank_profile.id'), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String)
    batch_id = Column(String)
    transfer_id = Column(String, index=True)
    status = Column(String)
    ext_service_name = Column(String, nullable=False)
    input_type = Column(String)
    input_unique_id = Column(Integer)
    error_message = Column(String)
    merchant_id = Column(Integer, nullable=False, index=True)

    bank_profile = relationship('FncBankProfile')



class NtfNotificationCenter(Base):
    __tablename__ = 'ntf_notification_center'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ntf_notification_center_id_seq'::regclass)"))
    input_type = Column(String)
    input_unique_id = Column(Integer)
    with_push_notification = Column(Boolean)
    with_sms = Column(Boolean)
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'))
    title = Column(String)
    user_id = Column(Integer)
    seen_at = Column(DateTime)

    template = relationship('NtfTemplate')


class NtfPushNotification(Base):
    __tablename__ = 'ntf_push_notification'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ntf_push_notification_id_seq'::regclass)"))
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    retrying_count = Column(Integer, nullable=False)
    status = Column(String)
    user_id = Column(Integer)
    token = Column(String, nullable=False)
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'))
    exception = Column(String)
    provider_message_id = Column(String)

    template = relationship('NtfTemplate')


class NtfSm(Base):
    __tablename__ = 'ntf_sms'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ntf_sms_id_seq'::regclass)"))
    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer)
    retrying_count = Column(Integer, nullable=False)
    last_retried = Column(DateTime)
    status = Column(String)
    provider_id = Column(ForeignKey('ntf_provider.id'))
    user_id = Column(Integer)
    mobile_number = Column(String, nullable=False)
    text = Column(String, nullable=False)
    template_id = Column(ForeignKey('ntf_template.id'))
    provider_message_id = Column(String)

    provider = relationship('NtfProvider')
    template = relationship('NtfTemplate')


class OrdFund(Base):
    __tablename__ = 'ord_fund'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('ord_fund_id_seq'::regclass)"))
    order_id = Column(ForeignKey('ord_pay.id'), nullable=False, unique=True)
    order_amount = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    used_free_credit = Column(Integer, nullable=False)
    used_non_free_credit = Column(Integer, nullable=False)
    repaid_free_credit = Column(Integer)
    repaid_non_free_credit = Column(Integer)
    used_asset_json = Column(JSON)
    extra_money_to_pay = Column(Integer)
    need_collateral = Column(Boolean)
    collateral_confirmed = Column(Boolean)
    need_wallex_asset = Column(Boolean)
    wallex_block_request_id = Column(String)
    payment_amount = Column(Integer)
    payment_id = Column(Integer)
    paid_at = Column(DateTime)
    completely_repaid_at = Column(DateTime)
    fill_percentage = Column(Integer, nullable=False)

    order = relationship('OrdPay', uselist=False)


class UasCryptoWithdraw(Base):
    __tablename__ = 'uas_crypto_withdraw'

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('uas_crypto_withdraw_id_seq'::regclass)"))
    unique_id = Column(Integer)
    trace_id = Column(String, index=True)
    user_id = Column(Integer, nullable=False)
    wallet_address_id = Column(ForeignKey('uas_wallet_address.id'), nullable=False)
    from_address = Column(String)
    from_memo = Column(String)
    to_address = Column(String, nullable=False)
    to_memo = Column(String)
    amount = Column(Float(53), nullable=False)
    ack = Column(Integer)
    verify = Column(Integer)
    bundle_id = Column(Integer)
    is_identical = Column(Integer)
    fee = Column(Float(53))
    tx_id = Column(String)
    status = Column(String)

    wallet_address = relationship('UasWalletAddres')


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


class FncSettleCredit(Base):
    __tablename__ = 'fnc_settle_credit'
    __table_args__ = (
        UniqueConstraint('order_id', 'type'),
        Index('FncSettleCredit_fnc_order_id__type', 'order_id', 'type')
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_settle_credit_id_seq'::regclass)"))
    order_id = Column(Integer, index=True)
    order_uuid = Column(String, index=True)
    type = Column(String, nullable=False)
    merchant_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    transfer_id = Column(ForeignKey('fnc_transfer.id'))

    transfer = relationship('FncTransfer')


class FncSettlePgw(Base):
    __tablename__ = 'fnc_settle_pgw'
    __table_args__ = (
        UniqueConstraint('order_id', 'type'),
        Index('FncSettlePgw_fnc_order_id__type', 'order_id', 'type')
    )

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    id = Column(Integer, primary_key=True, index=True, server_default=text("nextval('fnc_settle_pgw_id_seq'::regclass)"))
    order_id = Column(Integer, index=True)
    order_uuid = Column(String, index=True)
    type = Column(String, nullable=False)
    merchant_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    transfer_id = Column(ForeignKey('fnc_transfer.id'))

    transfer = relationship('FncTransfer')


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
