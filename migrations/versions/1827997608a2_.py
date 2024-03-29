"""empty message

Revision ID: 1827997608a2
Revises: 350397eae653
Create Date: 2024-02-02 13:17:09.261462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1827997608a2'
down_revision = '350397eae653'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('consumables', sa.String(length=250), nullable=True),
    sa.Column('manufacturer', sa.String(length=250), nullable=True),
    sa.Column('model', sa.String(length=250), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('cargo_capacity', sa.Integer(), nullable=True),
    sa.Column('cost_in_credits', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('favorit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'vehicle', ['vehicle_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorit', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('vehicle_id')

    op.drop_table('vehicle')
    # ### end Alembic commands ###
