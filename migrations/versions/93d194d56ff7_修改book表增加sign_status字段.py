"""修改book表增加sign_status字段

Revision ID: 93d194d56ff7
Revises: 3bf7b43bf56f
Create Date: 2025-06-19 21:44:26.187483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d194d56ff7'
down_revision = '3bf7b43bf56f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sign_status', sa.String(length=16), nullable=False, comment='签约状态 未签约/已签约'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('sign_status')

    # ### end Alembic commands ###
