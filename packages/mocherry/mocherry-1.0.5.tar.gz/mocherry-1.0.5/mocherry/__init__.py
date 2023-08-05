#!/usr/bin/env python
import sys
import os
import glob
import importlib

def bootstrap_application():
    from mocherry.settings import CONFIG
    if sys.argv[1] == 'runserver':
        from mocherry.library.wsgi import runserver
        runserver()

    else:
        module_args = sys.argv
        cli_module = str(sys.argv[1])
        module_list = glob.glob(os.path.join(CONFIG['basepath'], '*', 'commands', cli_module, '__init__.py'))
        if len(module_list) > 0:
            module_filepath = os.path.normpath(module_list[0]).split(os.sep)
            source_application = module_filepath[len(module_filepath)-4]
            module_path = '{}.commands.{}'.format(source_application, cli_module)
            module_obj = importlib.import_module(module_path)
            obj = module_obj.Command()
            del module_args[0]
            del module_args[0]
            obj.handle(*module_args)
        else:
            print('No such mocherry CLI command found: \'{}\''.format(cli_module))
    exit()
