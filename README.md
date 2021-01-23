# Someone's privileged Mattermost scripts.
+ Copyright (c) 2016-2021 by Someone <someone@somenet.org> (aka. Jan Vales <jan@jvales.net>)
+ published under MIT-License
+ These scripts need DB- and Filesystem-access.

Beware: These scripts run regularily and are well tested. BUT by using these scripts, MM inc. may refuse to help you, if you run into (unrelated) issues with your MM.

It all started with me starting to write my own DB+FS cleaner, after posting this: [https://mattermost.uservoice.com/forums/306457/suggestions/15357861](https://mattermost.uservoice.com/forums/306457/suggestions/15357861)
But eventually grew to include other scripts too.

consider running as cronjobs:

    00 23 * * *   (cd /srv/mattermost/mattermost-privileged; git pull --recurse-submodules=yes; git gc) &>/dev/null
    55 23 * * *   (cd /srv/mattermost/mattermost-privileged/maintenance; python3 -u db.py |tee /tmp/maintenance_db.log; python3 -u fs.py echo ""; du -sch /srv/mattermost/data/* | tail)
    59 11 * * MON (cd /srv/mattermost/mattermost-privileged/profile_badges; python3 -u main.py)
    0 0 * * 2-7   (cd /srv/mattermost/mattermost-privileged/stats; python3 -u main.py)
    0 0 * * MON   (cd /srv/mattermost/mattermost-privileged/stats; python3 -u main.py week)


## maintenance
+ permanently deletes {"deleted",orphaned,old,unused} MM-db data and unreferenced files.
+ fix db-health degrading issues MM has (had?).
+ enforce our system-policy (Can/must be enabled separately)
  + Deleting System-Spam messages and "Posts marked for deletion"
+ enforce our enhanced-system-policy (Can/must be enabled separately; Likely only makes sense for our instances)
  + Deleting inactive Channels + Users.

### **Beware: running this WILL break your instance's audit-trails. This IS intended behavior**


## profile_badges
+ Sets custom profile badges, needs DB access for post-count based badges.


## stats
+ various stats posted into channels.
