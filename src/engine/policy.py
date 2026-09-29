"""Strategy decision engine for Formula 1 tyre pit recommendations."""

from typing import Any, Dict, List, Optional
import pandas as pd


class JEVPolicyEngine:
    """Evaluates lap times against crossover thresholds to issue pit signals."""

    def __init__(
        self,
        wet_to_inter_threshold: float = 100.0,
        inter_to_slick_threshold: float = 89.0,
    ) -> None:
        """Initialize policy engine with crossover lap time thresholds (in seconds).
        
        Args:
            wet_to_inter_threshold: Lap time below which WET tyres should switch to INTER.
            inter_to_slick_threshold: Lap time below which INTER tyres should switch to SLICKS.
        """
        self.wet_to_inter_threshold = wet_to_inter_threshold
        self.inter_to_slick_threshold = inter_to_slick_threshold

    def evaluate_laps(self, driver_laps: pd.DataFrame) -> pd.DataFrame:
        """Evaluate driver lap times and generate strategic pit box signals.

        Args:
            driver_laps: FastF1 DataFrame containing driver lap telemetry data.

        Returns:
            pd.DataFrame: Summary table containing Lap, Compound, LapTime_Sec, and Signal.
        """
        results: List[Dict[str, Any]] = []

        for _, lap in driver_laps.iterrows():
            lap_num: Optional[int] = (
                int(lap["LapNumber"]) if pd.notnull(lap["LapNumber"]) else None
            )
            compound: Any = lap.get("Compound")
            lap_time = lap.get("LapTime")

            # Extract lap time in seconds safely
            lap_time_sec: Optional[float] = None
            if pd.notnull(lap_time) and hasattr(lap_time, "total_seconds"):
                lap_time_sec = float(lap_time.total_seconds())

            # Determine strategy signal based on crossover thresholds
            signal = "HOLD"
            if lap_time_sec is not None:
                if compound == "WET" and lap_time_sec < self.wet_to_inter_threshold:
                    signal = "BOX FOR INTERMEDIATES"
                elif compound == "INTERMEDIATE" and lap_time_sec < self.inter_to_slick_threshold:
                    signal = "BOX FOR SLICKS"

            results.append(
                {
                    "Lap": lap_num,
                    "Compound": compound,
                    "LapTime_Sec": round(lap_time_sec, 3) if lap_time_sec is not None else None,
                    "Signal": signal,
                }
            )

        return pd.DataFrame(results)