import asyncio
import datetime
import inspect
import json
import logging
import sys

import tornado.web
from qiskit import Aer, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj as Qobj

from qctic.backend import (QCticQasmSimulator, QCticStatevectorSimulator,
                           QCticUnitarySimulator)

_logger = logging.getLogger(__name__)


def _inspect_execute_params(aer_backend):
    sig_execute = inspect.signature(execute)
    sig_backend_run = inspect.signature(aer_backend.run)
    params_execute = list(sig_execute.parameters.keys())
    params_backend_run = list(sig_backend_run.parameters.keys())

    return params_execute + params_backend_run


def _get_aer_backend(backend_name):
    simulators = {
        QCticQasmSimulator.NAME: "qasm_simulator",
        QCticStatevectorSimulator.NAME: "statevector_simulator",
        QCticUnitarySimulator.NAME: "unitary_simulator"
    }

    if backend_name not in simulators:
        raise Exception("Unknown backend: {}".format(backend_name))

    return Aer.get_backend(simulators[backend_name])


class JobsHandler(tornado.web.RequestHandler):
    def initialize(self, job_store):
        self.job_store = job_store

    def get(self):
        data = json.dumps([item for item in self.job_store.values()])
        self.write(data)

    def post(self):
        job_data = json.loads(self.request.body)
        qobj = Qobj.from_dict(job_data["qobj"])
        circuits, run_config, user_qobj_header = disassemble(qobj)
        aer_backend = _get_aer_backend(user_qobj_header.get("backend_name"))

        execute_kwargs = {}
        execute_kwargs.update(run_config)
        execute_kwargs.update(job_data.get("run_params", {}))

        execute_kwargs = {
            key: val for key, val in execute_kwargs.items()
            if key in _inspect_execute_params(aer_backend)
        }

        job_data.update({
            "date_start": datetime.datetime.utcnow().isoformat()
        })

        _logger.info("Running job for circuit:\n%s", circuits[0])

        aer_job = execute(circuits[0], aer_backend, **execute_kwargs)
        aer_job_result = aer_job.result()

        _logger.info("Job finished")

        job_data.update({
            "date_end": datetime.datetime.utcnow().isoformat(),
            "status": JobStatus.DONE.name,
            "result": aer_job_result.to_dict()
        })

        self.job_store[job_data["job_id"]] = job_data


class JobHandler(tornado.web.RequestHandler):
    def initialize(self, job_store):
        self.job_store = job_store

    def get(self, job_id):
        data = json.dumps(self.job_store.get(job_id, None))
        self.write(data)


def build_app():
    job_store = {}

    return tornado.web.Application([
        (
            r"/jobs\/?",
            JobsHandler,
            dict(job_store=job_store)
        ),
        (
            r"/jobs/(?P<job_id>[^\/]+)\/?",
            JobHandler,
            dict(job_store=job_store)
        )
    ])


def run_local_server():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090
        app = build_app()
        app.listen(port)
        _logger.info("Listening on port %s", port)
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except:
        _logger.error("Error on API server", exc_info=True)
    finally:
        loop.close()
