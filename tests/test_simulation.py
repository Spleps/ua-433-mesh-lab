from ua433_mesh.model import Node, Packet
from ua433_mesh.simulation import choose_profile, find_route, simulate_delivery


def test_profile_switches_at_fast_link_range():
    assert choose_profile(200).name == "fast"
    assert choose_profile(500).name == "robust"


def test_route_uses_relay_when_direct_hop_is_too_long():
    nodes = [Node("a", 0), Node("b", 300), Node("c", 800)]
    assert [node.node_id for node in find_route(nodes, "a", "c")] == ["a", "b", "c"]


def test_expired_packet_is_not_delivered():
    result = simulate_delivery(
        [Node("a", 0), Node("b", 200)],
        "a",
        "b",
        Packet("a-1", "a", "HELP", created_at_s=0, valid_for_s=5),
        now_s=6,
    )
    assert result.delivered is False
    assert result.replay_accepted is False


def test_delivered_packet_cannot_be_replayed():
    result = simulate_delivery(
        [Node("a", 0), Node("b", 200)],
        "a",
        "b",
        Packet("a-1", "a", "CONTACT", created_at_s=10),
        now_s=11,
    )
    assert result.delivered is True
    assert result.replay_accepted is False

