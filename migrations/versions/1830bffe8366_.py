"""empty message

Revision ID: 1830bffe8366
Revises: None
Create Date: 2017-05-26 18:58:23.939434

"""

# revision identifiers, used by Alembic.
revision = '1830bffe8366'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.Column('alarm_type', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.String(length=30), nullable=False),
    sa.Column('device_ip', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('device')
    ### end Alembic commands ###
