#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""自进化引擎测试"""

import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evolve.experience_store import ExperienceStore
from src.evolve.emergence_detector import EmergenceDetector


def test_experience_store():
    """测试经验存储"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ExperienceStore(data_dir=Path(tmpdir))
        store.record_trip(
            destination="东京",
            origin="北京",
            budget=15000,
            travelers=2,
            start_date="2026-05-01",
            end_date="2026-05-07",
            rating=4.8,
            feedback="非常满意",
        )
        trips = store.get_trips()
        assert len(trips) == 1
        assert trips[0]["destination"] == "东京"
        print("✅ test_experience_store passed")


def test_emergence_detector():
    """测试涌现检测"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ExperienceStore(data_dir=Path(tmpdir))
        # 写入 3 次东京（达到阈值），每次间隔 1 秒避免 trip_id 冲突
        for i in range(3):
            time.sleep(1.1)
            store.record_trip(
                destination="东京",
                origin="北京",
                budget=15000 + i * 1000,
                travelers=2,
                start_date=f"2026-05-0{i+1}",
                end_date=f"2026-05-0{i+7}",
                rating=4.8,
            )
        count = store.get_destination_count("东京")
        assert count == 3, f"Expected 3 trips to Tokyo, got {count}"
        detector = EmergenceDetector(store=store)
        signals = detector.detect_all()
        dest_signals = [s for s in signals if s["type"] == "DestinationEmergence"]
        assert len(dest_signals) >= 1
        print("✅ test_emergence_detector passed")


if __name__ == "__main__":
    test_experience_store()
    test_emergence_detector()
    print("🎉 All evolve tests passed")


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48