APPNAME=predictive
APPDIR=/home/ec2-user/predictive/didactic-engima/Scripts/$APPNAME/

LOGFILE=$APPDIR'gunicorn.log'
ERRORFILE=$APPDIR'gunicorn-error.log'

NUM_WORKERS=3

ADDRESS=127.0.0.1:8000

cd $APPDIR

source ~/predictive/didactic-engima/predictive/bin/activate
workon $APPNAME

exec gunicorn $APPNAME.wsgi:application \
-w $NUM_WORKERS --bind=$ADDRESS \
--log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE &
