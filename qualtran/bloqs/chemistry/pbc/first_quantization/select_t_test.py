#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from qualtran.bloqs.chemistry.pbc.first_quantization.select_t import (
    _select_t,
    SelectTFirstQuantization,
)
from qualtran.resource_counting import get_cost_value, QECGatesCost


def test_select_t(bloq_autotester):
    bloq_autotester(_select_t)


def test_select_kinetic_t_counts():
    num_bits_p = 6
    sel = SelectTFirstQuantization(num_bits_p, 10)
    toffolis = get_cost_value(sel, QECGatesCost()).total_toffoli_only()
    assert toffolis == 5 * (num_bits_p - 1) + 2
