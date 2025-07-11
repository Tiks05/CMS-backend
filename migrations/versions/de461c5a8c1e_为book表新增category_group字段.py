"""为book表新增category_group字段

Revision ID: de461c5a8c1e
Revises: 3f270a9fc891
Create Date: 2025-06-14 19:20:11.376896

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de461c5a8c1e'
down_revision = '3f270a9fc891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_group', sa.String(length=16), nullable=True, comment='分类所属组：主题 / 角色 / 情节'))
        batch_op.alter_column('category_type',
               existing_type=mysql.VARCHAR(length=32),
               comment='分类主题',
               existing_comment='分类主题 主题/角色/情节',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('category_type',
               existing_type=mysql.VARCHAR(length=32),
               comment='分类主题 主题/角色/情节',
               existing_comment='分类主题',
               existing_nullable=True)
        batch_op.drop_column('category_group')

    # ### end Alembic commands ###
