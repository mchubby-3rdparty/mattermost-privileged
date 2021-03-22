#!/usr/bin/env python3
# Someone's Mattermost scripts.
#   Copyright (c) 2016-2021 by Someone <someone@somenet.org> (aka. Jan Vales <jan@jvales.net>)
#   Copyright (c) 2020 by michi <michi@fsinf.at> (SQL-fix)
#   published under MIT-License
#
# Active channels, order by last 7 days.
#

import psycopg2
import psycopg2.extras

import config


def main(dbconn):
    cur = dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                    WITH last_day AS(
                        SELECT channelid, count(0) AS cnt FROM posts WHERE deleteat = 0 AND createat > EXTRACT(EPOCH FROM (NOW() - INTERVAL '1 day'))*1000 GROUP BY channelid
                    ),
                    last_week AS(
                        SELECT channelid, count(0) AS cnt FROM posts WHERE deleteat = 0 AND createat > EXTRACT(EPOCH FROM (NOW() - INTERVAL '1 week'))*1000 GROUP BY channelid
                    ),
                    since_cutoff AS(
                        SELECT channelid, count(0) AS cnt FROM posts WHERE deleteat = 0 AND createat > EXTRACT(EPOCH FROM TIMESTAMP '"""+config.cutoff_date+"""')*1000 GROUP BY channelid
                    )
                    SELECT cname, cnt_seven_days, cnt_one_day, cnt_cutoff_date FROM (
                        SELECT
                            t.name || '|' || c.name AS cname,
                            COALESCE((SELECT cnt FROM last_day WHERE channelid = c.id), 0) AS cnt_one_day,
                            COALESCE((SELECT cnt FROM last_week WHERE channelid = c.id), 0) AS cnt_seven_days,
                            COALESCE((SELECT cnt FROM since_cutoff WHERE channelid = c.id), 0) AS cnt_cutoff_date
                        FROM teams AS t, channels AS c WHERE c.teamid = t.id AND c.type = 'O'
                    ) AS a
                    WHERE NOT (cnt_one_day = 0 AND cnt_seven_days = 0 AND cnt_cutoff_date = 0)
                    -- ORDER BY cnt_seven_days DESC, cname
                    ORDER BY cnt_cutoff_date DESC, cname
                """)

    total_one_day = total_seven_day = total_cutoff_date = 0
    msg = "#channel_activity #mmstats by last 7 days.\n\n|team|channel|since "+config.cutoff_date+"|7 days|24 hours|\n|---|---|---:|---:|---:|\n"
    for record in cur.fetchall():

        if record["cnt_cutoff_date"] > 2 and "w-inf-tuwien|" in record["cname"]:
            total_one_day += record["cnt_one_day"]
            total_seven_day += record["cnt_seven_days"]
            total_cutoff_date += record["cnt_cutoff_date"]
            msg += "|"+record["cname"]+"|"+str(record["cnt_cutoff_date"])+"|"+str(record["cnt_seven_days"])+"|"+str(record["cnt_one_day"])+"|\n"

    return msg + "||**Totals**|**"+str(total_seven_day)+"**|**"+str(total_one_day)+"**|**"+str(total_cutoff_date)+"**|"
