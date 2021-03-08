#!/bin/env bash
cd /var/www/html/friends/apps/notify-me/notify_me;


pipenv run python src/consumers/electricity_consumer.py;
