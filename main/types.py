"""Module contains custom types to use for type checking."""
from typing import TypedDict, NotRequired


class ServiceType(TypedDict):
    """Service is class based on TypedDict representing the structure of the entry
  in the DATA JSON."""
    service_title: str
    service_description: str
    is_service_appointment: NotRequired[str]
