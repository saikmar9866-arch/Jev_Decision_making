import os
import sys
from pathlib import Path

# Fix: Ensure double underscores around __file__
WORKSPACE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE_ROOT))

import fastf1
import pandas as pd
from src.engine.policy import JEVPolicyEngine


def main() -> None:
    print("\n==============================================")
    print("   JEV DECISION ENGINE - STAGE 0 EVALUATION   ")
    print("==============================================\n", flush=True)

    # 1. Setup Local Caching
    cache_dir = WORKSPACE_ROOT / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))

    # 2. Ingest Monaco 2022 Session Data
    print("Loading F1 Session Data: 2022 Monaco Grand Prix (Race)...")
    session = fastf1.get_session(2022, "Monaco", "R")
    session.load(laps=True, telemetry=False, weather=False)

    # 3. Extract Charles Leclerc (LEC) Laps
    lec_laps = session.laps.pick_drivers("LEC")

    # 4. Evaluate Strategy
    engine = JEVPolicyEngine(
        wet_to_inter_threshold=100.0,
        inter_to_slick_threshold=89.0,
    )
    strategy_report = engine.evaluate_laps(lec_laps)

    # 5. Output Recommendation Matrix
    print("\nStrategy Recommendation Signals (Laps 17-23):", flush=True)
    print(strategy_report.iloc[16:23].to_string(index=False))
    print("\n==============================================\n")


if __name__ == "__main__":
    main()