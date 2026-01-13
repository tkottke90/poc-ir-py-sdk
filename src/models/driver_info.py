from pydantic import BaseModel
from typing import Optional, Union


class Driver(BaseModel):
    """
    The Driver model provides details about a specific driver in the current
    iRacing session.
    """

    CarIdx: int
    UserName: str
    AbbrevName: Optional[str]
    Initials: Optional[str]
    UserID: int
    TeamID: int
    TeamName: str
    CarNumber: str
    CarNumberRaw: int
    CarPath: str
    CarClassID: int
    CarID: int
    CarIsPaceCar: int
    CarIsAI: int
    CarIsElectric: int
    CarScreenName: str
    CarScreenNameShort: str
    CarCfg: int
    CarCfgName: Optional[str]
    CarCfgCustomPaintExt: Optional[str]
    CarClassShortName: Optional[str]
    CarClassRelSpeed: int
    CarClassLicenseLevel: int
    CarClassMaxFuelPct: str
    CarClassWeightPenalty: str
    CarClassPowerAdjust: str
    CarClassDryTireSetLimit: str
    CarClassColor: int
    CarClassEstLapTime: float
    IRating: int
    LicLevel: int
    LicSubLevel: int
    LicString: str
    LicColor: Union[int, str]  # Can be int or string like '0xundefined'
    IsSpectator: int
    CarDesignStr: str
    HelmetDesignStr: str
    SuitDesignStr: str
    BodyType: int
    FaceType: int
    HelmetType: int
    CarNumberDesignStr: str
    CarSponsor_1: int
    CarSponsor_2: int
    CurDriverIncidentCount: int
    TeamIncidentCount: int


class DriverInfo(Driver):
    """
    The DriverInfo model provides details about the drivers in the current
    iRacing session. The root level contains information about the player
    as well as a list of the drivers in the session
    """

    Drivers: list[Driver]

