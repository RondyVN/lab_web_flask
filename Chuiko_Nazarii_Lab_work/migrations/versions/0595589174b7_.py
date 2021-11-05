"""empty message

Revision ID: 0595589174b7
Revises: 1092797bcf79
Create Date: 2021-11-05 11:07:25.632618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0595589174b7'
down_revision = '1092797bcf79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user', type_='unique')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(length=20), nullable=True))
        batch_op.create_unique_constraint('user', ['first_name'])

    # ### end Alembic commands ###
