import sys
import json
import uuid
import datetime
import logging


class Singleton:

    def __init__(self, cls):
        self._cls = cls
        # self._instance = None

    def Instance(self):

        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


class RedBanjoConfig:

    def __init__(self):
        self._logger = logging.getLogger("RedBanjoConfig")

        with open(sys.argv[1]) as jsonFile:
            self._config = json.load(jsonFile)

            self._logger.info("Parsed Config .................: \n%s", json.dumps(self._config, indent=4))

    def execution_id(self):
        return self._config["execution"]["id"]

    def arg0(self):
        return self._config["arguments"][0]

    def arg1(self):
        return self._config["arguments"][1]

    def arg2(self):
        return self._config["arguments"][2]

    def arg3(self):
        return self._config["arguments"][3]

    def arg4(self):
        return self._config["arguments"][4]


class RedBanjoChannel:

    def __init__(self, execution_id):
        self._logger = logging.getLogger('RedBanjoChannel')
        self._execution_id = execution_id
        self._path = sys.argv[2]
        self._pipe = open(sys.argv[2], "w")

        self._logger.info('channel path: %s', self._path)
        self._logger.info('execution id: %s', self._execution_id)

    def now(self) -> datetime.datetime:
        dtnow: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)

        return dtnow;

    def send_message(self, msg_type, msg_data):
        msg = {

            "id": str(uuid.uuid4()),
            "executionId": self._execution_id,
            "messageType": msg_type,
            "data": msg_data

        }

        self.send(msg)

    def send(self, msg):
        msg_json = json.dumps(msg)

        self._logger.info("Sending message: %s", msg_json)

        self._pipe.write(msg_json)
        self._pipe.write("\n")
        self._pipe.flush()

    def close(self):
        self._pipe.close()


@Singleton
class RedBanjo:

    def __init__(self):
        self._logger = logging.getLogger("RedBanjo")
        self._config = RedBanjoConfig()
        self._channel = RedBanjoChannel(self._config.execution_id())

    def __str__(self):
        return 'RedBanjo Client'

    def config(self) -> RedBanjoConfig:
        return self._config

    def record_metric(self, name: str, value_numeric, value_string: str):
        msg_data = {
            "name": name,
            "ts": int(self._channel.now() * 1000),
            "valueNumeric": value_numeric,
            "valueString": value_string
        }

        self._channel.send_message("recordMetric", msg_data)

    def record_assertion(self, isTrue: bool, reason: str, description: str):
        msg_data = {
            "timestamp": int(self._channel.now() * 1000),
            "isTrue": isTrue,
            "reason": reason,
            "description": description
        }

        self._channel.send_message("makeAssertion", msg_data)
