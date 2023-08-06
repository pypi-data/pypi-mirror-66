"""
Generic update SEO meta chain.

: `form_cls`
    The form that will be used to capture and validate the updated details of
    the document (required).

: `projection`
    The projection used when requesting the document from the database (defaults
    to None which means the detault projection for the frame class will be
    used).
"""

import flask
from manhattan.assets import Asset, transforms
from manhattan.assets.fields import AssetField
from manhattan.assets.validators import AssetType
from manhattan.assets.transforms.base import BaseTransform
from manhattan.chains import Chain, ChainMgr
from manhattan.forms import BaseForm, fields, validators
from manhattan.nav import Nav, NavItem
from manhattan.manage.views import factories, utils
from mongoframes import Q

__all__ = [
    'update_chains',
    'UpdateForm'
]


# Forms

class UpdateForm(BaseForm):

    # Head
    title = fields.StringField(
        'Title',
        render_kw={
            'data-mh-character-count': '',
            'data-mh-character-count--max-characters': 60
        }
    )
    full_title = fields.BooleanField('Full title')
    meta_description = fields.TextAreaField(
        'Meta description',
        render_kw={
            'data-mh-character-count': '',
            'data-mh-character-count--max-characters': 160
        }
    )
    meta_robots = fields.CheckboxField(
        'Meta robots',
        choices=[
            ('Noindex', 'Noindex'),
            ('Index', 'Index'),
            ('Follow', 'Follow'),
            ('Nofollow', 'Nofollow'),
            ('Noimageindex', 'Noimageindex'),
            ('None', 'None'),
            ('Noarchive', 'Noarchive'),
            ('Nocache', 'Nocache'),
            ('Nosnippet', 'Nosnippet')
        ]
    )

    # Sitemap
    exclude_from_sitemap = fields.BooleanField(
        'Exclude from sitemap'
    )
    sitemap_frequency = fields.SelectField(
        'Frequency',
        choices=[
            ('', 'Select...'),
            ('always', 'Always'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('never', 'Never'),
        ]
    )
    sitemap_priority = fields.FloatField(
        'Priority',
        validators=[validators.Optional()]
    )

    # Open graph
    og_title = fields.StringField(
        'Title',
        render_kw={
            'data-mh-character-count': '',
            'data-mh-character-count--max-characters': 90
        }
    )
    og_description = fields.TextAreaField(
        'Description',
        render_kw={
            'data-mh-character-count': '',
            'data-mh-character-count--max-characters': 200
        }
    )
    og_image =  AssetField(
        'Image',
        validators=[AssetType('image')],
        render_kw={
            'data-mh-file-field--file-type': 'image'
        }
    )
    og_audio = fields.StringField(
        'Audio (URL)',
        validators=[validators.Optional(), validators.URL()]
    )
    og_video = fields.StringField(
        'Video (URL)',
        validators=[validators.Optional(), validators.URL()]
    )


# Define the chains
update_chains = ChainMgr()

# GET
update_chains['get'] = Chain([
    'config',
    'authenticate',
    'get_document',
    'get_seo_meta',
    'init_form',
    'decorate',
    'render_template'
])

# POST
update_chains['post'] = Chain([
    'config',
    'authenticate',
    'get_document',
    'get_seo_meta',
    'init_form',
    'validate',
    [
        [
            'build_form_data',
            'update_document',
            'store_assets',
            'redirect'
        ],
        [
            'decorate',
            'render_template'
        ]
    ]
])

# Define the links
update_chains.set_link(
    factories.config(
        form_cls=UpdateForm,
        projection=None,
        seo_meta_projection=None
    )
)
update_chains.set_link(factories.authenticate())
update_chains.set_link(factories.get_document())
update_chains.set_link(factories.validate())
update_chains.set_link(factories.store_assets())
update_chains.set_link(factories.render_template('update_seo_meta.html'))
update_chains.set_link(factories.redirect('update_seo_meta', include_id=True))

@update_chains.link
def get_seo_meta(state):
    """
    Get the SEO meta from the document.

    This link adds the `seo_meta` key to the state.
    """
    document = state[state.manage_config.var_name]
    state.seo_meta = document.seo_meta_cls.one(
        Q.document == document,
        projection=state.seo_meta_projection or {
            'og_image': Asset.default_projection()
        }
    )

@update_chains.link
def decorate(state):
    """
    Add decor information to the state (see `utils.base_decor` for further
    details on what information the `decor` dictionary consists of).

    This link adds a `decor` key to the state.
    """
    document = state[state.manage_config.var_name]
    state.decor = utils.base_decor(
        state.manage_config,
        state.view_type,
        document
    )

    # Title
    state.decor['title'] = state.manage_config.titleize(document)

    # Breadcrumbs
    if Nav.exists(state.manage_config.get_endpoint('list')):
        state.decor['breadcrumbs'].add(
            utils.create_breadcrumb(state.manage_config, 'list')
        )
    if Nav.exists(state.manage_config.get_endpoint('view')):
        state.decor['breadcrumbs'].add(
            utils.create_breadcrumb(state.manage_config, 'view', document)
        )
    state.decor['breadcrumbs'].add(NavItem('SEO meta'))

@update_chains.link
def init_form(state):
    # Initialize the form
    form_data = None
    if flask.request.method == 'POST':
        form_data = flask.request.form

    # Initialize the form
    state.form = state.form_cls(form_data, obj=state.seo_meta)

@update_chains.link
def build_form_data(state):
    """
    Generate the form data that will be used to update the document.

    This link adds a `form_data` key to the the state containing the initialized
    form.
    """
    state.form_data = state.form.data

@update_chains.link
def update_document(state):
    """Update a document"""

    # Get the initialized document
    document = state[state.manage_config.var_name]
    seo_meta = state.seo_meta

    assert document, \
            'No `{0}` set in state'.format(state.manage_config.var_name)

    # Get a copy of the frames comparable data before the update
    original = seo_meta.comparable

    # Doesn't support `logged_update`
    for k, v in state.form_data.items():

        # Set empty values to None
        if not v and type(v) not in (float, int):
            v = None

        setattr(seo_meta, k, v)

    seo_meta.update()

    # And comparable difference is stored against the parent document not the
    # SEO meta.
    entry = document.__class__._change_log_cls({
        'type': 'UPDATED',
        'documents': [document],
        'user': state.manage_user
        })
    entry.add_diff(original, seo_meta.comparable)

    # Check there's a change to apply/log
    if entry.is_diff:
        entry.insert()

    # Flash message that the document was updated
    flask.flash('SEO meta updated.'.format(document=document))

@update_chains.link
def store_assets(state):

    if not getattr(flask.current_app, 'asset_mgr', None):
        return

    # Identify asset fields within the form
    seo_meta = state.seo_meta
    asset_fields = []

    for field in seo_meta.get_fields():

        if not isinstance(getattr(state.form, field, None), AssetField):
            continue

        asset_fields.append(field)

    # Build a list of assets to make permanent (persist), to generate new
    # variations for (transform) and to remove.
    assets_to_persist = []
    assets_to_transform = []
    assets_to_remove = []

    for field in asset_fields:

        asset = state.form_data.get(field)

        if asset:

            if asset.temporary:
                assets_to_persist.append(asset)

                if seo_meta.get(field):
                    assets_to_remove.append(seo_meta[field])

                if not asset.base_transforms:
                    continue

            elif not state.form[field].base_transform_modified:
                continue

        else:

            if seo_meta.get(field):
                assets_to_remove.append(seo_meta[field])

            continue

        # Build the transform instructions required to regenerate
        # variations for the asset.
        variations = state.manage_config.asset_variations.get(field, {})

        if asset.variations:

            # Check for local transforms against the asset which are added
            # to and may override variations defined for the field.
            for variation_name, variation_asset \
                    in asset.variations.items():

                if not isinstance(variation_asset, Asset):
                    variation_asset = Asset(variation_asset)

                variations[variation_name] = [
                    BaseTransform.from_json_type(t)
                    for t in variation_asset.local_transforms
                ]

        # Ensure the system set '--draft--' variation is never updated
        variations.pop('--draft--', None)

        if variations:

            # Add the tranform information for the asset (the asset,
            # variations and base transforms).
            assets_to_transform.append((
                asset,
                variations,
                [
                    BaseTransform.from_json_type(t)
                    for t in asset.base_transforms
                ]
            ))

    # Store assets permanently
    asset_mgr = flask.current_app.asset_mgr
    asset_mgr.persist_many(assets_to_persist)

    # Generate variations
    asset_mgr.generate_variations_for_many(
        [a[0] for a in assets_to_transform],
        {a[0].key: a[1] for a in assets_to_transform},
        {a[0].key: a[2] for a in assets_to_transform}
    )

    if asset_fields:

        # Update the seo meta
        if hasattr(seo_meta, 'logged_update'):
            seo_meta.logged_update(
                state.manage_user,
                {
                    field: state.form_data.get(field) or None
                    for field in asset_fields
                }
            )

        else:
            for field in asset_fields:
                setattr(
                    seo_meta,
                    field,
                    state.form_data.get(field) or None
                )

            seo_meta.update(*asset_fields)

    if state.remove_assets:

        # Remove assets
        asset_mgr.remove_many(assets_to_remove)
