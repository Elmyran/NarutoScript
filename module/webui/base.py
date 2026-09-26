import contextlib
import threading
from functools import wraps
from typing import Any, Dict

from pywebio.output import clear, put_html, put_text, set_scope, use_scope
from pywebio.session import defer_call, info, run_js

from module.webui.utils import Icon, WebIOTaskHandler, set_localstorage
from module.webui.widgets import type_to_html


def ensure_scope(name: str, container_scope: str = None) -> str:
    """Create-or-reuse a named scope without duplicating DOM ids."""
    set_scope(name, container_scope=container_scope, if_exist="clear")
    return name


def locked_page(fn):
    """Serialize page switches. Must wrap outside @use_scope so the whole render is exclusive."""

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        with self.enter_nav():
            return fn(self, *args, **kwargs)

    return wrapper


class Base:
    def __init__(self) -> None:
        self.alive = True
        # Whether window is visible
        self.visible = True
        # Device type
        self.is_mobile = info.user_agent.is_mobile
        # Task handler
        self.task_handler = WebIOTaskHandler()
        # Record scopes to reduce data transfer to frontend
        # Key: scope name, value: last update time
        self.scope: Dict[str, Any] = {}
        # Serialize page switches so concurrent clicks cannot interleave put_scope
        self.nav_lock = threading.RLock()
        # Bumped on every navigation; background tasks bail out when stale
        self.nav_gen = 0
        # True after shell (header/aside/menu/content) exists; avoids full rebuild
        self.shell_ready = False
        defer_call(self.stop)

    def stop(self) -> None:
        self.alive = False
        self.task_handler.stop()

    @contextlib.contextmanager
    def enter_nav(self):
        """Exclusive section for page switching. Increments nav generation."""
        with self.nav_lock:
            self.nav_gen += 1
            gen = self.nav_gen
            yield gen

    def nav_is_current(self, gen: int) -> bool:
        return self.alive and gen == self.nav_gen

    def scope_clear(self):
        self.scope = {}

    def scope_add(self, key, value):
        self.scope[key] = value

    def scope_expired(self, key, value) -> bool:
        try:
            return self.scope[key] != value
        except KeyError:
            return True

    def scope_expired_then_add(self, key, value) -> bool:
        if self.scope_expired(key, value):
            self.scope_add(key, value)
            return True
        else:
            return False


class Frame(Base):
    def __init__(self) -> None:
        super().__init__()
        self.page = "Home"

    def init_aside(self, expand_menu: bool = True, name: str = None) -> None:
        """
        Call this in aside button callback function.
        Args:
            expand_menu: expand menu
            name: button name(label) to be highlight
        """
        self.visible = True
        self.scope_clear()
        self.task_handler.remove_pending_task()
        clear("menu")
        if expand_menu:
            self.expand_menu()
        if name:
            self.active_button("aside", name)
            set_localstorage("aside", name)

    def init_menu(self, collapse_menu: bool = True, name: str = None) -> None:
        """
        Call this in menu button callback function.
        Args:
            collapse_menu: collapse menu
            name: button name(label) to be highlight
        """
        self.visible = True
        self.page = name
        self.scope_clear()
        self.task_handler.remove_pending_task()
        clear("content")
        if collapse_menu:
            self.collapse_menu()
        if name:
            self.active_button("menu", name)

    def ensure_shell(self) -> None:
        """Build header/aside/menu/content once; later switches only replace regions."""
        if self.shell_ready:
            return
        self._show()
        self.shell_ready = True

    @staticmethod
    @use_scope("ROOT", clear=True)
    def _show() -> None:
        ensure_scope("header")
        with use_scope("header"):
            put_html(Icon.ALAS).style("--header-icon--")
            put_text("NS").style("--header-text--")
            ensure_scope("header_status")
            ensure_scope("header_title")
        ensure_scope("contents")
        with use_scope("contents"):
            ensure_scope("aside")
            ensure_scope("menu")
            ensure_scope("content")

    @staticmethod
    @use_scope("header_title", clear=True)
    def set_title(text=""):
        put_text(text)

    @staticmethod
    def collapse_menu() -> None:
        run_js(
            f"""
            $("#pywebio-scope-menu").addClass("container-menu-collapsed");
            $(".container-content-collapsed").removeClass("container-content-collapsed");
        """
        )

    @staticmethod
    def expand_menu() -> None:
        run_js(
            f"""
            $(".container-menu-collapsed").removeClass("container-menu-collapsed");
            $("#pywebio-scope-content").addClass("container-content-collapsed");
        """
        )

    @staticmethod
    def active_button(position, value) -> None:
        run_js(
            f"""
            $("button.btn-{position}").removeClass("btn-{position}-active");
            $("div[style*='--{position}-{value}--']>button").addClass("btn-{position}-active");
        """
        )

    @staticmethod
    def pin_set_invalid_mark(keys) -> None:
        if isinstance(keys, str):
            keys = [keys]
        keys = ["_".join(key.split(".")) for key in keys]
        js = "".join(
            [
                f"""$(".form-control[name='{key}']").addClass('is-invalid');"""
                for key in keys
            ]
        )
        if js:
            run_js(js)
        # for key in keys:
        #     pin_update(key, valid_status=False)

    @staticmethod
    def pin_remove_invalid_mark(keys) -> None:
        if isinstance(keys, str):
            keys = [keys]
        keys = ["_".join(key.split(".")) for key in keys]
        js = "".join(
            [
                f"""$(".form-control[name='{key}']").removeClass('is-invalid');"""
                for key in keys
            ]
        )
        if js:
            run_js(js)
        # for key in keys:
        # pin_update(key, valid_status=0)

    @staticmethod
    def pin_set_hidden_arg(key, type_) -> None:
        """
        Hide arg

        Args:
            key: Path
            type_: Type in _widget_type_to_func
        """
        type_ = type_to_html(type_)
        key = "_".join(key.split("."))
        key = f"pywebio-scope-arg_container-{type_}-{key}"
        # This aims to be a typo, don't correct it, leave it as it is
        if type_ == 'textarea':
            key = key.replace('container', 'contianer')
        js = f"""$("#{key}").css("display","none");"""
        if js:
            run_js(js)

    @staticmethod
    def pin_remove_hidden_arg(key, type_) -> None:
        type_ = type_to_html(type_)
        key = "_".join(key.split("."))
        key = f"pywebio-scope-arg_container-{type_}-{key}"
        if type_ == 'textarea':
            key = key.replace('container', 'contianer')
        js = f"""$("#{key}").removeAttr('style');"""
        if js:
            run_js(js)
