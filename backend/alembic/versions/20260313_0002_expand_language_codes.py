"""expand language codes to include de and fr

Revision ID: 20260313_0002
Revises: 20260312_0001
Create Date: 2026-03-13 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260313_0002"
down_revision = "20260312_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "locale",
        existing_type=sa.Enum("en", "es", "ru", name="language_code", native_enum=False),
        type_=sa.Enum("en", "es", "de", "fr", "ru", name="language_code", native_enum=False),
        existing_nullable=False,
        existing_server_default="en",
    )
    op.alter_column(
        "user_settings",
        "language",
        existing_type=sa.Enum("en", "es", "ru", name="language_code_settings", native_enum=False),
        type_=sa.Enum("en", "es", "de", "fr", "ru", name="language_code_settings", native_enum=False),
        existing_nullable=False,
        existing_server_default="en",
    )


def downgrade() -> None:
    op.alter_column(
        "user_settings",
        "language",
        existing_type=sa.Enum("en", "es", "de", "fr", "ru", name="language_code_settings", native_enum=False),
        type_=sa.Enum("en", "es", "ru", name="language_code_settings", native_enum=False),
        existing_nullable=False,
        existing_server_default="en",
    )
    op.alter_column(
        "users",
        "locale",
        existing_type=sa.Enum("en", "es", "de", "fr", "ru", name="language_code", native_enum=False),
        type_=sa.Enum("en", "es", "ru", name="language_code", native_enum=False),
        existing_nullable=False,
        existing_server_default="en",
    )
