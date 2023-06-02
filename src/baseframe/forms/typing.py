"""Form type aliases and protocols."""

import typing as t

from markupsafe import Markup
from wtforms import Field as WTField
from wtforms import Form as WTForm
import typing_extensions as te

FilterCallable: te.TypeAlias = t.Callable[[t.Any], t.Any]
FilterList: te.TypeAlias = t.Iterable[FilterCallable]
ReturnIterChoices: te.TypeAlias = t.Generator[t.Tuple[str, str, bool], None, None]
ValidatorCallable: te.TypeAlias = t.Callable[[WTForm, WTField], None]
ValidatorList: te.TypeAlias = t.Sequence[ValidatorCallable]
ValidatorConstructor: te.TypeAlias = t.Callable[..., ValidatorCallable]


class WidgetProtocol(te.Protocol):
    """Protocol for a WTForms widget."""

    def __call__(self, field: WTField, **kwargs: t.Any) -> Markup:
        ...


WidgetConstructor: te.TypeAlias = t.Callable[..., WidgetProtocol]


class ValidatorProtocol(te.Protocol):
    """Protocol for validators."""

    field_flags: t.Dict[str, bool]

    def __call__(self, form: WTForm, field: WTField) -> None:
        ...
