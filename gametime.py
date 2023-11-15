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
    self.s += sec

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

  def show_time(self):
    # Define time-related translations
    times_of_day = {
      (0, 5): "noc",
      (5, 9): "rano",
      (9, 11): "przed południem",
      (12, 13): "południe",
      (13, 17): "po południu",
      (17, 20): "wieczór",
      (20, 24): "noc"
    }

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
      1: "wiosna",
      2: "lato",
      3: "jesień",
      4: "zima"
    }
      

    # Retrieve time components
    hour = self.h
    day = self.d
    week_day = self.week_d
    season = self.sn
    year = self.y

    # Determine the time of day
    time_of_day = next((value for key, value in times_of_day.items() if key[0] < hour <= key[1]), None)



    # Get the day of the week, month, and construct the output
    day_of_week = days_of_week.get(week_day)
    season_name = seasons.get(season)

    print("Jest {}, {}, {} {} roku {}".format(time_of_day, day_of_week, day, season_name, year))

  
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
  