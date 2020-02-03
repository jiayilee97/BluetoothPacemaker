class BLEDevice():
    """Represents a bluetooth peripheral"""
    DEFAULT_CONNECT_TIMEOUT = 3.0

def __init__(self, mac_address, hci_device='hci0'):
        """Initialises the device.

        Sets up threading for the notification listener and starts the
        gatttool session.

        Args:
            mac_address (str): The mac address of the BLE device to connect
                to in the format "XX:XX:XX:XX:XX:XX"
            hci_device (str): The hci device to use with gatttool

        Raises:
            pexpect.TIMEOUT: If, for some reason, pexpect fails to spawn a 
                gatttool instance (e.g. you don't have gatttool installed).
        """
        ##### Internal state #####
        self._address = mac_address
        self._handles = {}               # Used for tracking which handles
        self._subscribed_handlers = {}   # have subscribed callbacks
        self._callbacks = defaultdict(set)
        self._lock = threading.Lock()
        self._connection_lock = threading.RLock()
        self._running = True
        self._thread = None
        self._con = None                 # The gatttool instance
        self._connected = False

        ##### Set up gatttool #####
        gatttool_cmd = ' '.join(
            ['gatttool',
             '-b', self._address,
             '-i', hci_device,
             '-I']
        )

        self._con = pexpect.spawn(gatttool_cmd, ignore_sighup=False)
        self._con.expect(r'\[LE\]>', timeout=1)

        ##### Start notification listener thread #####
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        pass

    def char_write(self, handle, value, wait_for_response=False):
        """Writes a value to a given characteristic handle.

        Args:
            handle (int): The handle to write to
            value (bytearray): The value to write
            wait_for_response (bool): If true, waits for a response from
                the peripheral to check that the value was written succesfully. 

        Raises:
            NotConnectedError: If no connection to the device has been
                established.
            NoResponseError: If `wait_for_response` is True and no response
                was received from the peripheral.
        """
        pass

    def char_read_hnd(self, handle):
        """Reads a characteristic by handle.

        Args:
            handle (int): The handle of the characteristic to read.

        Returns:
            bytearray: The value of the characteristic.

        Raises:
            NotConnectedError: If no connection to the device has been 
                established.
            NotificationTimeout: If the device is connected, but reading
                fails for another reason.
        """
        pass

    def connect(self, timeout=DEFAULT_CONNECT_TIMEOUT):
        """Established a connection with the device. 

        If connection fails, try running an LE scan first. 

        Args:
            timeout (numeric): Time in seconds to wait before giving up on
                trying to connect.

        Raises:
            NotConnectedError: If connection to the device fails.
        """
        try:
            self._con.sendline('connect')
            self._con.expect(r'Connection successful.*\[LE\]>', timeout)
            self._connected = True
            if not self._running:
                self._thread.run()
        except pexpect.TIMEOUT:
            self.stop()
            message = ('timed out after connecting to %s after %f seconds.'
                       % (self._address, timeout))
            raise NotConnectedError(message)

    def run(self):
        """Listens for notifications."""
        while self._running:
            with self._connection_lock:
                try:
                    self._expect('nonsense value foobar', timeout=0.1)
                except NotificationTimeout:
                    pass
                except (NotConnectedError, pexpect.EOF):
                    break

            time.sleep(0.05)  # Stop thread from hogging _connection_lock
        pass

        def stop(self):
        """Stops the gatttool instance and listener thread."""
        self._running = False  # stop the listener thread
        if self._con.isalive():
            self._con.sendline('exit')

            # wait one second for gatttool to stop
            for i in range(100):
                if not self._con.isalive(): break
                time.sleep(0.01)

            self._con.close()  # make sure gatttool is dead
            self._connected = False

    def subscribe(self, handle, callback=None, type_=0):
        """Subscribes to notification/indiciatons from a characteristic.

        This is achieved by writing to the control handle, which is assumed
        to be `handle`+1. If indications are requested and we are already
        subscribed to notifications (or vice versa), we write 0300 
        (signifying we want to enable both). Otherwise, we write 0100 for
        notifications or 0200 for indications.

        Args:
            handle (int): The handle to listen for.
            callback (f(int, bytearray)): A function that will be called
                when the notif/indication is received. When called, it will be
                passed the handle and value.
            type_ (int): If 0, requests notifications. If 1, requests 
                indications. If 2, requests both. Any other value will
                result in a ValueError being raised. 

        Raises:
            NotificationTimeout: If writing to the control handle fails.
            ValueError: If `type_` is not in {0, 1, 2}.
        """
        pass

    def unsubscribe(self, handle, callback=None):
        """Unsubscribes from notif/indications on a handle.

        Writes 0000 to the control handle, which is assumed to be `handle`+1.
        If `callback` is supplied, removes `callback` from the list of
        callbacks for this handle.

        Args:
            handle (int): The handle to unsubscribe from.
            callback (f(int, bytearray)): The callback to remove,
                previously passed as the `callback` parameter of
                self.subscribe(handle, callback).

        Raises:
            NotificationTimeout: If writing to the control handle fails.
        """
        pass
