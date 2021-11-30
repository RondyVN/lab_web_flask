"""empty message

Revision ID: 0ac4ada854cf
Revises: 19d283cc166d
Create Date: 2021-11-30 12:23:16.721786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ac4ada854cf'
down_revision = '19d283cc166d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('post_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['post_id'], ['id'])

    # ### end Alembic commands ###
