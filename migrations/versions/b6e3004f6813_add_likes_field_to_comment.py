"""add likes field to comment

Revision ID: b6e3004f6813
Revises: a82cc6ce0926
Create Date: 2025-06-20 14:02:01.206516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6e3004f6813'
down_revision = 'a82cc6ce0926'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=True, comment='点赞数'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('likes')

    # ### end Alembic commands ###
