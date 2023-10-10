"""empty message

Revision ID: 5acac2f7a296
Revises: 
Create Date: 2023-10-05 20:22:24.836796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5acac2f7a296'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Patient',
    sa.Column('pat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pat_firstname', sa.String(length=50), nullable=False),
    sa.Column('pat_lastname', sa.String(length=45), nullable=False),
    sa.Column('pat_password', sa.String(length=200), nullable=False),
    sa.Column('pat_email', sa.String(length=45), nullable=False),
    sa.Column('pat_phn', sa.String(length=45), nullable=False),
    sa.Column('pat_dob', sa.Date(), nullable=False),
    sa.Column('pat_gender', sa.String(length=45), nullable=False),
    sa.Column('pat_mStatus', sa.String(length=45), nullable=False),
    sa.Column('insurance_number', sa.Integer(), nullable=False),
    sa.Column('profile_picture', sa.String(length=100), nullable=True),
    sa.Column('pat_address', sa.String(length=70), nullable=False),
    sa.Column('datereg', sa.DateTime(), nullable=True),
    sa.Column('pat_restricted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('pat_id'),
    sa.UniqueConstraint('pat_email')
    )
    op.create_table('Specialization',
    sa.Column('spec_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spec_name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('spec_id')
    )
    op.create_table('Subscription',
    sa.Column('subs_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sub_email', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('subs_id')
    )
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_firstname', sa.String(length=50), nullable=False),
    sa.Column('admin_lastname', sa.String(length=45), nullable=False),
    sa.Column('admin_password', sa.String(length=200), nullable=False),
    sa.Column('admin_email', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('state',
    sa.Column('state_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('state_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('state_id')
    )
    op.create_table('Personnel',
    sa.Column('per_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('per_firstname', sa.String(length=50), nullable=False),
    sa.Column('per_lastname', sa.String(length=45), nullable=False),
    sa.Column('per_password', sa.String(length=200), nullable=False),
    sa.Column('per_email', sa.String(length=45), nullable=False),
    sa.Column('per_phn', sa.String(length=45), nullable=False),
    sa.Column('per_dob', sa.Date(), nullable=False),
    sa.Column('liscence_number', sa.Integer(), nullable=False),
    sa.Column('acc_num', sa.Integer(), nullable=False),
    sa.Column('per_address', sa.String(length=70), nullable=False),
    sa.Column('per_gender', sa.String(length=70), nullable=False),
    sa.Column('per_mStatus', sa.String(length=45), nullable=False),
    sa.Column('per_lga', sa.String(length=45), nullable=False),
    sa.Column('per_status', sa.Enum('1', '0'), server_default='0', nullable=False),
    sa.Column('per_profile_picture', sa.String(length=100), nullable=False),
    sa.Column('datereg', sa.DateTime(), nullable=True),
    sa.Column('per_restricted', sa.Boolean(), nullable=True),
    sa.Column('per_spec_id', sa.Integer(), nullable=False),
    sa.Column('per_state_id', sa.Integer(), nullable=False),
    sa.Column('per_bank_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['per_bank_id'], ['banks.id'], ),
    sa.ForeignKeyConstraint(['per_spec_id'], ['Specialization.spec_id'], ),
    sa.ForeignKeyConstraint(['per_state_id'], ['state.state_id'], ),
    sa.PrimaryKeyConstraint('per_id'),
    sa.UniqueConstraint('per_email')
    )
    op.create_table('lga',
    sa.Column('lga_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lga_name', sa.String(length=20), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.state_id'], ),
    sa.PrimaryKeyConstraint('lga_id')
    )
    op.create_table('Appointment',
    sa.Column('app_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('app_status', sa.Enum('pending', 'approved', 'declined'), server_default='pending', nullable=False),
    sa.Column('app_date', sa.Date(), nullable=True),
    sa.Column('app_time', sa.Time(), nullable=True),
    sa.Column('app_pat_id', sa.Integer(), nullable=False),
    sa.Column('app_per_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['app_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['app_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('app_id')
    )
    op.create_table('Financial',
    sa.Column('fin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fin_status', sa.Enum('pending', 'approved', 'declined'), server_default='pending', nullable=False),
    sa.Column('app_date_time', sa.DateTime(), nullable=True),
    sa.Column('fin_amount', sa.Integer(), nullable=False),
    sa.Column('payment_invoice', sa.String(length=250), nullable=False),
    sa.Column('paygate_response', sa.Text(), nullable=True),
    sa.Column('fin_fullname', sa.String(length=100), nullable=True),
    sa.Column('fin_email', sa.String(length=100), nullable=True),
    sa.Column('fin_pat_id', sa.Integer(), nullable=False),
    sa.Column('fin_per_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fin_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['fin_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('fin_id')
    )
    op.create_table('Kyc',
    sa.Column('kyc_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kyc_pix', sa.String(length=200), nullable=False),
    sa.Column('kyc_per_id', sa.Integer(), nullable=False),
    sa.Column('kyc_reason', sa.Text(), nullable=True),
    sa.Column('kyc_date', sa.DateTime(), nullable=True),
    sa.Column('kyc_status', sa.Enum('pending', 'approved', 'declined'), server_default='pending', nullable=False),
    sa.ForeignKeyConstraint(['kyc_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('kyc_id')
    )
    op.create_table('Message',
    sa.Column('msg_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('msg_pat_id', sa.Integer(), nullable=False),
    sa.Column('msg_per_id', sa.Integer(), nullable=False),
    sa.Column('messages', sa.Text(), nullable=True),
    sa.Column('msg_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['msg_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['msg_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('msg_id')
    )
    op.create_table('Notification',
    sa.Column('not_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('not_messages', sa.Text(), nullable=True),
    sa.Column('not_pat_id', sa.Integer(), nullable=False),
    sa.Column('not_per_id', sa.Integer(), nullable=False),
    sa.Column('not_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['not_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['not_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('not_id')
    )
    op.create_table('Reviews',
    sa.Column('rev_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rev_pat_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('rev_per_id', sa.Integer(), nullable=False),
    sa.Column('rev_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['rev_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['rev_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('rev_id')
    )
    op.create_table('Feedback',
    sa.Column('feed_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('feed_pat_id', sa.Integer(), nullable=False),
    sa.Column('feed_per_id', sa.Integer(), nullable=False),
    sa.Column('feed_app_id', sa.Integer(), nullable=False),
    sa.Column('feed_message', sa.Text(), nullable=True),
    sa.Column('feed_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['feed_app_id'], ['Appointment.app_id'], ),
    sa.ForeignKeyConstraint(['feed_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['feed_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('feed_id')
    )
    op.create_table('Labtest',
    sa.Column('lab_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lab_result', sa.String(length=250), nullable=False),
    sa.Column('lab_test', sa.String(length=250), nullable=True),
    sa.Column('lab_order', sa.String(length=250), nullable=True),
    sa.Column('lab_date_time', sa.DateTime(), nullable=True),
    sa.Column('lab_app_id', sa.Integer(), nullable=True),
    sa.Column('lab_pat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lab_app_id'], ['Appointment.app_id'], ),
    sa.ForeignKeyConstraint(['lab_pat_id'], ['Patient.pat_id'], ),
    sa.PrimaryKeyConstraint('lab_id')
    )
    op.create_table('HealthRecords',
    sa.Column('health_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('medical_history', sa.Text(), nullable=True),
    sa.Column('allergies', sa.Text(), nullable=True),
    sa.Column('Medications', sa.Text(), nullable=True),
    sa.Column('health_date_time', sa.DateTime(), nullable=True),
    sa.Column('health_pat_id', sa.Integer(), nullable=False),
    sa.Column('health_lab_id', sa.Integer(), nullable=True),
    sa.Column('health_per_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['health_lab_id'], ['Labtest.lab_id'], ),
    sa.ForeignKeyConstraint(['health_pat_id'], ['Patient.pat_id'], ),
    sa.ForeignKeyConstraint(['health_per_id'], ['Personnel.per_id'], ),
    sa.PrimaryKeyConstraint('health_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('HealthRecords')
    op.drop_table('Labtest')
    op.drop_table('Feedback')
    op.drop_table('Reviews')
    op.drop_table('Notification')
    op.drop_table('Message')
    op.drop_table('Kyc')
    op.drop_table('Financial')
    op.drop_table('Appointment')
    op.drop_table('lga')
    op.drop_table('Personnel')
    op.drop_table('state')
    op.drop_table('admin')
    op.drop_table('Subscription')
    op.drop_table('Specialization')
    op.drop_table('Patient')
    # ### end Alembic commands ###