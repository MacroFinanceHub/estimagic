import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from estimagic.visualization.comparison_plot import _prep_result_df

# ===========================================================================
# FIXTURES
# ===========================================================================


@pytest.fixture()
def minimal_res_dict():
    groups = ["a", "a", "b", "b", "b", "b", "c"]
    names = ["u", "i", "a", "e", "n", "r", "t"]

    df1 = pd.DataFrame()
    df1["group"] = groups
    df1["name"] = names
    df1["final_value"] = [1.58, 2.01, 2.73, 1.62, 2.18, 1.75, 2.25]

    df2 = pd.DataFrame()
    df2["group"] = groups + ["c", "d", "d"]
    df2["name"] = names + ["x", "v", "l"]
    df2["final_value"] = [1.48, 1.82, 1.12, 2.15, 1.65, 1.93, 2.39, 1.68, -1.24, -0.95]

    df3 = df1.copy()
    df3["final_value"] += [-0.23, -0.2, -0.11, 0.03, -0.13, -0.21, 0.17]

    df4 = df2.copy()
    df4["final_value"] += [0.4, -0.2, -0.6, -0.0, 0.2, -0.1, 0.1, -0.1, 0.0, -0.3]

    res_dict = {
        "mod1": {"result_df": df1},
        "mod2": {"result_df": df2, "model_class": "class2"},
        "mod3": {"result_df": df3},
        "mod4": {"result_df": df4},
    }
    return res_dict


@pytest.fixture()
def res_dict_with_model_class(minimal_res_dict):
    res_dict = minimal_res_dict
    res_dict["mod2"]["model_class"] = "large"
    res_dict["mod4"]["model_class"] = "large"
    return res_dict


# _prep_result_df
# ===========================================================================


def test_prep_result_df(minimal_res_dict):
    model = "mod1"
    model_dict = minimal_res_dict[model]
    res = _prep_result_df(model_dict, model)
    expected = pd.DataFrame.from_dict(
        {
            "group": {0: "a", 1: "a", 2: "b", 3: "b", 4: "b", 5: "b", 6: "c"},
            "name": {0: "u", 1: "i", 2: "a", 3: "e", 4: "n", 5: "r", 6: "t"},
            "final_value": {
                0: 1.58,
                1: 2.01,
                2: 2.73,
                3: 1.62,
                4: 2.18,
                5: 1.75,
                6: 2.25,
            },
            "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
            "full_name": {
                0: "a_u",
                1: "a_i",
                2: "b_a",
                3: "b_e",
                4: "b_n",
                5: "b_r",
                6: "c_t",
            },
            "model_class": {
                0: "no class",
                1: "no class",
                2: "no class",
                3: "no class",
                4: "no class",
                5: "no class",
                6: "no class",
            },
            "model": {
                0: "mod1",
                1: "mod1",
                2: "mod1",
                3: "mod1",
                4: "mod1",
                5: "mod1",
                6: "mod1",
            },
        }
    )
    assert_frame_equal(res, expected, check_like=True)


# _df_with_all_results
# ===========================================================================


# _create_plot_specs
# ===========================================================================


# _determine_plot_heights
# ===========================================================================


# _determine_figure_height
# ===========================================================================


# _add_plot_specs_to_df
# ===========================================================================


# _add_color_column
# ===========================================================================


# _add_dodge_and_binned_x
# ===========================================================================


# _find_next_lower
# ===========================================================================


# _find_next_upper
# ===========================================================================


# _flatten_dict
# ===========================================================================