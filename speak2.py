from subprocess import call
import time

cmd_beg = 'espeak -ven-en '
cmd_end = ' --stdout | aplay'


def speak(phrase):
    activate = 'Alexa'
    call([cmd_beg+activate+cmd_end], shell=True)
    time.sleep(2)
    phrase = phrase.replace(' ','_')
    call([cmd_beg+phrase+cmd_end], shell=True)
   
if __name__ == '__main__':
   speak('Turn on office one')
   time.sleep(5)
   speak('Turn off office one')

