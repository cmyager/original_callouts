from datetime import datetime

import discord
import pytz

VERSION = "0.0.1"
BLUE = discord.Colour(3381759)
CLEANUP_DELAY = 2

# TODO
OWNERS = (197819576220778498,)
MODS = (197819576220778498,)

# TODO
SOLAR_ICON = 365922485524234240
ARC_ICON = 366298692161896458
VOID_ICON = 366298728048492544

XBOX_ICON = 773963366519668836
PS_ICON = 773964479759253554
STEAM_ICON = 773964460918439987
STADIA_ICON = 773964680728150026

NUMBER = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

TIME_ZONES = ['ACT', 'ACDT', 'ACST', 'ADT', 'AEDT',
              'AEST', 'AKDT', 'AKST', 'AMT', 'AMST', 'AST', 'AWST',
              'BOT', 'BRT', 'BRST', 'BST', 'CDT', 'CEST', 'CET',
              'CHST', 'CLT', 'CLST', 'COT', 'CST', 'CXT', 'CWST',
              'ECT', 'EDT', 'EEST', 'EST', 'FKST', 'FKT', 'FNT', 'GFT',
              'GMT', 'GMT+1', 'GMT+2', 'GMT+3', 'GMT+4', 'GMT+5', 'GMT+6',
              'GMT+7', 'GMT+8', 'GMT+9', 'GMT+10', 'GMT+11', 'GMT+12',
              'GMT-1', 'GMT-2', 'GMT-3', 'GMT-4', 'GMT-5', 'GMT-6', 'GMT-7',
              'GMT-8', 'GMT-9', 'GMT-10', 'GMT-11', 'GMT-12',
              'GYT', 'HADT', 'HAST', 'HST', 'HKT', 'IST', 'JST', 'KUYT',
              'LHDT', 'LHST', 'MDT', 'MSD', 'MSK', 'MST', 'NDT',
              'NFT', 'NST', 'NZST', 'NZDT', 'PDT', 'PST', 'PET', 'PYT', 'PYST',
              'SAMT', 'SDT', 'SRT', 'SST',
              'UTC', 'UTC+1', 'UTC+2', 'UTC+3', 'UTC+4', 'UTC+5', 'UTC+6',
              'UTC+7', 'UTC+8', 'UTC+9', 'UTC+10', 'UTC+11', 'UTC+12',
              'UTC-1', 'UTC-2', 'UTC-3', 'UTC-4', 'UTC-5', 'UTC-6', 'UTC-7',
              'UTC-8', 'UTC-9', 'UTC-10', 'UTC-11', 'UTC-12',
              'UYST', 'UYT', 'VET', 'WDT', 'WEST', 'WET', 'WST', 'YST', 'YDT']

TIME_ZONE_CONVERT = {"PST": "US/Pacific",
                     "PDT": "US/Pacific",
                     "MST": "US/Mountain",
                     "MDT": "US/Mountain",
                     "CST": "US/Central",
                     "CDT": "US/Central",
                     "EST": "US/Eastern",
                     "EDT": "US/Eastern"}

RELEASE_DATES = [
                 ("Beyond Light", datetime(2020, 11, 10, tzinfo=pytz.timezone('US/Pacific'))),
                 ("My Birthday", datetime(2021, 7, 14, tzinfo=pytz.timezone('US/Pacific'))),
                ]

PLATFORMS = {'xbox': 1,
             'playstation': 2,
             'steam': 3,
             'stadia': 5}

PLATFORM_URLS = {1: 'https://www.bungie.net/img/theme/bungienet/icons/xboxLiveLogo.png',
                 2: 'https://www.bungie.net/img/theme/bungienet/icons/psnLogo.png',
                 3: 'https://www.bungie.net/img/theme/bungienet/icons/steamLogo.png',
                 5: 'https://www.bungie.net/img/theme/bungienet/icons/stadiaLogo.png'}


# TODO
ELEMENTS = {2: 'https://i.imgur.com/pR2hu13.png',
            3: 'https://i.imgur.com/paWpNGd.png',
            4: 'https://i.imgur.com/RHDetvb.png'}
