"""create return date column

Revision ID: 33786e1755f0
Revises: 72bf2eefd9a8
Create Date: 2024-08-18 04:51:04.578773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33786e1755f0'
down_revision = '72bf2eefd9a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('issued_books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('return_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('issued_books', schema=None) as batch_op:
        batch_op.drop_column('return_date')

    # ### end Alembic commands ###
