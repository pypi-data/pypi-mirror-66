from subprocess import call

# contains system control messages allowing program to
# shutdown and reboot itself

def reboot():
    # print("Rebooting...")
    call('sudo reboot', shell=True)

def shutdown():
    # print("Shutting down...")
    call('sudo poweroff', shell=True)