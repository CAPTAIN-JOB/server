""" created a create_app

Revision ID: 046a99bbceb8
Revises: 
Create Date: 2024-11-11 23:09:25.534714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '046a99bbceb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
