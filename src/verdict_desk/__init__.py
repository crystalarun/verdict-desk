"""Verdict Desk: cited analytics answers, or an explicit refusal."""

from verdict_desk.engine import Desk
from verdict_desk.models import Citation, Verdict

__all__ = ["Desk", "Citation", "Verdict"]
__version__ = "0.1.0"
