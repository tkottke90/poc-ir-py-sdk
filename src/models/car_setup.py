from pydantic import BaseModel
from typing import Optional


# Reusable models (used multiple times)
class TireData(BaseModel):
    """Reusable model for tire data (used for all 4 tire positions)"""
    StartingPressure: str
    LastHotPressure: str
    LastTempsOMI: Optional[str] = None  # For rear tires
    LastTempsIMO: Optional[str] = None  # For front tires
    TreadRemaining: str


class CornerSetup(BaseModel):
    """Reusable model for corner setup (used for all 4 corners)"""
    CornerWeight: str
    RideHeight: str
    BumpRubberGap: str
    SpringRate: str
    Camber: str
    ToeIn: Optional[str] = None  # Only for rear corners


class DamperSettings(BaseModel):
    """Reusable model for damper settings (used for front and rear)"""
    LowSpeedCompressionDamping: str
    HighSpeedCompressionDamping: str
    LowSpeedReboundDamping: str
    HighSpeedReboundDamping: str


# Single-use nested models
class TireType(BaseModel):
    TireType: str


class AeroBalanceCalc(BaseModel):
    FrontRhAtSpeed: str
    RearRhAtSpeed: str
    WingSetting: str
    FrontDownforce: str


class TiresAero(BaseModel):
    TireType: TireType
    LeftFront: TireData
    LeftRear: TireData
    RightFront: TireData
    RightRear: TireData
    AeroBalanceCalc: AeroBalanceCalc


class FrontBrakes(BaseModel):
    ArbBlades: int
    TotalToeIn: str
    FrontMasterCyl: str
    RearMasterCyl: str
    BrakePads: str
    CenterFrontSplitterHeight: str


class Rear(BaseModel):
    FuelLevel: str
    ArbBlades: int
    WingAngle: str


class InCarAdjustments(BaseModel):
    BrakePressureBias: str
    AbsSetting: str
    TcSetting: str
    FWtdist: str
    CrossWeight: str


class GearsDifferential(BaseModel):
    GearStack: str
    FrictionFaces: int
    DiffPreload: str


class Chassis(BaseModel):
    FrontBrakes: FrontBrakes
    LeftFront: CornerSetup
    LeftRear: CornerSetup
    Rear: Rear
    InCarAdjustments: InCarAdjustments
    RightFront: CornerSetup
    RightRear: CornerSetup
    GearsDifferential: GearsDifferential


class Dampers(BaseModel):
    FrontDampers: DamperSettings
    RearDampers: DamperSettings


class CarSetup(BaseModel):
    UpdateCount: int
    TiresAero: TiresAero
    Chassis: Chassis
    Dampers: Dampers

