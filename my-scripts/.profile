

### Please note:
###
### The following two commands will print your quota and machine usage
### information for you.
###
### Please remove these two commands if they cause any trouble with your
### programs.
###
gladequota
freehosts

### My Personal Prompt
export PS1="\[\e[00;34m\]\u@\h: \[\e[00;36m\]\w\[\e[00;31m\] \$ \[\e[0m\]"

HOSTNAME=$(hostname)

case $HOSTNAME in
    yslogin*  ) source .profile_ys;;
    cheyenne* ) source .profile_cy;;
esac

