#!/bin/env bash

cd /var/www/html/friends/apps/notify-me/notify_me;

/root/.local/share/virtualenvs/notify_me-xWl7iJdx/bin/python src/producers/electricity_producer.py;
