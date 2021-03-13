from kecleon import Store, FileClerk, WebClerk

from .bs_clerk import BSClerk


store = Store(
    warehouse=BSClerk(),
    deliveries=FileClerk(),
    provider=WebClerk(),
)
