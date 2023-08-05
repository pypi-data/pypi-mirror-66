# Copyright 2020 The fingym Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fingym.envs.aapl_envs import AaplDailyEnv

import pytest

@pytest.fixture
def aapl_daily_v0_env():
    return AaplDailyEnv()

def test_make_aapl_daily_v0_env(aapl_daily_v0_env):
    assert type(aapl_daily_v0_env) == AaplDailyEnv

def test_amd_daily_v0_file_location(aapl_daily_v0_env):
    assert 'filtered_aapl_data' in aapl_daily_v0_env._get_data_file()