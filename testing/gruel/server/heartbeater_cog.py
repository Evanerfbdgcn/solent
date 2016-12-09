#
# heartbeater (testing)
#
# // license
# Copyright 2016, Free Software Foundation.
#
# This file is part of Solent.
#
# Solent is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Solent is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Solent. If not, see <http://www.gnu.org/licenses/>.

from testing import run_tests
from testing import test
from testing.eng import engine_fake
from testing.gruel.server.receiver_cog import receiver_cog_fake

from solent.eng import activity_new
from solent.eng import log_snoop_new
from solent.eng import orb_new
from solent.eng.cs import *
from solent.gruel import gruel_schema_new
from solent.gruel import gruel_press_new
from solent.gruel import gruel_puff_new
from solent.gruel.server.gs_nearcast_schema import gs_nearcast_schema_new
from solent.gruel.server.heartbeater_cog import heartbeater_cog_new
from solent.gruel.server.server_customs_cog import server_customs_cog_new
from solent.gruel.server.server_customs_cog import ServerCustomsState
from solent.log import log
from solent.util import uniq

from enum import Enum
import sys

MTU = 500

@test
def should_start_on_announce_login_and_stop_on_announce_condrop():
    engine = engine_fake()
    clock = engine.get_clock()
    gruel_schema = gruel_schema_new()
    gruel_press = gruel_press_new(
        gruel_schema=gruel_schema,
        mtu=engine.mtu)
    gruel_puff = gruel_puff_new(
        gruel_schema=gruel_schema,
        mtu=engine.mtu)
    #
    orb = orb_new(
        engine=engine,
        nearcast_schema=gs_nearcast_schema_new())
    heartbeater_cog = orb.init_cog(
        construct=heartbeater_cog_new)
    r = orb.init_cog(
        construct=receiver_cog_fake)
    #
    # check starting assumptions
    assert 0 == r.count_heartbeat_send()
    #
    # scenario: time passes with no client logged in
    clock.inc(10)
    #
    # confirm effects
    assert 0 == r.count_heartbeat_send()
    #
    # scenario: client connects and one second passes
    r.nc_announce_login(
        max_packet_size=1400,
        max_fulldoc_size=20000)
    clock.inc(1)
    orb.cycle()
    #
    # confirm effects: we should see a heartbeat
    assert 1 == r.count_heartbeat_send()
    #
    # scenario: more than a second passes
    clock.inc(3)
    orb.cycle()
    #
    # confirm effects: we should see a new heartbeat
    assert 2 == r.count_heartbeat_send()
    #
    # scenario: condrop happens, and more time passes
    r.nc_announce_tcp_condrop()
    clock.inc(10)
    orb.cycle()
    #
    # confirm effects: we should see no new heartbeats
    assert 2 == r.count_heartbeat_send()
    #
    return True

if __name__ == '__main__':
    run_tests(
        unders_file=sys.modules['__main__'].__file__)
