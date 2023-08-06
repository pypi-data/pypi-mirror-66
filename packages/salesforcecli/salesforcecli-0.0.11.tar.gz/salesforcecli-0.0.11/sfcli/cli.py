from cmd import Cmd
from functools import lru_cache
from typing import List
from simple_salesforce import Salesforce
from tabulate import tabulate
import pprint
from sfcli.util import bulk_change, bulk_delete, write_results, start_session, strtime, print_error
import sys


class Cli(Cmd):

    def __init__(self):
        super(Cli, self).__init__()
        self.env = 'default'
        self.vs = 44.0
        self.threads = 4
        self.session = start_session(self.vs, self.env)
        self._set_base_url()

    def _set_base_url(self):
        self.base_url = f'https://{self.session.sf_instance}/services/data/v{self.vs}'

    def _update_env(self):
        self.session = start_session(self.vs, self.env)
        self._set_base_url()
        print('environment updated')

    def help_setthreads(self):
        print('args:\n'
              'num_threads: int\n'
              'set the number of threads to use in threaded processes like create and update')

    def do_setthreads(self, args):
        self.threads = args

    def help_getthreads(self):
        print('prints the number of threads currently set')

    def do_getthreads(self, args):
        print(self.threads)

    def help_getenv(self):
        print('show the current environment')

    def do_getenv(self, args):
        print(self.env)

    def help_getversion(self):
        print('prints the version of the API currently in use')

    def do_getversion(self):
        print(self.vs)

    def help_setenv(self):
        print('args:\n'
              'envorionment_suffix: str (e.g. prod)\n'
              'Log into a new Salesforce Environment\n'
              'based on the environment suffix you input (this suffix will be\n'
              'appended to the default environment variable names to retrieve\n'
              'the desired variables from the .env file')

    def do_setenv(self, env_suffix: str = None):
        self.env = env_suffix if env_suffix else 'default'
        self._update_env()

    def help_setversion(self):
        print('args:\n'
              'version: str (e.g. input 42.0)\n'
              'Input the version of the API being used')

    def do_setversion(self, args):
        self.vs = args
        self._update_env()

    def _query_star(self, query: str) -> str:
        split = query.split()
        if len(split) > 2 and split[1] == '*':
            object_name = split[3]
            all_fields = self._get_object_fields(object_name)
            fields = ','.join(all_fields)
            star_query = query.replace('*', fields, 1)
            return star_query
        else:
            return query

    def _query(self, query: str) -> dict:
        final_query = self._query_star(query)
        results = self.session.query_all(final_query)
        if results:
            records = results['records']
            for r in records:
                del r['attributes']
            return records

    def help_select(self):
        print('type in a SOQL query as you normally would. Results will be\n'
              'printed in the console. supports select * from!!')

    @print_error
    def do_select(self, args):
        query = f'select {args}'
        records = self._query(query)
        if records:
            print(tabulate(records, headers='keys'))

    @print_error
    def do_SELECT(self, args):
        self.do_select(args)

    def help_download(self):
        print('type in a SOQL query after the "download" keyword. Results will be saved in a .csv')

    @print_error
    def do_download(self, args: str):
        records = self._query(args)
        if records:
            write_results(f'query_{strtime()}', records)

    def _get_object_names(self) -> List[list]:
        url = f'{self.base_url}/sobjects'
        results = self.session._call_salesforce('GET', url)
        if results:
            objects = results.json()['sobjects']
            names = [[o['name']] for o in objects]
            return names
        else:
            return None

    def help_objects(self):
        print('args:\n'
              'filter: Optional[str]\n'
              'returns a list of all the objects in the org.\n'
              'Optional string parameter to filter the objects by.')

    def do_objects(self, args: str):
        names = self._get_object_names()
        names = [n for n in names if args.lower() in n[0].lower()] if args else names
        if names:
            print(tabulate(names, headers=['name']))
        else:
            print('no results')

    @lru_cache(maxsize=32)
    def _get_object_fields(self, object_name: str) -> dict:
        url = f'{self.base_url}/sobjects/{object_name}/describe/'
        results = self.session._call_salesforce('GET', url).json()['fields']
        return [r['name'] for r in results]

    def help_fields(self):
        print('args:\n'
              'filter: Optional[str]\n'
              'Input the name of the object to return the fields for e.g. order\n'
              'Optional string parameter to filter the fields by e.g. name.')

    def do_fields(self, args: str):
        arg_lst = args.split()
        object_name = arg_lst[0]
        results = self._get_object_fields(object_name)
        if len(arg_lst) > 1:
            filter = arg_lst[1]
            tab_results = [[r] for r in results if filter.lower() in r.lower()]
        else:
            tab_results =[[r] for r in results]
        print(tabulate(tab_results, headers=['field_name']))

    def help_update(self):
        print('args:\n'
              'object: str\n'
              'file_name: str\n'
              'input the name of the object to update and the name of the file including the path.\n'
              'This file should contain columns for the fields you want set on create of these records.\n'
              'One of the columns must have the id header and contain the id of the record to be updated.\n'
              'Note the columns headers in the file must match the API names of the fields in Salesforce\n'
              'Optional parameter to specify the number of threads to use (default is 4)')

    @print_error
    def do_update(self, args: str):
        bulk_change(args, 'PATCH', self.session, self.base_url, self.threads)

    def help_create(self):
        print('args:\n'
              'object: str\n'
              'file_name: str\n''input the name of the object to update and the name of the file including the path.\n'
              'This file should contain columns for the fields you want set on create of these records.\n'
              'Note the columns headers in the file must match the API names of the fields in Salesforce\n'
              'Optional parameter to specify the number of threads to use (default is 4)')

    @print_error
    def do_create(self, args: str):
        bulk_change(args, 'POST', self.session, self.base_url, self.threads)

    def help_delete(self):
        print('args:\n'
              'file_name: str\n''input the name of the object to update and the name of the file including the path.\n'
              'The file should contain one column titled id with the ids of all the records to delete.\n'
              'These records do not need to be of the same type.\n'
              'Optional parameter to specify the number of threads to use (default is 4)')

    @print_error
    def do_delete(self, args: str):
        bulk_delete(args, self.session, self.base_url, self.threads)

    def help_end(self):
        print('Exits the shell')

    def do_end(self, args: str = None):
        sys.exit()
