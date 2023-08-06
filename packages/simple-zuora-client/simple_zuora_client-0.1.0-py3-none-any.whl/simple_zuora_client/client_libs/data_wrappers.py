from io import TextIOWrapper, BytesIO
from json import dumps
from csv import reader as read_csv_file
from json.decoder import JSONDecodeError


class ZuoraExportQueryResult:

    def __init__(self, raw_data, key_formatter=None):
        self.raw_data = raw_data
        try:
            assert callable(key_formatter)
            self.key_formatter = key_formatter
        except AssertionError:
            self.key_formatter = None

    @staticmethod
    def __format_key_name(key):
        formatted_key = (
            key.replace(":", "")
                .replace(" ", "")
                .replace("#", "")
                .replace("/", "")
                .replace("_", "")
                .replace("-", "")
                .replace('AccountAccount', 'account')
                .replace('SubscriptionSubscription', 'subscription')
                .replace('RevenueScheduleRevenueSchedule', 'RevenueSchedule')
        )

        # TODO: add more formatting cases
        if len(formatted_key) > 1:
            out_key = formatted_key[0].lower() + formatted_key[1:]
            return out_key

        elif len(formatted_key) == 1:
            return formatted_key.lower()

    def __str__(self):
        return str(self.raw_data)

    @property
    def dicts(self):
        out_array = []
        keys = None
        for row in self.csv_decoded:
            if keys is None:
                formatter_func = self.key_formatter if self.key_formatter is not None else self.__format_key_name
                keys = [formatter_func(key).strip() for key in row]

            else:
                udr = dict(zip(keys, row))
                out_array.append(udr)
        return out_array

    @property
    def json_formatted(self):
        return dumps(self.dicts)

    @property
    def csv_decoded(self):
        with TextIOWrapper(BytesIO(bytes(self.raw_data)), encoding='utf-8', newline='\r\n') as csv_file:
            return read_csv_file(csv_file, delimiter=',', quotechar='"')


class ZuoraResponse:
    def __init__(self, response):
        """

        :type response: requests.Response
        """
        self.raw_data = response.content
        try:
            self.as_dict = response.json()
            self.is_json_response = True
        except JSONDecodeError:
            self.is_json_response = False
