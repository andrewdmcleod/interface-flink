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

import json
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class FlinkRequires(RelationBase):
    scope = scopes.GLOBAL

    def installed(self):
        return self.get_remote('installed', 'false').lower() == 'true'

    @hook('{requires:flink}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.related')

    @hook('{requires:flink}-relation-changed')
    def changed(self):
        conv = self.conversation()
        if self.installed():
            conv.set_state('{relation_name}.available')

    @hook('{provides:flink}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.related')
        conv.remove_state('{relation_name}.available')
