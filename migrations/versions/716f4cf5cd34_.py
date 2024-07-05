"""empty message

Revision ID: 716f4cf5cd34
Revises: d2a6d0705793
Create Date: 2024-07-05 21:45:04.839698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '716f4cf5cd34'
down_revision = 'd2a6d0705793'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###
