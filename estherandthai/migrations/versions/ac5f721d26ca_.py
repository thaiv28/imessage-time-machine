"""empty message

Revision ID: ac5f721d26ca
Revises: c8a0c98918f4
Create Date: 2023-12-30 22:44:05.382667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac5f721d26ca'
down_revision = 'c8a0c98918f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meta', sa.String(length=100), nullable=False),
    sa.Column('reply', sa.String(length=5000), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('dt', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('reaction', sa.Boolean(), nullable=False),
    sa.Column('image', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_dt'), ['dt'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_time'), ['time'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_time'))
        batch_op.drop_index(batch_op.f('ix_message_dt'))
        batch_op.drop_index(batch_op.f('ix_message_date'))

    op.drop_table('message')
    # ### end Alembic commands ###