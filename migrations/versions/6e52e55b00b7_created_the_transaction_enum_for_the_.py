from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6e52e55b00b7'
down_revision = 'ed58b572f65a'
branch_labels = None
depends_on = None

def upgrade():
    # Temporarily change the column type to text
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.VARCHAR(length=20),
            type_=sa.Text,
            existing_nullable=False
        )
    
    # Alter the column to use the new Enum type with a USING clause
    op.execute("""
        ALTER TABLE transactions
        ALTER COLUMN status TYPE transactionstatus
        USING status::transactionstatus
    """)

def downgrade():
    # Reverse the column type back to VARCHAR(20)
    op.execute("""
        ALTER TABLE transactions
        ALTER COLUMN status TYPE VARCHAR(20)
        USING status::text
    """)
