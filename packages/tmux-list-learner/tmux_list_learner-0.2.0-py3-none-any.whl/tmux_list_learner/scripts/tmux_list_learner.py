#!/usr/bin/env python

import click
from tmux_list_learner.tmux_list_learner import get_window_name

@click.command()
@click.argument('server_start')
@click.argument('session_name')
@click.argument('window_index', type=int)
def cli(server_start, session_name, window_index):
    window_name = get_window_name(server_start, session_name, window_index)
    print(window_name)
