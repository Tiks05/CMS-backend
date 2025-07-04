"""为book表新增theme_type role_type, category_type改名为plot_type字段

Revision ID: 946751397a33
Revises: de461c5a8c1e
Create Date: 2025-06-14 19:40:17.261867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '946751397a33'
down_revision = 'de461c5a8c1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('theme_type', sa.String(length=64), nullable=True, comment='主题分类标签，如 青春甜宠、克苏鲁'))
        batch_op.add_column(sa.Column('role_type', sa.String(length=64), nullable=True, comment='角色分类标签，如 多女主、总裁'))
        batch_op.alter_column('plot_type',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=64),
               comment='情节分类标签，如 异世穿越、末日求生',
               existing_comment='分类主题',
               existing_nullable=True)
        batch_op.drop_column('category_group')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_group', mysql.VARCHAR(length=16), nullable=True, comment='分类所属组：主题 / 角色 / 情节'))
        batch_op.alter_column('plot_type',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=64),
               comment='分类主题',
               existing_comment='情节分类标签，如 异世穿越、末日求生',
               existing_nullable=True)
        batch_op.drop_column('role_type')
        batch_op.drop_column('theme_type')

    # ### end Alembic commands ###
