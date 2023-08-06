from pyicloud import PyiCloudService

class ICloudCalendar:

    def __init__(self, username, password):
        self.connected = False
        self.verification_code_required = False
        self.api = PyiCloudService(username, password)

        if self.api.requires_2sa:
            self.verification_code_required = True
        else:
            self.connected = True

    def get_devices(self):
        return self.api.devices

    def send_code(self, device):
        if not self.connected:
            if not self.api.send_verification_code(device):
                raise Exception('Could not send verification code')
        else:
            raise Exception("Already connected")

    def validate_code(self, device, code):
        if not self.connected:
            if not self.api.validate_verification_code(device, code):
                raise Exception("Invalid verification code")
            else:
                self.verification_code_required = False
                self.connected = True
        else:
            raise Exception("Already connected")

    def get_events(self, start, end):
        if self.connected:
            return self.api.calendar.events(from_dt=start, to_dt=end)
        else:
            if self.verification_code_required:
                raise Exception("Not connected : Verification code is missing")
            else:
                raise Exception("Not connected")
