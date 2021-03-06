"""soft delete post

Revision ID: ff2b8e7166bc
Revises: 4c264698869c
Create Date: 2022-01-23 19:41:30.329708

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ff2b8e7166bc'
down_revision = '4c264698869c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deleted_posts',
                    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('soft_deleted_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(('post_id',), ['post.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_id')
                    )
    op.create_index(op.f('ix_deleted_posts_soft_deleted_at'), 'deleted_posts', ['soft_deleted_at'], unique=False)

    op.alter_column('post', 'create_datetime', new_column_name='created_at')
    op.drop_index('ix_post_create_datetime', table_name='post')
    op.create_index(op.f('ix_post_created_at'), 'post', ['created_at'], unique=False)

    op.drop_constraint('post_author_id_fkey', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['author_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('session_user_id_fkey', 'session', type_='foreignkey')
    op.create_foreign_key(None, 'session', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('session_user_id_fkey', 'session', type_='foreignkey')
    op.create_foreign_key('session_user_id_fkey', 'session', 'user', ['user_id'], ['id'])
    op.drop_constraint('post_author_id_fkey', 'post', type_='foreignkey')
    op.create_foreign_key('post_author_id_fkey', 'post', 'user', ['author_id'], ['id'])

    op.drop_index(op.f('ix_post_created_at'), table_name='post')
    op.alter_column('post', 'created_at', new_column_name='create_datetime')
    op.create_index('ix_post_create_datetime', 'post', ['create_datetime'], unique=False)

    op.drop_index(op.f('ix_deleted_posts_soft_deleted_at'), table_name='deleted_posts')
    op.drop_table('deleted_posts')
    # ### end Alembic commands ###
