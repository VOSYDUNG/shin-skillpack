"""Count reported session tokens without exposing messages or estimating money."""
import argparse
import json
from datetime import datetime
from pathlib import Path

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")


def inspect(path):
    session_id = None
    latest = None
    count = malformed = 0
    model = None
    last_timestamp = None
    with Path(path).open(encoding="utf-8-sig") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if not isinstance(event, dict):
                malformed += 1
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            if event.get("type") == "session_meta":
                session_id = payload.get("id", session_id)
            if event.get("type") == "turn_context":
                model = payload.get("model", model)
            if event.get("type") == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info")
                totals = info.get("total_token_usage") if isinstance(info, dict) else None
                if isinstance(totals, dict):
                    latest = {key: value if type(value := totals.get(key)) is int and value >= 0 else None for key in FIELDS}
                    last_timestamp = event.get("timestamp")
                    count += 1
    return {"session_id": session_id, "file": str(Path(path).resolve()), "last_observed_model": model,
            "status": "REPORTED" if latest else "UNKNOWN", "last_reported_total": latest,
            "last_counter_timestamp": last_timestamp, "file_mtime": Path(path).stat().st_mtime,
            "cumulative_events_observed": count, "malformed_lines": malformed}


def summarize(paths):
    results = []
    seen = {}
    for path in paths:
        try:
            result = inspect(path)
        except (OSError, UnicodeError):
            results.append({"file": str(Path(path).resolve()), "status": "UNREADABLE"})
            continue
        key = result["session_id"] or result["file"]
        if key not in seen:
            seen[key] = len(results)
            results.append(result)
            continue
        previous = results[seen[key]]
        if result["status"] != previous["status"]:
            choose_new = result["status"] == "REPORTED"
        else:
            try:
                old_time = datetime.fromisoformat(previous["last_counter_timestamp"].replace("Z", "+00:00"))
                new_time = datetime.fromisoformat(result["last_counter_timestamp"].replace("Z", "+00:00"))
                choose_new = new_time > old_time
            except (AttributeError, TypeError, ValueError):
                choose_new = result["file_mtime"] > previous["file_mtime"]
        if choose_new:
            results[seen[key]] = result
    return {"schema_version": 1, "sessions": results, "cost": "UNKNOWN", "quota_attribution": "UNKNOWN",
            "method": "Last cumulative counter per unique session. Duplicate snapshots select newest counter timestamp; if unavailable, file mtime is a heuristic. Prefer a reported counter over an unknown snapshot. Components overlap; do not add them. No cross-session total: parent/child counters may overlap. Last model is not per-model attribution. Running sessions are partial."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcripts", nargs="+")
    args = parser.parse_args()
    result = summarize(args.transcripts)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if any(row["status"] == "UNREADABLE" for row in result["sessions"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
