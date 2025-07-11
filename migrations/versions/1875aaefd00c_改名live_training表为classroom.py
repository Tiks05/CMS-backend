"""改名live_training表为classroom

Revision ID: 1875aaefd00c
Revises: 0b6ad7bded3d
Create Date: 2025-06-16 16:02:05.842047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1875aaefd00c'
down_revision = '0b6ad7bded3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False, comment='主标题'),
    sa.Column('category_type', sa.String(length=50), nullable=True, comment='分类标签'),
    sa.Column('cover_url', sa.String(length=255), nullable=True, comment='封面图路径'),
    sa.Column('intro', sa.String(length=255), nullable=True, comment='简介/摘要'),
    sa.Column('is_include_video', sa.Boolean(), nullable=False, comment='是否展示视频按钮'),
    sa.Column('content', sa.Text(), nullable=True, comment='HTML内容，含视频或正文'),
    sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classroom')
    # ### end Alembic commands ###
