"""Add notes and date fields to Workout

Revision ID: 5d86520dbac0
Revises: 9ae64b47f284
Create Date: 2025-03-20 20:34:07.370938

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5d86520dbac0'
down_revision = '9ae64b47f284'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('workout', sa.Column('date', sa.Date(), nullable=False, server_default=sa.func.current_date()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'date')
    op.drop_column('workout', 'notes')
    # ### end Alembic commands ###
