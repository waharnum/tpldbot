FROM python:3-onbuild
CMD python tpldbot.py $CONSUMER_KEY $CONSUMER_SECRET $ACCESS_TOKEN $ACCESS_TOKEN_SECRET
# docker run -d --name tpldbot-running --env-file ./tpldbot_env.ini tpldbot
# create tpldbot_env.ini with required config (see tpldbot_env.ini.sample )
