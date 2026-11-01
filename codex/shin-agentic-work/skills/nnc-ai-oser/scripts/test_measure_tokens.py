import json
import os
from pathlib import Path
import tempfile
import unittest
from measure_tokens import summarize


class TokenTests(unittest.TestCase):
    def test_cumulative_not_summed_and_duplicate_session_not_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            events = [{"type": "session_meta", "payload": {"id": "session-a"}}]
            for n in (10, 30):
                events.append({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": n, "total_tokens": n + 3}}}})
            path.write_text("\n".join(map(json.dumps, events)), encoding="utf-8")
            result = summarize([path, path])
            self.assertEqual(len(result["sessions"]), 1)
            self.assertEqual(result["sessions"][0]["last_reported_total"]["input_tokens"], 30)
            self.assertIsNone(result["sessions"][0]["last_reported_total"]["output_tokens"])
            self.assertEqual(result["cost"], "UNKNOWN")

    def test_missing_counter_is_unknown_no_messages_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            path.write_text('{"type":"response_item","payload":{"content":"PRIVATE_MARKER"}}\n{broken', encoding="utf-8")
            result = summarize([path])
            self.assertEqual(result["sessions"][0]["status"], "UNKNOWN")
            self.assertEqual(result["sessions"][0]["malformed_lines"], 1)
            self.assertNotIn("PRIVATE_MARKER", json.dumps(result))

    def test_duplicate_snapshots_choose_newest_counter_in_either_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / "old.jsonl", Path(tmp) / "new.jsonl"]
            for index, path in enumerate(paths):
                events = [{"type": "session_meta", "payload": {"id": "same-session"}},
                          {"type": "event_msg", "timestamp": f"2026-09-10T0{index}:00:00Z", "payload": {"type": "token_count", "info": {"total_token_usage": {"total_tokens": 100 * (index + 1)}}}}]
                path.write_text("\n".join(map(json.dumps, events)), encoding="utf-8")
                os.utime(path, (1000 - index, 1000 - index))
            for order in (paths, paths[::-1]):
                result = summarize(order)
                self.assertEqual(len(result["sessions"]), 1)
                self.assertEqual(result["sessions"][0]["last_reported_total"]["total_tokens"], 200)
            for path in paths:
                events = [json.loads(line) for line in path.read_text().splitlines()]
                events[1].pop("timestamp")
                path.write_text("\n".join(map(json.dumps, events)), encoding="utf-8")
            os.utime(paths[0], (1000, 1000))
            os.utime(paths[1], (2000, 2000))
            self.assertEqual(summarize(paths[::-1])["sessions"][0]["last_reported_total"]["total_tokens"], 200)


if __name__ == "__main__":
    unittest.main()
