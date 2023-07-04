from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.finish import export_device


class OTExportDevice(OTBase):
    @classmethod
    def poll(cls, context):
        # always make it possible to export a scocket
        return True

    def main_func(self, context):
        export_device(context)


class OTRestart(OTBase):
    @classmethod
    def poll(cls, context):
        # always make it possible to restart
        return True

    def main_func(self, context):
        raise NotImplementedError("Subclasses must implement main_func")
