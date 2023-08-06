from manhattan.assets import transforms

__all__ = ['default_og_image_variations']


def default_og_image_variations():
    """Return the default set of image variations for the open graph image"""

    return {
        'socialcard': [
            transforms.images.Fit(1200, 1200),
            transforms.images.Output('jpg', 75)
        ]
    }
