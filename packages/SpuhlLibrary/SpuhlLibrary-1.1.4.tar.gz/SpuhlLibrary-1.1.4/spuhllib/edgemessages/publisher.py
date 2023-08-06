import json
import logging
import uuid
import threading
from datetime import datetime

# pylint: disable=E0611
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message      


class Publisher:
    """
    The publisher can dump dictionaries to a json-string and send this string as a message to the specified
    target module
    """

    def __init__(self, module_name, output_name):
        """
        Create a new publisher to send values to the iot hub
        :param module_name: Name of the module as str
        :param output_name: The name of the output queue as str
        """
        self.module_name = module_name
        self.output_name = output_name
        self.module_client = IoTHubModuleClient.create_from_edge_environment()
        self.last_sent_values = dict()
        self.datetime_last_message = None
        self.input_listeners = []
        logging.log(logging.DEBUG, "Setup publisher for module %s" % module_name)

    def _create_message(self, module_name, values) -> Message:
        """
        Creates the message with the values to forward to the output.
        :param module_name: Name of the module
        :param values: The values as dict which have to be forwarded
        """
        values["moduleName"] = module_name
        values["time"] = str(datetime.now())
        message = Message(bytearray(json.dumps(values), 'utf-8'))
        message.message_id = str(uuid.uuid4())
        return message

    def send_message(self, values):
        """
        Forwards the message to the outuput.
        :param values: The values as dict which have to be forwarded
        """
        logging.log(logging.DEBUG, "Sending values: " + json.dumps(values))
        message = self._create_message(self.module_name, values)
        self.module_client.send_message_to_output(message, self.output_name)
        self.last_sent_values = values
        self.datetime_last_message = datetime.now()

    def register_input_listener(self, callback_func, input_tag):
        """
        Registers a callback function which must be called when a message with the specified input_tag parameter arrives.
        :param input_tag: The input for which must be listened to
        :param callback: The callback function which must be called
        """
        listen_thread = InputListener(self.module_client, callback_func, input_tag, self.module_name)
        listen_thread.daemon = True
        listen_thread.start()
        self.input_listeners.append(listen_thread)
        logging.log(logging.DEBUG, "Module %s registered a callback function for input %s" % (self.module_name, input_tag))


class InputListener(threading.Thread):
    """
    The input listener executes the callback function when a message with the specified input_tag arrives.
    """

    def __init__(self, module_client, callback_func, input_tag, module_name):
        """
         Create a new input listener.
        :param module_client: The client that connects to the Azure IoT Hub
        :param callback_func: The callback function which must be called
        :param input_tag: The input for which must be listened to
        """
        threading.Thread.__init__(self)
        self.module_client = module_client
        self.callback_func = callback_func
        self.input_tag = input_tag
        self.module_name = module_name

    def run(self):
        """
        Executes the callback function when a message with the specified input_tag arrives.
        """
        while True:
            try:
                input_message = self.module_client.receive_message_on_input(self.input_tag) # blocking call
                logging.log(logging.DEBUG, "Input message receiveved at module: %s input: %s" % (self.module_name, self.input_tag))
                message = input_message.data
                message_text = message.decode('utf-8')
                self.callback_func(json.loads(message_text))
            except Exception as ex:
                logging.log(logging.ERROR, "Unexpected error in input listener: %s" % ex )