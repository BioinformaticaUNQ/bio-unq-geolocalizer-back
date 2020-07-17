import xlrd
from geopy import geocoders
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


class GeoServices:
    def get_countries_from_xls(
        self, input_file, nro_id_col=1, nro_country_col=3, nro_shet=0, headers=True
    ):
        """
        Return a list of countries
        Params:
            input_file: file's path
            nro_id_col: the id_gbank's position column in the table
            nro_country_col: the country's position column in the table
            nro_shet: document's shet number
            headers: if have headers true, else false
        """
        init = 1
        documento = xlrd.open_workbook(input_file).sheet_by_index(nro_shet)
        countries = []
        dictionary = dict()
        if not headers:
            init = 0
        for i in range(init, documento.nrows):
            dictionary[
                (documento.cell_value(i, nro_id_col)[3:-1])
            ] = documento.cell_value(i, nro_country_col)
        return dictionary

    def get_location_for_idseq(self, listseq, dicc):
        result = []
        for seqq in listseq:
            if "genbank_accession" in seqq and seqq["genbank_accession"] in dicc:
                result.append(
                    {**seqq, **(self.get_coords_from(dicc[seqq["genbank_accession"]]))}
                )
        return result

    def get_coords_from(self, name):
        """
        return a dictionary with name, lattitud and longitude.
        params, name of city or country
        """
        geolocator = Nominatim(user_agent="spanish")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(name)
        return {
            "name": name,
            "latitude": location.latitude,
            "longitude": location.longitude,
        }
