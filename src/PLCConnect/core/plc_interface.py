import logging
import pathlib
import time
from threading import Lock, Thread, Event

from PLCConnect import initialize_plc, InteractionMode
from PLCConnect.core.edge_type import EdgeDetectionStrategy
from PLCConnect.utils.common import read_toml_to_box
from PLCConnect.utils.enums import EdgeType
from pykka import ThreadingActor


class PlcObserver:
    """
    Observer class to handle different types of events from PLCIOManager.
    """

    def __init__(self, signal: int, message_class,
                 hardware_actor: ThreadingActor):
        """
        Initialize observer with a signal, corresponding message class,
        and hardware actor.

        Args:
            signal (int): Input signal from PLC.
            message_class : Class of the message to be sent.
            hardware_actor (ThreadingActor): Actor to which messages
            will be sent.
        """
        self.signal = signal
        self.message_class = message_class
        self.hardware_actor = hardware_actor

    def handle_event(self):
        """
        Handle the event by sending the message to the hardware actor.
        """
        message = self.message_class()
        if self.hardware_actor:
            print(f"Signal {self.signal} is High, Triggered Event {type(self.message_class).__name__}")
            self.hardware_actor.tell(message)


class PlcIoManager:
    """
    Class to manage input/output operations for a PLC.
    """

    def __init__(self, plc_settings: pathlib.Path,
                 edge_type: EdgeDetectionStrategy = EdgeType.RISING,
                 mode: InteractionMode = InteractionMode.RTU,
                 caller_actor=None):
        """
        Initialize PLCIOManager with a PLC connection.

        Args:
            plc_settings: Connection object for communicating with the PLC.
        """
        self._lock = Lock()
        self._is_alive = False
        self._observers = []
        self._pause = Event()
        self._plc_settings = read_toml_to_box(plc_settings)
        self._plc_connection = initialize_plc(connection_mode=mode)
        self._strategy = edge_type
        self.caller_actor = caller_actor
        self.__monitor_io_thread = None

    def start(self):
        """
        Start monitoring input/output operations.
        """
        try:
            with self._lock:
                if not self._is_alive:
                    self._is_alive = True
                    self._plc_connection.connect(settings=self._plc_settings)
                    self.__monitor_io_thread = Thread(target=self._monitor_io, name="IOManager Thread")
                    self.__monitor_io_thread.start()
        except Exception as e:
            logging.error("Please Ensure your Plc connection. PLCIOManager Stopped")

    def stop(self):
        """
        Stop monitoring input/output operations.
        """
        with self._lock:
            if self._is_alive:
                self.resume()
                self._is_alive = False
        self.__monitor_io_thread.join()
        self._plc_connection.disconnect()

    def reconfig(self, mode: InteractionMode, plc_settings: pathlib.Path,
                 edge_type: EdgeType):
        """
        Reconfigure the PLC connection.

        Args:
            mode (InteractionMode): Interaction mode for the PLC.
            plc_settings (pathlib.Path): Path to PLC settings.
            edge_type (EdgeType): Edge detection strategy.
        """
        with self._lock:
            self._plc_connection.disconnect()
            self._strategy = edge_type
            self._plc_connection = initialize_plc(connection_mode=mode)
            self._plc_settings = read_toml_to_box(plc_settings)
            self._plc_connection.connect(settings=self._plc_settings)

    def register_observer(self, message):
        """
        Register an observer to receive events from the PLCIOManager.

        Args:
            message: Message to be sent to the observer.
        """
        if self.caller_actor:
            observer = PlcObserver(message_class=message.message,
                                   signal=message.signal_index,
                                   hardware_actor=self.caller_actor)
            self._observers.append(observer)

    def _monitor_io(self):
        """
        Monitor input/output operations.
        """
        if self._plc_connection is None:
            logging.error("Connection Not Established")
            raise Exception("Connection not Established")
        else:
            previous_value = [False] * 8
            while self._is_alive:
                while self._pause.isSet():
                    pass
                with self._lock:
                    if not self._is_alive:
                        break
                    try:
                        current_value = self._plc_connection.read_bit(address=self._plc_settings.address.read.m)
                        if current_value is not None:
                            edge = self._strategy.value.detect_edges(
                                previous_states=previous_value,
                                current_states=current_value
                            )
                            if len(edge) > 0:
                                for signal in edge:
                                    for observer in self._observers:
                                        if observer.signal == signal:
                                            print("Received signal : ", signal)
                                            observer.handle_event()
                            previous_value = current_value
                    except Exception as e:
                        logging.warning("Please ensure your connection.trying..")
                time.sleep(0.1)
    
    def write_address(self, address, value):
        if self._plc_connection:
            return self._plc_connection.write_bit(self._plc_settings.address.write[address], value=value) if address in self._plc_settings.address.write else f"Unable to locate address {address}"
    
    def pause(self):
        print("Paused PLCIOManager Thread")
        self._pause.set()
    
    def resume(self):
        print("Resumed PLCIOManager Thread")
        self._pause.clear()
