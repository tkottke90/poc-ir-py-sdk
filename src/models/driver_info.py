from pydantic import BaseModel, Field
from typing import Optional, Union
from .telemetry import TelemetryHandler
from irsdk import TrkLoc


class Driver(BaseModel):
    """
    The Driver model provides details about a specific driver in the current
    iRacing session.
    """

    CarIdx: int = Field(description='Car index', default=-1)
    UserName: str = Field(description='User Display Name', default='Unknown')
    AbbrevName: Optional[str] = Field(description='Abbreviated Name', default='')
    Initials: Optional[str] = Field(description='Initials', default='')
    UserID: int = Field(description='User ID', default=0)
    TeamID: int = Field(description='Team ID', default=0)
    TeamName: str = Field(description='Team Name', default='')
    CarNumber: str = Field(description='Car Number', default='0')
    CarNumberRaw: int = Field(description='Car Number (Raw)', default=0)
    CarPath: str = Field(description='Car Path', default='')
    CarClassID: int = Field(description='Car Class ID', default=0)
    CarID: int = Field(description='Car ID', default=0)
    CarIsPaceCar: int = Field(description='Car is Pace Car', default=0)
    CarIsAI: int = Field(description='Car is AI', default=0)
    CarIsElectric: int = Field(description='Car is Electric', default=0)
    CarScreenName: str = Field(description='Car Screen Name', default='')
    CarScreenNameShort: str = Field(description='Car Screen Name (Short)', default='')
    CarCfg: int = Field(description='Car Config', default=0)
    CarCfgName: Optional[str] = Field(description='Car Config Name', default='')
    CarCfgCustomPaintExt: Optional[str] = Field(description='Car Config Custom Paint Extension', default='')
    CarClassShortName: Optional[str] = Field(description='Car Class Short Name', default='')
    CarClassRelSpeed: int = Field(description='Car Class Relative Speed', default=0)
    CarClassLicenseLevel: int = Field(description='Car Class License Level', default=0)
    CarClassMaxFuelPct: str = Field(description='Car Class Max Fuel Pct', default='')
    CarClassWeightPenalty: str = Field(description='Car Class Weight Penalty', default='')
    CarClassPowerAdjust: str = Field(description='Car Class Power Adjust', default='')
    CarClassDryTireSetLimit: str = Field(description='Car Class Dry Tire Set Limit', default='')
    CarClassColor: int = Field(description='Car Class Color', default=0)
    CarClassEstLapTime: float = Field(description='Car Class Estimated Lap Time', default=0.0)
    IRating: int = Field(description='iRating', default=0)
    LicLevel: int = Field(description='License Level', default=0)
    LicSubLevel: int = Field(description='License Sub Level', default=0)
    LicString: str = Field(description='License String', default='')
    LicColor: Union[int, str] = Field(description='License Color', default=0) # Can be int or string like '0xundefined'
    IsSpectator: int = Field(description='Is Spectator', default=0)
    CarDesignStr: str = Field(description='Car Design String', default='')
    HelmetDesignStr: str = Field(description='Helmet Design String', default='')
    SuitDesignStr: str = Field(description='Suit Design String', default='')
    BodyType: int = Field(description='Body Type', default=0)
    FaceType: int = Field(description='Face Type', default=0)
    HelmetType: int = Field(description='Helmet Type', default=0)
    CarNumberDesignStr: str = Field(description='Car Number Design String', default='')
    CarSponsor_1: int = Field(description='Car Sponsor 1', default=0)
    CarSponsor_2: int = Field(description='Car Sponsor 2', default=0)
    CurDriverIncidentCount: int = Field(description='Current Driver Incident Count', default=0)
    TeamIncidentCount: int = Field(description='Team Incident Count', default=0)

    def is_player(self, idx: int) -> bool:
        return self.CarIdx == idx
    
    def driver_location(self, ir: TelemetryHandler) -> str:
        return ir[f'CarIdxTrackSurface'][self.CarIdx]

    def driver_location_display(self, ir: TelemetryHandler) -> str:
        location = self.driver_location(ir)
        return f"{ir.decode_car_location(location)} ({location})"

    def driver_in_pit_stall(self, ir: TelemetryHandler) -> bool:
        return self.driver_location(ir) == TrkLoc.in_pit_stall

    def driver_on_pit_road(self, ir: TelemetryHandler) -> bool:
        return self.driver_location(ir) == TrkLoc.aproaching_pits

    def driver_on_track(self, ir: TelemetryHandler) -> bool:
        return self.driver_location(ir) == TrkLoc.on_track

    def driver_display(self) -> str:
        nameLine = f"{ self.UserName } #{self.CarNumber}";

        if self.TeamID != 0:
            nameLine += f" ({self.TeamName})"
        
        carLine = f"  {self.CarScreenName} ({self.CarClassShortName})"
        ratingLine = f"  {self.IRating} ({self.LicString})"
        
        return f"""
        {nameLine}
        {carLine}
        {ratingLine}
        """


class DriverInfo(Driver):
    """
    The DriverInfo model provides details about the drivers in the current
    iRacing session. The root level contains information about the player
    as well as a list of the drivers in the session
    """

    Drivers: list[Driver] = Field(default_factory=list, description='List of drivers in the session')

    @staticmethod
    def from_iracing(ir: TelemetryHandler):
        if (ir['DriverInfo'] is None):
            return DriverInfo()

        return DriverInfo(**ir['DriverInfo'])
    
    def get_driver(self, idx: int) -> Driver | None:
        return next((d for d in self.Drivers if d.CarIdx == idx), None)
    
    def driver_list(self) -> tuple[int, str]:
        return [(d.CarIdx, d.CarScreenName) for d in self.Drivers]