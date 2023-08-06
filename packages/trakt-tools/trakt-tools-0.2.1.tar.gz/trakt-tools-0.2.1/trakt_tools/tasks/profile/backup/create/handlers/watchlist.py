from __future__ import print_function

import logging

log = logging.getLogger(__name__)


class WatchlistHandler(object):
    def run(self, backup, profile):
        print('Watchlist')

        # Request ratings
        response = profile.get('/sync/watchlist')

        if response.status_code != 200:
            print('Invalid response returned')
            return False

        # Retrieve items
        items = response.json()

        print(' - Received %d item(s)' % len(items))

        # Write watchlist to disk
        print(' - Writing to "watchlist.json"...')

        try:
            return backup.write('watchlist.json', items)
        except Exception as ex:
            log.error('Unable to write watchlist to disk: %s', ex, exc_info=True)

        return False
