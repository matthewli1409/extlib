class SettingsCol(ConnectMongoDB):
    def __init__(self, db, client, strat):
        super().__init__(db, client)
        self.mongo_client = super().get_mongo_client()
        self.strat = strat

    def get_strat_info_db(self, strat):
        """Get strat information

        Arguments:
            strat {str} -- strategy name "MA_BO_I"

        Keyword Arguments:
            mongo_client {client} -- use user provided mongo client else function will call itself (default: {None})

        Returns:
            list -- list of strat information
        """
        return list(self.mongo_client['settings'].find({'strategy': strat}))[0]

    def get_last_run(self):
        """Get last time the strategy was ran

        Returns:
            datetime.datetime -- datetime of the last time the strat was ran
        """
        strat_info = self.get_strat_info_db(self.strat)
        return strat_info.get('lastRun')

    def set_last_run(self, dt):
        """Get last time the strategy was ran

        Arguments:
            dt {datetime.datetime} -- datetime to set
        """
        query = {'strategy': self.strat}
        newvalues = {'$set': {'lastRun': dt}}
        self.mongo_client['settings'].update_one(query, newvalues)
