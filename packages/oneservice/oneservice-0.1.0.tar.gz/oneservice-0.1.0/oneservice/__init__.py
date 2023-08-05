from flask import Flask, request, jsonify
from types import FunctionType


class Microservice(object):
    def __init__(
        self,
        handler: FunctionType,
        service_version: str = "",
        data_validator: FunctionType = None,
        handler_method: str = "POST",
        enable_health_endpoint: bool = True,
    ) -> None:
        self.app = Flask(__name__)

        if enable_health_endpoint:
            self._create_health_endpoint(service_version=service_version)

        self._create_handler_endpoint(
            handler=handler,
            service_version=service_version,
            data_validator=data_validator,
            handler_method=handler_method,
        )

    def _create_health_endpoint(self, service_version: str) -> None:
        @self.app.route("/health", methods=["GET"])
        def health():
            return service_version, 200

    def _create_handler_endpoint(
        self,
        handler: FunctionType,
        service_version: str = "",
        data_validator: FunctionType = None,
        handler_method: str = "POST",
    ) -> None:
        @self.app.route("/", methods=[handler_method])
        def call_handler():
            if request.headers["Content-Type"] != "application/json":
                return (
                    jsonify({"error": "'Content-Type' must be 'application/json'"}),
                    400,
                )

            data = request.get_json()

            if data_validator is not None:
                errors = data_validator(data)
                if len(errors) != 0:
                    return jsonify({"errors": errors}), 400

            response, response_code = handler(data)
            return jsonify(response), response_code

    def start(self, host: str = "0.0.0.0", port: str = "5000") -> None:
        """
            Start serving microservice
        """
        self.app.run(host, port)
