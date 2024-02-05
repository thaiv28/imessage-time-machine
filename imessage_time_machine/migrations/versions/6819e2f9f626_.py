"""empty message

Revision ID: 6819e2f9f626
Revises: 
Create Date: 2023-12-30 07:11:20.990232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6819e2f9f626'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('meta', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('reply', sa.String(length=5000), nullable=False))
        batch_op.add_column(sa.Column('text', sa.String(length=5000), nullable=False))
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('time', sa.Time(), nullable=False))
        batch_op.add_column(sa.Column('dt', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('reaction', sa.Boolean(), nullable=False))
        batch_op.create_index(batch_op.f('ix_message_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_dt'), ['dt'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_time'), ['time'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_time'))
        batch_op.drop_index(batch_op.f('ix_message_dt'))
        batch_op.drop_index(batch_op.f('ix_message_date'))
        batch_op.drop_column('reaction')
        batch_op.drop_column('name')
        batch_op.drop_column('dt')
        batch_op.drop_column('time')
        batch_op.drop_column('date')
        batch_op.drop_column('text')
        batch_op.drop_column('reply')
        batch_op.drop_column('meta')

    # ### end Alembic commands ###