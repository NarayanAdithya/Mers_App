"""empty message

Revision ID: eb153141b922
Revises: e5a85ef38c67
Create Date: 2021-06-04 16:30:22.542226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb153141b922'
down_revision = 'e5a85ef38c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accepted_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('req_status', sa.String(length=10), nullable=True),
    sa.Column('preference', sa.String(length=15), nullable=True),
    sa.Column('exchange_with_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('denied_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('req_status', sa.String(length=10), nullable=True),
    sa.Column('preference', sa.String(length=15), nullable=True),
    sa.Column('exchange_with_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('denied_requests')
    op.drop_table('accepted_requests')
    # ### end Alembic commands ###
