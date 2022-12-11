import enum
from typing import Mapping, MutableMapping

KRAKEN_ENVIRONMENT_TYPE_VARIABLE = "_KRAKEN_COMMONS_ENVIRONMENT_TYPE"


class KrakenEnvironmentType(enum.Enum):
    """
    This enumeration describes the type of environment that is being used to run Kraken in.
    """

    #: This enum reflects that Kraken was run directly, without being invoked through Kraken wrapper.
    NATIVE = 0

    #: Wrapper, using a virtual environment.
    VENV = 1

    #: Wrapper, using a PEX file.
    PEX_ZIPAPP = 2

    #: Wrapper, using a packed PEX environment.
    PEX_PACKED = 3

    #: Wrapper, using a loose PEX environment.
    PEX_LOOSE = 4

    def is_native(self) -> bool:
        return self == KrakenEnvironmentType.NATIVE

    def is_pex(self) -> bool:
        return self in (
            KrakenEnvironmentType.PEX_ZIPAPP,
            KrakenEnvironmentType.PEX_PACKED,
            KrakenEnvironmentType.PEX_LOOSE,
        )

    def is_venv(self) -> bool:
        return self == KrakenEnvironmentType.VENV

    def is_wrapped(self) -> bool:
        return self != KrakenEnvironmentType.NATIVE

    @staticmethod
    def get(environ: Mapping[str, str]) -> "KrakenEnvironmentType":
        value = environ.get(KRAKEN_ENVIRONMENT_TYPE_VARIABLE, KrakenEnvironmentType.NATIVE.name)
        try:
            return KrakenEnvironmentType(value)
        except ValueError:
            raise RuntimeError(
                f"The value of environment variable {KRAKEN_ENVIRONMENT_TYPE_VARIABLE}={value!r} is invalid, "
                f"valid values are {', '.join(x.name for x in KrakenEnvironmentType)}. The most likely cause of this "
                "error is that the version of kraken-wrapper and kraken-build are incompatible."
            )

    def set(self, environ: MutableMapping[str, str]) -> None:
        environ[KRAKEN_ENVIRONMENT_TYPE_VARIABLE] = self.name
