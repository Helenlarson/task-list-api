from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "90c04030ba1e"
down_revision = None  # deve ser None porque você resetou as migrations
branch_labels = None
depends_on = None

def upgrade():
    # Se existir string vazia na coluna, transforme em NULL para não quebrar o cast
    op.execute("UPDATE task SET completed_at = NULL WHERE completed_at = ''")

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column(
            'completed_at',
            existing_type=sa.String(),
            type_=sa.DateTime(),
            existing_nullable=True,
            nullable=True,
            postgresql_using="completed_at::timestamp without time zone",
        )

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column(
            'completed_at',
            existing_type=sa.DateTime(),
            type_=sa.String(),
            existing_nullable=True,
            nullable=True,
            postgresql_using="completed_at::text",
        )
