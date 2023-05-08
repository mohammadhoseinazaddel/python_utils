from datetime import datetime
from sqlalchemy import create_engine
from faker import Faker
from system.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import not_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from user_models import UsrUserMerchant, UsrUser, UsrMerchant, UsrUserGroups, UsrGroupScope, UsrScope, UsrKyc, UsrGroup, \
    UsrSession

fake = Faker()
engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
default_session = Session()
fake_fa = Faker('fa_IR')


# create an engine to connect to the database
class UserRelatedSeeder:
    def __init__(self, session: Session = default_session):
        self.session = session

    # generate fake data for the UsrUser model
    def create_fake_kyc(self, number):
        for _ in range(number):
            kyc = UsrKyc(
                created_at=fake.date_time_between(start_date='-30d', end_date='now'),
                updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
                deleted_at=None,
                sabte_ahval_inquired_at=fake.date_time_between(start_date='-30d', end_date='now'),
                sabte_ahval_track_no=fake.uuid4(),
                sabte_ahval_verified=fake.boolean(),
                shahkar_inquired_at=fake.date_time_between(start_date='-30d', end_date='now'),
                shahkar_verified=fake.boolean(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                father_name=fake.first_name(),
            )
            self.session.add(kyc)
        self.session.commit()

    def create_fake_user(self, number):
        for _ in range(number):
            kyc_ids = [kyc.id for kyc in self.session.query(UsrKyc.id)]
            usr_user = UsrUser(
                created_at=fake.date_time_between(start_date='-30d', end_date='now'),
                updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
                deleted_at=None,
                kyc_id=fake.random_element(elements=kyc_ids),
                merchant_id=None,
                email=fake.email(),
                mobile=fake.phone_number(),
                username=fake.user_name(),
                hashed_pass=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                father_name=fake.first_name(),
                gender=fake.random_element(elements=('male', 'female')),
                national_code=fake.unique.random_number(digits=10),
                birth_date=fake.date_of_birth(),
                profile_image=fake.image_url(),
                last_login=fake.date_time_between(start_date='-30d', end_date='now'),
                identifier=fake.uuid4(),
                is_disabled=fake.boolean(),
                verified=fake.boolean(),
                verified_by=fake.random_element(elements=('sabte_ahval', 'shahkar')),
                verified_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
            self.session.add(usr_user)
        self.session.commit()

    # generate fake data for the UsrMerchant model
    def create_user_merchant(self, number):
        for _ in range(number):
            name = fake.unique.company()
            name_fa = fake_fa.unique.company()
            url = fake.url()
            logo_address = fake.image_url()
            logo_background_color = fake.color()

            # check if the name already exists in the table
            try:
                existing_merchant = self.session.query(UsrMerchant).filter_by(name=name).one()
                # if the name exists, skip this record and move on to the next one
                continue
            except NoResultFound:
                # if the name does not exist, insert a new record
                usr_merchant = UsrMerchant(
                    created_at=fake.date_time_between(start_date='-30d', end_date='now'),
                    updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
                    deleted_at=None,
                    name=name,
                    name_fa=name_fa,
                    url=url,
                    logo_address=logo_address,
                    logo_background_color=logo_background_color
                )
                self.session.add(usr_merchant)
        self.session.commit()

    # generate fake data for the UsrUserMerchant model
    def create_user_user_merchant(self, number):
        for _ in range(number):
            user_id = self.session.query(UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(UsrMerchant.id).order_by(func.random()).first()[0]
            created_at = fake.date_time_between(start_date='-30d', end_date='now')
            updated_at = created_at
            deleted_at = None
            usr_user_merchant = UsrUserMerchant(
                created_at=created_at,
                updated_at=updated_at,
                deleted_at=deleted_at,
                user_id=user_id,
                merchant_id=merchant_id
            )
            self.session.add(usr_user_merchant)

            try:
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                if 'duplicate key value violates unique constraint "user_merchant_unique"' in str(e):
                    # if the error is due to a duplicate record, skip it and move on to the next one
                    continue
                else:
                    # if the error is due to some other reason, raise the error
                    raise e

        self.session.commit()

    # commit the session to the database
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         if 'duplicate key value violates unique constraint "user_merchant_unique"' in str(e):
    #             # if the error is due to a duplicate record, skip it and move on to the next one
    #             pass
    #         else:
    #             # if the error is due to some other reason, raise the error
    #             raise e

    # # generate fake data for the UsrGroup model
    # for _ in range(5):
    #     usr_group = UsrGroup(
    #         created_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         deleted_at=None,
    #         name=fake.unique.word(),
    #         fa_name=fake.unique.word(),
    #         description=fake.text()
    #     )
    #     session.add(usr_group)
    #
    # # generate fake data for the UsrUserGroups model
    # for _ in range(10):
    #     gp_id = [gp.id for gp in session.query(UsrGroup.id)]
    #     user = session.query(UsrUser.id).order_by(func.random()).first()
    #     group = session.query(UsrGroup).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_user_groups = UsrUserGroups(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         user_id=user.id,
    #         group_id=group.id
    #     )
    #     session.add(usr_user_groups)

    # generate fake data for the UsrScope model
    # for _ in range(5):
    #     usr_scope = UsrScope(
    #         created_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         deleted_at=None,
    #         name=fake.unique.word(),
    #         fa_name=fake.unique.word(),
    #         description=fake.text(),
    #         module='usr',
    #         interface=fake.unique.word(),
    #         endpoint=fake.unique.url(),
    #         action=fake.unique.word(),
    #     )
    #     session.add(usr_scope)

    # generate fake data for the UsrGroupScope model
    # for _ in range(10):
    #     group = session.query(UsrGroup).order_by(func.random()).first()
    #     scope = session.query(UsrScope).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_group_scope = UsrGroupScope(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         group_id=group.id,
    #         scope_id=scope.id
    #     )
    #     session.add(usr_group_scope)

    # generate fake data for the UsrSession model
    # for _ in range(10):
    #     user = session.query(UsrUser).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_session = UsrSession(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         token=fake.uuid4(),
    #         user_id=user.id,
    #         expire_at=fake.date_time_between(start_date='+30d', end_date='+60d'),
    #         os=fake.user_agent(),
    #         ip=fake.ipv4_public(),
    #         device_model=fake.user_agent(),
    #         device_token=fake.uuid4(),
    #         device_id=fake.uuid4(),
    #     )
    #     session.add(usr_session)



user_seeder = UserRelatedSeeder()
user_seeder.create_fake_kyc(11)
user_seeder.create_fake_user(10)
user_seeder.create_user_merchant(14)
user_seeder.create_user_user_merchant(4)
