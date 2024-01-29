"""Form type aliases and protocols."""

import typing as t
import typing_extensions as te

from markupsafe import Markup
from wtforms import Field as WTField, Form as WTForm

FilterCallable: te.TypeAlias = t.Callable[[t.Any], t.Any]
FilterList: te.TypeAlias = t.Iterable[FilterCallable]
ReturnIterChoices: te.TypeAlias = t.Generator[
    t.Tuple[str, str, bool, t.Dict[str, t.Any]], None, None
]
ValidatorCallable: te.TypeAlias = t.Callable[[WTForm, WTField], None]
ValidatorList: te.TypeAlias = t.Sequence[ValidatorCallable]
ValidatorConstructor: te.TypeAlias = t.Callable[..., ValidatorCallable]


class WidgetProtocol(te.Protocol):
    """Protocol for a WTForms widget."""

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup: ...


WidgetConstructor: te.TypeAlias = t.Callable[..., WidgetProtocol]


class ValidatorProtocol(te.Protocol):
    """Protocol for validators."""

    field_flags: t.Dict[str, bool]

    def __call__(self, form: WTForm, field: WTField) -> None: ...
