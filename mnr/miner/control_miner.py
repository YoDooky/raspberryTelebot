from compileall import compile_dir
from pickle import TRUE
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


def main(run=True):
    cmd = GPIO.HIGH if run else GPIO.LOW
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
    GPIO.output(12, cmd) # Turn on


if __name__ == main:
    main()