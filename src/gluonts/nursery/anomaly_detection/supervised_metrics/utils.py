# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# Standard library imports
from typing import List

# Third-party imports
import numpy as np


def range_overlap(left_range: range, right_range: range,) -> bool:
    """
    Checks if two ranges have an overlap.
    Here each range is assumed to be consecutive, i.e., `step` field of `range` is always 1.

    Parameters
    ----------
    left_range
    right_range

    Returns
    -------
    True or False depending on the overlap.

    """
    if left_range[0] <= right_range[-1] and left_range[-1] >= right_range[0]:
        return True
    return False


def labels_to_ranges(labels: List[bool]) -> List[range]:
    """
    Converts the given list of labels to list of anomaly (defined by positive label) ranges.

    Parameters
    ----------
    labels
        Boolean list of labels.

    Returns
    -------
    List of ranges.

    """

    ranges_ls = []
    start_ix = None
    stop_ix = None
    for ix, label in enumerate(labels):
        if label:
            # this might be the last positive label in the anomaly range
            stop_ix = ix + 1
            if start_ix is None:
                # a new positive label is seen
                start_ix = ix
        elif start_ix is not None:
            # a consecutive sequence of positive labels is ended
            assert stop_ix is not None
            ranges_ls.append(range(start_ix, stop_ix))
            start_ix = None

    if start_ix is not None:
        # the last element of `labels` is True, we never ended that range
        assert stop_ix is not None
        ranges_ls.append(range(start_ix, stop_ix))

    return ranges_ls


def ranges_to_singletons(ranges: List[range],) -> List[range]:
    """
    Convenient function to convert list of consecutive ranges to list of singleton ranges.

    Parameters
    ----------
    ranges
        List of ranges.

    Returns
    -------
    List of singleton ranges.

    """
    assert all(
        r.step == 1 and r.start >= 0 and r.stop >= 0 for r in ranges
    ), "Ranges should be consecutive and contain non-negative indices."

    return [range(i, i + 1) for r in ranges for i in r]
