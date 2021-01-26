import scurry.net.ping as ping


def test_parse_ping_line():
    line = "64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.056 ms"
    parsed = ping.parse_ping_line(line)

    assert parsed.host == "127.0.0.1"
    assert parsed.latency == 0.056


def test_ping():
    results = ping.ping("127.0.0.1", count=3)
