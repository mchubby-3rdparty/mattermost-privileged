#!/usr/bin/env python3
# Someone's Mattermost scripts.
#   Copyright (c) 2016-2021 by Someone <someone@somenet.org> (aka. Jan Vales <jan@jvales.net>)
#   published under MIT-License
#
# Run stats and post results to stats-channel(s).
#

import sys
import traceback

import mattermost
import psycopg2

import config

def run_stats(module):
    try:
        return module.main(dbconn)
    except:
        return "``BOT-AUTODELETE-FAST`` Error in module: ``"+repr(module)+"``\n# :boom::boom::boom::boom::boom:\n```\n"+traceback.format_exc()+"\n```"


dbconn = psycopg2.connect(config.dbconnstring)
dbconn.set_session(autocommit=False, isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE, readonly=True)

mm = mattermost.MMApi(config.mm_api_url)
mm.login(config.mm_user, config.mm_user_pw)

# run daily stats
[mm.create_post(config.stats_daily_channel_id, "``BOT-AUTODELETE-FAST`` "+run_stats(m)) for m in config.stats_daily]

# weekly
if len(sys.argv) > 1 and sys.argv[1] == "week":
    [mm.create_post(config.stats_weekly_channel_id, "``BOT-AUTODELETE-SLOW`` "+run_stats(m)) for m in config.stats_weekly]

mm.logout()
