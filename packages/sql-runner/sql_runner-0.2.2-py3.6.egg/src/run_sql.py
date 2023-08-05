from dialog import Dialog
import argparse
import json
import glob
import os
from subprocess import Popen

def main():
    parser = argparse.ArgumentParser(description='Interactive SQL runner.')

    parser.add_argument(
        'config',
        type=str,
        help='Path to the config file'
    )

    args = parser.parse_args()

    with open(args.config) as fp:
        config = json.load(fp)
        sqlpath = config['sql_path']
        del config

    d = Dialog(dialog="dialog")

    d.set_background_title("SQL Runner")

    code, action = d.menu("What do you want to do?",
                          choices=[('execute', 'Execute statements based on the provided list of CSV command files'),
                                   ('test', 'Test execution of statements based on the provided list of CSV command files'),
                                   ('staging', 'Executes commands as specified, but in staging schema'),
                                   ('deps', 'View dependencies graph'),
                                   ('clean', 'Schemata prefix to clean up')
                          ],
                          title="What do you want to do?",
                          backtitle="What do you want to do?")
    
    if code != d.OK:
        proc = Popen(["clear"])
        return

    files = list((os.path.basename(f).split('.')[0], "", False) for f in glob.glob(sqlpath + "/*.csv"))

    code, files = d.checklist("What files to run?",
                              choices=files,
                              title="Which files to run?",
                              backtitle="Which files to run?")
    if code != d.OK:
        proc = Popen(["clear"])
        return

    proc = Popen(["runner", '--config', args.config, '--' + action] + files)
    proc.wait()


if __name__ == '__main__':
    main()