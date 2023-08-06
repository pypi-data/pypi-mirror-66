#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import fire


class CommandLine(object):
    """
    usage: smn [options] <command> <subcommand> [<subcommand> ...] [parameters]
    \n
    smn -h/--help
    smn <command> -h/--help
    smn <command> <subcommand> -h/--help
    """

    def init(self):
        """
        Help for init
        :return:
        """
        current_dir = os.path.abspath('/')
        config_path = current_dir + "/config.yaml"
        open(config_path, 'w')
        # os.makedirs('%s/content' % current_dir)
        # os.makedirs('%s/theme' % current_dir)

        data = {'source_path': current_dir}

        with open(config_path, 'w') as f:
            yaml.dump(data, f)

    def config(self, local):
        pass

    def new(self, t=None, title=None, c=None, category=None):
        """
        Help for new
        category name
        for new markdown files
        """

        current_dir = os.path.abspath('/')

        print(t)
        print(title)
        print(c)
        print(category)


def main():
    fire.Fire(CommandLine)


if __name__ == '__main__':
    main()
