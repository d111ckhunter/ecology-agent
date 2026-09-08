# -*- coding: utf-8 -*-
"""
SQLAlchemy ORM models.

水环境 (01) -> app.models.water_env
水生生态 (02) -> app.models.aqua_eco
"""

from app.models.base import Base
from app.models.water_env import (  # noqa: F401
    HydroStation,
    HydroData,
    AutoSurfaceWaterStation,
    AutoSurfaceWaterData,
    ManualSurfaceWaterStation,
    ManualSurfaceWaterData,
    SedimentStation,
    SedimentData,
    AutoWaterTempStation,
    AutoWaterTempData,
    AutoGroundwaterLevelStation,
    AutoGroundwaterLevelData,
    ManualGroundwaterQualityStation,
    ManualGroundwaterQualityData,
)
from app.models.aqua_eco import (  # noqa: F401
    HabitatMonitorData,
    ReachBiodiversityData,
    ReachBioSurveyData,
    FishSpecies,
    FishCatchData,
    FishDiversityData,
    FishGrounds,
    AquaReachInfo,
    SurveyPointInfo,
)

__all__ = [
    # 01 水环境
    "HydroStation", "HydroData",
    "AutoSurfaceWaterStation", "AutoSurfaceWaterData",
    "ManualSurfaceWaterStation", "ManualSurfaceWaterData",
    "SedimentStation", "SedimentData",
    "AutoWaterTempStation", "AutoWaterTempData",
    "AutoGroundwaterLevelStation", "AutoGroundwaterLevelData",
    "ManualGroundwaterQualityStation", "ManualGroundwaterQualityData",
    # 02 水生生态
    "HabitatMonitorData", "ReachBiodiversityData", "ReachBioSurveyData",
    "FishSpecies", "FishCatchData", "FishDiversityData", "FishGrounds",
    "AquaReachInfo", "SurveyPointInfo",
    # infra
    "Base",
]
