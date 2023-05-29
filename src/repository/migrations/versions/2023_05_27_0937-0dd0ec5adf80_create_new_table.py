"""Create new table

Revision ID: 0dd0ec5adf80
Revises: 
Create Date: 2023-05-27 09:37:59.853431

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '0dd0ec5adf80'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table('cargo',
    sa.Column('pick_up_lat', sa.Numeric(scale=6), nullable=False),
    sa.Column('pick_up_lng', sa.Numeric(scale=6), nullable=False),
    sa.Column('pick_up_post_code', sa.String(length=15), nullable=False),
    sa.Column('pick_up', Geometry(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('delivery_lat', sa.Numeric(scale=6), nullable=False),
    sa.Column('delivery_lng', sa.Numeric(scale=6), nullable=False),
    sa.Column('delivery_post_code', sa.String(length=15), nullable=False),
    sa.Column('delivery', Geometry(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('weight', sa.Numeric(scale=3), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_index('idx_cargo_delivery', 'cargo', ['delivery'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_index('idx_cargo_pick_up', 'cargo', ['pick_up'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('location',
    sa.Column('country', sa.String(length=400), nullable=False),
    sa.Column('state', sa.String(length=400), nullable=False),
    sa.Column('city', sa.String(length=400), nullable=False),
    sa.Column('post_code', sa.String(length=15), nullable=False),
    sa.Column('location', Geometry(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('lat', sa.Numeric(scale=6), nullable=False),
    sa.Column('lng', sa.Numeric(scale=6), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_index('idx_location_location', 'location', ['location'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_geospatial_table('transport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_lng', sa.Numeric(scale=6), nullable=False),
    sa.Column('location_lat', sa.Numeric(scale=6), nullable=False),
    sa.Column('transport_number', sa.String(length=5), nullable=False),
    sa.Column('location', Geometry(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.Column('payload_capacity', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_index('idx_transport_location', 'transport', ['location'], unique=False, postgresql_using='gist', postgresql_ops={})
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index('idx_transport_location', table_name='transport', postgresql_using='gist', column_name='location')
    op.drop_geospatial_table('transport')
    op.drop_geospatial_index('idx_location_location', table_name='location', postgresql_using='gist', column_name='location')
    op.drop_geospatial_table('location')
    op.drop_geospatial_index('idx_cargo_pick_up', table_name='cargo', postgresql_using='gist', column_name='pick_up')
    op.drop_geospatial_index('idx_cargo_delivery', table_name='cargo', postgresql_using='gist', column_name='delivery')
    op.drop_geospatial_table('cargo')
    # ### end Alembic commands ###