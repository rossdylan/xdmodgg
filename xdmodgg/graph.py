from datetime import datetime, timedelta
from StringIO import StringIO
import requests
import json


def format_date(dt):
    """
    Return a datetime object as a string in the format xdmod expects it in
    :param dt: The datetime object
    :type dt: datetime.datetime
    :return The formatted string containing the date
    :rtype str
    """
    return dt.strftime("%Y-%m-%d")

DEFAULT_OPTIONS = {
    "public_user": "true",
    "realm": "Jobs",
    "group_by": "resource",
    "statistic": "",
    "start_date": format_date(datetime.utcnow() - timedelta(weeks=1)),
    "end_date": format_date(datetime.utcnow()),
    "timeframe_labal": "7+day",
    "scale": "1",
    "aggregation_unit": "Auto",
    "dataset_type": "timeseries",
    "thumbnail": "n",
    "query_group": "tg_usage",
    "display_type": "bar",
    "combine_type": "side",
    "limit": "10",
    "offset": "0",
    "log_scale": "n",
    "show_guide_lines": "y",
    "show_tend_line": "n",
    "show_error_bars": "y",
    "show_aggregate_labels": "n",
    "show_error_labels": "n",
    "show_title": "n",
    "width": "1280",
    "height": "720",
    "legend_type": "bottom_center",
    "font_size": "3",
    "format": "png",
    "inline": "n",
    "operation": "get_data",
    "controller_module": "user_interface"
}


class Graph(object):
    """
    A class defining what a graph within xdmod is.
    :param name: The name of this graph (only used within xdmodgg)
    :type name: str
    :param root_url: The base url for the xdmod instance
    :type root_url: str
    """
    def __init__(self, name, root_url, **options):
        self.name = name
        self.root_url = root_url
        self.main_url = "{0}/controllers/user_interface.php".format(self.root_url)
        self.options = DEFAULT_OPTIONS
        self.options.update(options)

    def set_options(self, **params):
        """
        Set the options for this graph. These options are used to tell xdmod
        how to export the graph.
        :param params: The options to set graph export options
        """
        self.options.update(params)

    def download(self):
        """
        Return a StringIO instance with the downloaded graph image
        :return A StringIO buffer with the image
        :rtype StringIO
        """
        resp = requests.post(self.main_url, data=self.options)
        resp.raise_for_status()
        return StringIO(resp.content)

    def download_to_file(self, fname=None):
        """
        Download the graph directly to a file
        :param fname: The name of the file to save the graph as
        :type fname: str
        """
        resp = requests.post(self.main_url, data=self.options, stream=True)
        resp.raise_for_status()
        true_fname = fname or "{0}.{1}".format(self.name, self.options['format'])
        with open(true_fname, 'wb') as fd:
            for chunk in resp.iter_content(1024):
                fd.write(chunk)

    def to_json(self):
        """
        Export this graph definition to json
        :return a json encoded string with the options of this graph
        :rtype str
        """
        graph_dict = {
            "meta": {
                "name": self.name,
                "root_url": self.root_url,
            },
            "options": self.options,
        }
        return json.dumps(graph_dict)

    @classmethod
    def from_json(cls, json_str):
        """
        A Class method which creates a new Graph object based on a json string
        :param json_str: The json defining a Graph
        :type json_str: str
        :return A new Graph object based on the provided json
        :rtype Graph
        """
        graph_dict = json.loads(json_str)
        new_graph = Graph(
            graph_dict['meta']['name'],
            graph_dict['meta']['root_url'],
            **graph_dict['options'])
        return new_graph
