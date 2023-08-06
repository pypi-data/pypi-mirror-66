import pandas as pd
import numpy as np
import sys

from plotnine.coords import coord_flip
from plotnine.geoms.geom_rect import geom_rect
from plotnine.geoms.annotate import annotate

from itertools import islice, cycle


class annotation_stripes_dppd(annotate):
    """
    Alternating stripes, centered around each label.

    see https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.annotation_stripes.html#plotnine.geoms.annotation_stripes

    This fixes the fill_range to be on by default, extend
    in the color of the first/last range (instead of adding two more ranges
    of alternating color), and the fills actually start with your first one.
    """

    def __init__(self, **kwargs):
        if "direction" in kwargs:
            allowed = ("vertical", "horizontal")
            if (not isinstance(kwargs["direction"], str)) or (
                kwargs["direction"] not in allowed
            ):
                raise ValueError("direction must be one of %s" % (allowed,))
        if not "fill_range" in kwargs:
            kwargs["fill_range"] = True
        if "fill" in kwargs:
            kwargs["fill"] = list(
                islice(cycle(kwargs["fill"]), 1, len(kwargs["fill"]) + 1)
            )

        self._annotation_geom = _geom_stripes(**kwargs)


anno_stripes_module = sys.modules[
    "plotnine.geoms.annotation_stripes"
]  # plotnine shadows the module with the type


class _geom_stripes(anno_stripes_module._geom_stripes):
    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        extend = params["extend"]
        fill_range = params["fill_range"]
        direction = params["direction"]

        # Range
        if direction == "vertical":
            axis, other_axis = "x", "y"
        else:
            axis, other_axis = "y", "x"

        if isinstance(coord, coord_flip):
            axis, other_axis = other_axis, axis

        breaks = getattr(panel_params, axis).breaks
        range = getattr(panel_params, axis).range
        other_range = getattr(panel_params, other_axis).range

        # Breaks along the width
        n_stripes = len(breaks)
        if n_stripes > 1:
            diff = np.diff(breaks)
            step = diff[0]
            equal_spaces = np.all(diff == step)
            if not equal_spaces:
                raise ValueError(
                    "The major breaks are not equally spaced. "
                    "We cannot create stripes."
                )
        else:
            step = breaks[0]

        deltas = np.array([step / 2] * n_stripes)
        xmin = breaks - deltas
        xmax = breaks + deltas
        if fill_range:
            if range[0] < breaks[0]:
                n_stripes += 1
                xmax = np.insert(xmax, 0, xmin[0])
                xmin = np.insert(xmin, 0, range[0])
            if range[1] > breaks[1]:
                n_stripes += 1
                xmin = np.append(xmin, xmax[-1])
                xmax = np.append(xmax, range[1])

        # Height
        full_height = other_range[1] - other_range[0]
        ymin = other_range[0] + full_height * extend[0]
        ymax = other_range[0] + full_height * extend[1]
        fill = list(islice(cycle(params["fill"]), n_stripes))
        if fill_range:
            # change from plotnine - I want them to blend into the existing stripes!
            fill[0] = fill[1]
            fill[-1] = fill[-2]

        if direction != "vertical":
            xmin, xmax, ymin, ymax = ymin, ymax, xmin, xmax

        data = pd.DataFrame(
            {
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
                "fill": fill,
                "alpha": params["alpha"],
                "color": params["color"],
                "linetype": params["linetype"],
                "size": params["size"],
            }
        )

        return geom_rect.draw_group(data, panel_params, coord, ax, **params)
