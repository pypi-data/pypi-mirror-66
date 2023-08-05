"""Class that manage profile retrieving process."""

from .profile import Profile
from .api_utils import exec_api_call


# 12 decembre 2012
BASE_DATE_START = "1356059704"


class ProfileRetriever(object):
    """Profile retriever manage profile getting process."""

    def __init__(self, client, source_ids):
        """Init."""
        self.n_sources = len(source_ids)
        self.source_ids = source_ids
        self.client = client

    def _get_profiles_base(self, source_ids, page):
        """Get profiles from a given page (see /profiles)."""
        date_start = BASE_DATE_START
        resp, err = exec_api_call(lambda: self.client.profile.searching.get(source_ids=source_ids, limit=1000, date_start=date_start, page=page, sort_by="date_reception"))
        if err is not None:
            err = "Cannot get profiles from api: {} (source: {} - page: {})".format(err, source_ids, page)
            raise BaseException(err)
        profiles = []
        # put profile's data in a profile_entity object
        for r_profile in resp['data']['profiles']:
            p = Profile(r_profile['profile_id'], r_profile['source_id'])
            profiles.append(p)
        return profiles

    def _get_profiles(self, source_ids):
        """Manage get profile datas process."""
        date_start = BASE_DATE_START
        # do the operation once at start to know the number of profiles
        # associated with the sources
        resp, err = exec_api_call(lambda: self.client.profile.searching.get(source_ids=source_ids, limit=1000, date_start=date_start, sort_by="date_reception"))
        if err is not None:
            err = "Cannot get profiles from api: {} (source: {})".format(err, source_ids)
            raise BaseException(err)

        max_page = resp['max_page']
        profiles = []
        for page_idx in range(max_page):
            page_idx += 1
            profiles += self._get_profiles_base(source_ids, page_idx)
        return profiles

    def get_next_profiles(self):
        """Get profiles for the next source."""
        if len(self.source_ids) == 0:
            return None, None
        source_id = [self.source_ids.pop()]

        return self._get_profiles(source_id), source_id
