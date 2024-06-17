from konsola import Konsola
from helper import Helper

class GameTime:
  def __init__(self, s, m, h, d, week_d, w, sn, y):
    self.s = s
    self.m = m
    self.h = h
    self.d = d
    self.week_d = week_d
    self.w = w
    self.sn = sn
    self.y = y

    self.time_passed = 0
    self.time_of_day = None
    self.times_of_day = {
      (0, 6): "noc",
      (6, 10): "rano",
      (10, 12): "przed południem",
      (12, 14): "południe",
      (14, 18): "po południu",
      (18, 21): "wieczór",
      (21, 24): "noc"
    }
  
  def get_current_time_of_day(self):
    return next((value for key, value in self.times_of_day.items() if key[0] <= self.h < key[1]), None)
  
  def get_hour_minute(self):
    return f"{self.h:02d}:{self.m:02d}"

  def time_progress(self, sec):
    # Define constants for the new time system
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    DAYS_PER_WEEK = 21
    DAYS_PER_SEASON = 21
    WEEKS_PER_SEASON = 3
    SEASONS_PER_YEAR = 4

    # Increment seconds and handle overflow
    self.time_passed = int(sec)
    self.s += int(sec)


    # Update time based on seconds
    if self.s >= SECONDS_PER_MINUTE:
      self.m += self.s // SECONDS_PER_MINUTE
      self.s %= SECONDS_PER_MINUTE

    if self.m >= MINUTES_PER_HOUR:
      self.h += self.m // MINUTES_PER_HOUR
      self.m %= MINUTES_PER_HOUR

    if self.h >= HOURS_PER_DAY:
      self.d += self.h // HOURS_PER_DAY
      self.h %= HOURS_PER_DAY

    if self.d >= DAYS_PER_WEEK:
      self.w += self.w // DAYS_PER_WEEK
      self.d %= DAYS_PER_WEEK

    if self.d >= DAYS_PER_SEASON:
      self.sn += self.d // DAYS_PER_SEASON
      self.d %= DAYS_PER_SEASON

    if self.sn >= SEASONS_PER_YEAR:
      self.y += self.sn // SEASONS_PER_YEAR
      self.sn %= SEASONS_PER_YEAR
    
    time_of_day = self.get_current_time_of_day()
    if self.time_of_day != time_of_day:
      Konsola.print("  Jest "+ time_of_day, "green")
      self.time_of_day = time_of_day
      Helper.sleep(0.5)


  def show_time(self, exact=False):
    # Define time-related translations

    days_of_week = {
      1: "poniedziałek",
      2: "wtorek",
      3: "środa",
      4: "czwartek",
      5: "piątek",
      6: "sobota",
      7: "niedziela"
    }

    seasons = {
      1: "wiosny",
      2: "lata",
      3: "jesieni",
      4: "zimy"
    }
      

    # Retrieve time components
    hour = self.h
    day = self.d
    week_day = self.week_d
    season = self.sn
    year = self.y

    # Determine the time of day
    time_of_day = self.get_current_time_of_day()



    # Get the day of the week, month, and construct the output
    day_of_week = days_of_week.get(week_day)
    season_name = seasons.get(season)
    
    if not exact:
      print("Jest {}, {}, {} dzień {} roku {}".format(time_of_day, day_of_week, day, season_name, year))
    else:
      print("Jest {:02d}:{:02d}:{:02d}, {}, {} dzień {} roku {}".format(self.h, self.m, self.s, day_of_week, day, season_name, year))


  
  def to_dict(self):
    return {
      "s": self.s,
      "m" : self.m,
      "h": self.h,
      "d": self.d,
      "week_d": self.week_d,
      "w": self.w,
      "sn": self.sn,
      "y": self.y
    }

  @classmethod
  def from_dict(cls, data):
    return cls(data["s"], data["m"], data["h"], data["d"], data["week_d"], data["w"], data["sn"], data["y"])
  