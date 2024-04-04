"""Form type aliases and protocols."""

from collections.abc import Generator, Iterable, Sequence
from typing import Any, Callable
from typing_extensions import Protocol, TypeAlias

from markupsafe import Markup
from wtforms import Field as WTField, Form as WTForm

FilterCallable: TypeAlias = Callable[[Any], Any]
FilterList: TypeAlias = Iterable[FilterCallable]
ReturnIterChoices: TypeAlias = Generator[
    tuple[str, str, bool, dict[str, Any]], None, None
]
ValidatorCallable: TypeAlias = Callable[[WTForm, WTField], None]
ValidatorList: TypeAlias = Sequence[ValidatorCallable]
ValidatorConstructor: TypeAlias = Callable[..., ValidatorCallable]


class WidgetProtocol(Protocol):
    """Protocol for a WTForms widget."""

    def __call__(self, field: WTField, **kwargs: Any) -> Markup: ...


WidgetConstructor: TypeAlias = Callable[..., WidgetProtocol]


class ValidatorProtocol(Protocol):
    """Protocol for validators."""

    field_flags: dict[str, bool]

    def __call__(self, form: WTForm, field: WTField) -> None: ...
