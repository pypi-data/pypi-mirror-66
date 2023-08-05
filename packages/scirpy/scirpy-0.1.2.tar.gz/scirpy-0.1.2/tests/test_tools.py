# pylama:ignore=W0611,W0404
import pandas as pd
import scirpy as st
from scanpy import AnnData
import pytest
import numpy.testing as npt
import pandas.testing as pdt
import numpy as np
from scirpy._util import _get_from_uns
from .fixtures import adata_clonotype, adata_tra, adata_vdj, adata_diversity


def test_chain_pairing():
    obs = pd.DataFrame.from_records(
        [
            ["False", "nan", "nan", "nan", "nan", "nan"],
            ["True", "True", "AAAA", "BBBB", "CCCC", "DDDD"],
            ["True", "False", "AAAA", "BBBB", "CCCC", "DDDD"],
            ["True", "nan", "AAAA", "nan", "nan", "nan"],
            ["True", "False", "AAAA", "nan", "CCCC", "nan"],
            ["True", "False", "AAAA", "BBBB", "nan", "nan"],
            ["True", "False", "AAAA", "BBBB", "CCCC", "nan"],
            ["True", "False", "nan", "nan", "CCCC", "nan"],
            ["True", "False", "nan", "nan", "CCCC", "DDDD"],
            ["True", "False", "AAAA", "nan", "CCCC", "DDDD"],
        ],
        columns=[
            "has_tcr",
            "multi_chain",
            "TRA_1_cdr3",
            "TRA_2_cdr3",
            "TRB_1_cdr3",
            "TRB_2_cdr3",
        ],
    )
    adata = AnnData(obs=obs)
    res = st.tl.chain_pairing(adata, inplace=False)
    npt.assert_equal(
        res,
        [
            "No TCR",
            "Multichain",
            "Two full chains",
            "Orphan alpha",
            "Single pair",
            "Orphan alpha",
            "Extra alpha",
            "Orphan beta",
            "Orphan beta",
            "Extra beta",
        ],
    )


def test_clip_and_count_clonotypes(adata_clonotype):
    adata = adata_clonotype

    res = st._tools._clonal_expansion._clip_and_count(
        adata, groupby="group", target_col="clonotype", clip_at=2, inplace=False
    )
    npt.assert_equal(res, np.array([">= 2"] * 3 + ["1"] * 4 + [">= 2"] * 2))

    # check without group
    res = st._tools._clonal_expansion._clip_and_count(
        adata, target_col="clonotype", clip_at=5, inplace=False
    )
    npt.assert_equal(res, np.array(["4"] * 3 + ["1"] + ["4"] + ["1"] * 2 + ["2"] * 2))

    # check if target_col works
    adata.obs["new_col"] = adata.obs["clonotype"]
    adata.obs.drop("clonotype", axis="columns", inplace=True)

    st._tools._clonal_expansion._clip_and_count(
        adata, groupby="group", target_col="new_col", clip_at=2,
    )
    npt.assert_equal(
        adata.obs["new_col_clipped_count"],
        np.array([">= 2"] * 3 + ["1"] * 4 + [">= 2"] * 2),
    )

    # check if it raises value error if target_col does not exist
    with pytest.raises(ValueError):
        st._tools._clonal_expansion._clip_and_count(
            adata, groupby="group", target_col="clonotype", clip_at=2, fraction=False,
        )


def test_clonal_expansion(adata_clonotype):
    res = st.tl.clonal_expansion(
        adata_clonotype, expanded_in="group", clip_at=2, inplace=False
    )
    npt.assert_equal(res, np.array([">= 2"] * 3 + ["1"] * 4 + [">= 2"] * 2))

    res = st.tl.clonal_expansion(adata_clonotype, clip_at=2, inplace=False)
    npt.assert_equal(
        res, np.array([">= 2"] * 3 + ["1"] + [">= 2"] + ["1"] * 2 + [">= 2"] * 2)
    )


def test_clonal_expansion_summary(adata_clonotype):
    res = st.tl.summarize_clonal_expansion(
        adata_clonotype, "group", target_col="clonotype", clip_at=2, normalize=True
    )
    pdt.assert_frame_equal(
        res,
        pd.DataFrame.from_dict(
            {"group": ["A", "B"], "1": [0, 2 / 5], ">= 2": [1.0, 3 / 5]}
        ).set_index("group"),
        check_names=False,
    )

    # test the `expanded_in` parameter.
    res = st.tl.summarize_clonal_expansion(
        adata_clonotype,
        "group",
        target_col="clonotype",
        clip_at=2,
        normalize=True,
        expanded_in="group",
    )
    pdt.assert_frame_equal(
        res,
        pd.DataFrame.from_dict(
            {"group": ["A", "B"], "1": [0, 3 / 5], ">= 2": [1.0, 2 / 5]}
        ).set_index("group"),
        check_names=False,
    )

    # test the `summarize_by` parameter.
    res = st.tl.summarize_clonal_expansion(
        adata_clonotype,
        "group",
        target_col="clonotype",
        clip_at=2,
        normalize=True,
        summarize_by="clonotype",
    )
    pdt.assert_frame_equal(
        res,
        pd.DataFrame.from_dict(
            {"group": ["A", "B"], "1": [0, 2 / 4], ">= 2": [1.0, 2 / 4]}
        ).set_index("group"),
        check_names=False,
    )

    res_counts = st.tl.summarize_clonal_expansion(
        adata_clonotype, "group", target_col="clonotype", clip_at=2, normalize=False
    )
    print(res_counts)
    pdt.assert_frame_equal(
        res_counts,
        pd.DataFrame.from_dict(
            {"group": ["A", "B"], "1": [0, 2], ">= 2": [3, 3]}
        ).set_index("group"),
        check_names=False,
        check_dtype=False,
    )


def test_alpha_diversity(adata_diversity):
    res = st.tl.alpha_diversity(
        adata_diversity, groupby="group", target_col="clonotype_", inplace=False
    )
    assert res.to_dict(orient="index") == {"A": {0: 0.0}, "B": {0: 1.0}}

    st.tl.alpha_diversity(
        adata_diversity, groupby="group", target_col="clonotype_", inplace=True
    )
    npt.assert_equal(
        adata_diversity.obs["alpha_diversity_clonotype_"].values,
        np.array([0.0] * 4 + [1.0] * 4),
    )


def test_group_abundance():
    obs = pd.DataFrame.from_records(
        [
            ["cell1", "A", "ct1"],
            ["cell2", "A", "ct1"],
            ["cell3", "A", "ct1"],
            ["cell3", "A", "NaN"],
            ["cell4", "B", "ct1"],
            ["cell5", "B", "ct2"],
        ],
        columns=["cell_id", "group", "clonotype"],
    ).set_index("cell_id")
    adata = AnnData(obs=obs)

    # Check counts
    res = st.tl.group_abundance(
        adata, groupby="clonotype", target_col="group", fraction=False
    )
    expected_count = pd.DataFrame.from_dict(
        {"ct1": {"A": 3.0, "B": 1.0}, "ct2": {"A": 0.0, "B": 1.0},}, orient="index",
    )
    npt.assert_equal(res.values, expected_count.values)

    # Check fractions
    res = st.tl.group_abundance(
        adata, groupby="clonotype", target_col="group", fraction=True
    )
    expected_frac = pd.DataFrame.from_dict(
        {"ct1": {"A": 0.75, "B": 0.25}, "ct2": {"A": 0.0, "B": 1.0},}, orient="index",
    )
    npt.assert_equal(res.values, expected_frac.values)

    # Check swapped
    res = st.tl.group_abundance(
        adata, groupby="group", target_col="clonotype", fraction=True
    )
    expected_frac = pd.DataFrame.from_dict(
        {"A": {"ct1": 1.0, "ct2": 0.0}, "B": {"ct1": 0.5, "ct2": 0.5},}, orient="index",
    )
    npt.assert_equal(res.values, expected_frac.values)


def test_spectratype(adata_tra):
    # Check numbers
    res1 = st.tl.spectratype(
        adata_tra, groupby="TRA_1_cdr3", target_col="sample", fraction=False,
    )
    res2 = st.tl.spectratype(
        adata_tra, groupby=("TRA_1_cdr3",), target_col="sample", fraction=False,
    )
    expected_count = pd.DataFrame.from_dict(
        {
            0: {1: 0.0, 3: 0.0, 5: 0.0},
            1: {1: 0.0, 3: 0.0, 5: 0.0},
            2: {1: 0.0, 3: 0.0, 5: 0.0},
            3: {1: 0.0, 3: 0.0, 5: 0.0},
            4: {1: 0.0, 3: 0.0, 5: 0.0},
            5: {1: 0.0, 3: 0.0, 5: 0.0},
            6: {1: 0.0, 3: 0.0, 5: 0.0},
            7: {1: 0.0, 3: 0.0, 5: 0.0},
            8: {1: 0.0, 3: 0.0, 5: 0.0},
            9: {1: 0.0, 3: 0.0, 5: 0.0},
            10: {1: 0.0, 3: 0.0, 5: 0.0},
            11: {1: 0.0, 3: 0.0, 5: 0.0},
            12: {1: 1.0, 3: 2.0, 5: 0.0},
            13: {1: 2.0, 3: 0.0, 5: 0.0},
            14: {1: 0.0, 3: 2.0, 5: 1.0},
            15: {1: 2.0, 3: 1.0, 5: 1.0},
            16: {1: 0.0, 3: 0.0, 5: 0.0},
            17: {1: 0.0, 3: 0.0, 5: 2.0},
        },
        orient="index",
    )
    npt.assert_equal(res1.values, expected_count.values)
    npt.assert_equal(res2.values, expected_count.values)

    # Check fractions
    res = st.tl.spectratype(
        adata_tra, groupby="TRA_1_cdr3", target_col="sample", fraction="sample"
    )
    expected_frac = pd.DataFrame.from_dict(
        {
            0: {1: 0.0, 3: 0.0, 5: 0.0},
            1: {1: 0.0, 3: 0.0, 5: 0.0},
            2: {1: 0.0, 3: 0.0, 5: 0.0},
            3: {1: 0.0, 3: 0.0, 5: 0.0},
            4: {1: 0.0, 3: 0.0, 5: 0.0},
            5: {1: 0.0, 3: 0.0, 5: 0.0},
            6: {1: 0.0, 3: 0.0, 5: 0.0},
            7: {1: 0.0, 3: 0.0, 5: 0.0},
            8: {1: 0.0, 3: 0.0, 5: 0.0},
            9: {1: 0.0, 3: 0.0, 5: 0.0},
            10: {1: 0.0, 3: 0.0, 5: 0.0},
            11: {1: 0.0, 3: 0.0, 5: 0.0},
            12: {1: 0.2, 3: 0.4, 5: 0.0},
            13: {1: 0.4, 3: 0.0, 5: 0.0},
            14: {1: 0.0, 3: 0.4, 5: 0.25},
            15: {1: 0.4, 3: 0.2, 5: 0.25},
            16: {1: 0.0, 3: 0.0, 5: 0.0},
            17: {1: 0.0, 3: 0.0, 5: 0.5},
        },
        orient="index",
    )
    npt.assert_equal(res.values, expected_frac.values)


def repertoire_overlap(adata_tra):
    res = st.tl.repertoire_overlap(adata, 'sample')
    expected_cnt = pd.DataFrame.from_dict(
        {
            1: {
                'clonotype_157': 0.0,
                'clonotype_158': 0.0,
                'clonotype_284': 0.0,
                'clonotype_330': 0.0,
                'clonotype_425': 0.0,
                'clonotype_430': 0.0,
                'clonotype_458': 0.0,
                'clonotype_459': 1.0,
                'clonotype_460': 0.0,
                'clonotype_592': 0.0,
                'clonotype_738': 1.0,
                'clonotype_739': 1.0,
                'clonotype_986': 1.0,
                'clonotype_987': 1.0
            },
            3: {
                'clonotype_157': 0.0,
                'clonotype_158': 0.0,
                'clonotype_284': 0.0,
                'clonotype_330': 1.0,
                'clonotype_425': 1.0,
                'clonotype_430': 1.0,
                'clonotype_458': 1.0,
                'clonotype_459': 0.0,
                'clonotype_460': 1.0,
                'clonotype_592': 0.0,
                'clonotype_738': 0.0,
                'clonotype_739': 0.0,
                'clonotype_986': 0.0,
                'clonotype_987': 0.0
                },
            5: {
                'clonotype_157': 1.0,
                'clonotype_158': 1.0,
                'clonotype_284': 1.0,
                'clonotype_330': 0.0,
                'clonotype_425': 0.0,
                'clonotype_430': 0.0,
                'clonotype_458': 0.0,
                'clonotype_459': 0.0,
                'clonotype_460': 0.0,
                'clonotype_592': 1.0,
                'clonotype_738': 0.0,
                'clonotype_739': 0.0,
                'clonotype_986': 0.0,
                'clonotype_987': 0.0
                }
            },
        orient="index",
    )
    npt.assert_equal(res.values, expected_cnt.values)