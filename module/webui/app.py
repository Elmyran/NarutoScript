import argparse
import html
import json
import os
import queue
import re
import threading
import time
from datetime import datetime
from functools import partial
from typing import Dict, List, Optional

import yaml
from pywebio import config as webconfig
from pywebio.output import (
    Output,
    clear,
    close_popup,
    popup,
    put_button,
    put_buttons,
    put_collapse,
    put_column,
    put_error,
    put_html,
    put_link,
    put_loading,
    put_markdown,
    put_row,
    put_scope,
    put_table,
    put_text,
    put_warning,
    set_scope,
    toast,
    use_scope,
)
from pywebio.pin import pin, pin_on_change
from pywebio.session import (
    go_app,
    info,
    local,
    register_thread,
    run_js,
    set_env,
)

import module.webui.lang as lang
from module.config.config import AzurLaneConfig, Function
from module.config.deep import deep_get, deep_iter, deep_set
from module.config.utils import (
    alas_instance,
    alas_template,
    dict_to_kv,
    filepath_args,
    filepath_config,
    read_file,
)
from module.logger import logger
from module.webui.base import Frame
from module.webui.fake import (
    get_config_mod,
    load_config,
)
from module.webui.fastapi import asgi_app
from module.webui.lang import _t, t
from module.webui.patch import fix_py37_subprocess_communicate, patch_executor,patch_mimetype
from module.webui.pin import put_file_upload, put_input, put_select
from module.webui.process_manager import ProcessManager
from module.webui.remote_access import RemoteAccess
from module.webui.setting import State
from module.webui.updater import updater
from module.webui.utils import (
    Icon,
    Switch,
    TaskHandler,
    add_css,
    filepath_css,
    get_alas_config_listen_path,
    get_localstorage,
    get_window_visibility_state,
    login,
    parse_pin_value,
    raise_exception,
    readable_number,
    re_fullmatch,
    to_pin_value,
)
from module.webui.widgets import (
    BinarySwitchButton,
    RichLog,
    T_Output_Kwargs,
    put_icon_buttons,
    put_loading_text,
    put_none,
    put_output,
)

patch_executor()
patch_mimetype()
fix_py37_subprocess_communicate()
task_handler = TaskHandler()


class AlasGUI(Frame):
    ALAS_MENU: Dict[str, Dict[str, List[str]]]
    ALAS_ARGS: Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
    ALAS_STORED: Dict[str, Dict[str, Dict[str, str]]]
    theme = "default"

    def initial(self) -> None:
        self.ALAS_MENU = read_file(filepath_args("menu", self.alas_mod))
        self.ALAS_ARGS = read_file(filepath_args("args", self.alas_mod))
        self.ALAS_STORED = read_file(filepath_args("stored", self.alas_mod))
        self._init_alas_config_watcher()

    def __init__(self) -> None:
        super().__init__()
        # modified keys, return values of pin_wait_change()
        self.modified_config_queue = queue.Queue()
        # alas config name
        self.alas_name = ""
        self.alas_mod = "alas"
        self.alas_config = AzurLaneConfig("template")
        self.alas_config_hidden = set()
        self.initial()
        # rendered state cache
        self.rendered_cache = []
        self.inst_cache = []
        self.load_home = False
        self.af_flag = False

    @use_scope("aside", clear=True)
    def set_aside(self) -> None:
        # TODO: update put_icon_buttons()
        put_icon_buttons(
            Icon.DEVELOP,
            buttons=[
                {"label": t("Gui.Aside.Home"), "value": "Home", "color": "aside"}
            ],
            onclick=[self.ui_develop],
        ),
        # Create instance rows as nested scopes in one shot (no later put_scope of same ids)
        put_scope("aside_instance", [
            put_scope(f"alas-instance-{i}", [])
            for i, _ in enumerate(alas_instance())
        ], scope="aside")
        self.set_aside_status()
        put_icon_buttons(
            Icon.ADD,
            buttons=[
                {"label": t("Gui.Aside.ManageAlas"), "value": "ManageAlas", "color": "aside"}
            ],
            onclick=[self.ui_manage_alas],
        ),

        current_date = datetime.now().date()
        if current_date.month == 4 and current_date.day == 1:
            self.af_flag = True

    @use_scope("aside_instance")
    def set_aside_status(self) -> None:
        flag = True

        def update(name, seq):
            # Only fill existing scopes — never put_scope here (avoids duplicate id)
            with use_scope(f"alas-instance-{seq}", clear=True):
                icon_html = Icon.RUN
                rendered_state = ProcessManager.get_manager(name).state
                if rendered_state == 1 and self.af_flag:
                    icon_html = icon_html[:31] + " anim-rotate" + icon_html[31:]
                put_icon_buttons(
                    icon_html,
                    buttons=[{"label": name, "value": name, "color": "aside"}],
                    onclick=self.ui_alas,
                )
            return rendered_state

        if not len(self.rendered_cache) or self.load_home:
            # Reload when add/delete new instance | first start | HomePage
            flag = False
            self.inst_cache = alas_instance()
        if flag:
            for index, inst in enumerate(self.inst_cache):
                state = ProcessManager.get_manager(inst).state
                if state != self.rendered_cache[index]:
                    self.rendered_cache[index] = update(inst, index)
                    flag = False
        else:
            # Do NOT clear("aside_instance"): that removes nested scopes set_aside just created.
            # Just refill each child via use_scope.
            self.rendered_cache.clear()
            for index, inst in enumerate(self.inst_cache):
                self.rendered_cache.append(update(inst, index))
            self.load_home = False
        if not flag:
            aside_name = get_localstorage("aside")
            self.active_button("aside", aside_name)

        return

    @use_scope("header_status")
    def set_status(self, state: int) -> None:
        """
        Args:
            state (int):
                1 (running)
                2 (not running)
                3 (warning, stop unexpectedly)
                4 (stop for update)
                0 (hide)
                -1 (*state not changed)
        """
        if state == -1:
            return
        clear()

        if state == 1:
            put_loading_text(t("Gui.Status.Running"), color="success")
        elif state == 2:
            put_loading_text(t("Gui.Status.Inactive"), color="secondary", fill=True)
        elif state == 3:
            put_loading_text(t("Gui.Status.Warning"), shape="grow", color="warning")
        elif state == 4:
            put_loading_text(t("Gui.Status.Updating"), shape="grow", color="success")

    @classmethod
    def set_theme(cls, theme="default") -> None:
        cls.theme = theme
        State.deploy_config.Theme = theme
        State.theme = theme
        webconfig(theme=theme)

    @use_scope("menu", clear=True)
    def alas_set_menu(self) -> None:
        """
        Set menu
        """
        put_buttons(
            [{
                "label": t("Gui.MenuAlas.Overview"),
                "value": "Overview",
                "color": "menu",
            }],
            onclick=[self.alas_overview],
        ).style(f"--menu-Overview--")

        for menu, task_data in self.ALAS_MENU.items():
            if task_data.get("page") == "tool":
                _onclick = self.alas_daemon_overview
            else:
                _onclick = self.alas_set_group

            if task_data.get("menu") == "collapse":
                task_btn_list = [
                    put_buttons(
                        [{
                            "label": t(f"Task.{task}.name"),
                            "value": task,
                            "color": "menu",
                        }],
                        onclick=_onclick,
                    ).style(f"--menu-{task}--")
                    for task in task_data.get("tasks", [])
                ]
                put_collapse(title=t(f"Menu.{menu}.name"), content=task_btn_list)
            else:
                title = t(f"Menu.{menu}.name")
                put_html('<div class="hr-task-group-box">'
                         '<span class="hr-task-group-line"></span>'
                         f'<span class="hr-task-group-text">{title}</span>'
                         '<span class="hr-task-group-line"></span>'
                         '</div>'
                         )
                for task in task_data.get("tasks", []):
                    put_buttons(
                        [{
                            "label": t(f"Task.{task}.name"),
                            "value": task,
                            "color": "menu",
                        }],
                        onclick=_onclick,
                    ).style(f"--menu-{task}--").style(f"padding-left: 0.75rem")

        self.alas_overview()

    @use_scope("content", clear=True)
    def alas_set_group(self, task: str) -> None:
        """
        Set arg groups from dict
        """
        self.init_menu(name=task)
        self.set_title(t(f"Task.{task}.name"))

        put_scope("_groups", [put_none(), put_scope("groups"), put_scope("navigator")])

        task_help: str = t(f"Task.{task}.help")
        if task_help:
            put_scope(
                "group__info",
                scope="groups",
                content=[put_text(task_help).style("font-size: 1rem")],
            )

        config = self.alas_config.read_file(self.alas_name)
        self.alas_config_hidden = self.alas_config.get_hidden_args(config)
        for group, arg_dict in deep_iter(self.ALAS_ARGS[task], depth=1):
            if self.set_group(group, arg_dict, config, task):
                self.set_navigator(group)

    @use_scope("groups")
    def set_group(self, group, arg_dict, config, task):
        group_name = group[0]

        output_list: List[Output] = []
        for arg, arg_dict in deep_iter(arg_dict, depth=1):
            output_kwargs: T_Output_Kwargs = arg_dict.copy()

            # Skip hide
            display: Optional[str] = output_kwargs.pop("display", None)
            if display == "hide":
                continue
            # Disable
            elif display == "disabled":
                output_kwargs["disabled"] = True
            # Output type
            output_kwargs["widget_type"] = output_kwargs.pop("type")

            arg_name = arg[0]  # [arg_name,]
            # Internal pin widget name
            output_kwargs["name"] = f"{task}_{group_name}_{arg_name}"
            # Display title
            output_kwargs["title"] = t(f"{group_name}.{arg_name}.name")

            # Get value from config
            value = deep_get(
                config, [task, group_name, arg_name], output_kwargs["value"]
            )
            # idk
            value = str(value) if isinstance(value, datetime) else value
            # Default value
            output_kwargs["value"] = value
            # Options
            output_kwargs["options"] = options = output_kwargs.pop("option", [])
            # Options label
            options_label = []
            for opt in options:
                options_label.append(t(f"{group_name}.{arg_name}.{opt}"))
            output_kwargs["options_label"] = options_label
            # Help
            arg_help = t(f"{group_name}.{arg_name}.help")
            if arg_help == "" or not arg_help:
                arg_help = None
            output_kwargs["help"] = arg_help
            # Invalid feedback
            output_kwargs["invalid_feedback"] = t("Gui.Text.InvalidFeedBack", value)

            o = put_output(output_kwargs)
            if o is not None:
                # output will inherit current scope when created, override here
                o.spec["scope"] = f"#pywebio-scope-group_{group_name}"
                # Add hidden-arg
                if f"{task}.{group_name}.{arg_name}" in self.alas_config_hidden:
                    o.style("display:none")
                output_list.append(o)

        if not output_list:
            return 0

        with use_scope(f"group_{group_name}"):
            put_text(t(f"{group_name}._info.name"))
            group_help = t(f"{group_name}._info.help")
            if group_help != "":
                put_text(group_help)
            put_html('<hr class="hr-group">')
            for output in output_list:
                output.show()

        return len(output_list)

    @use_scope("navigator")
    def set_navigator(self, group):
        js = f"""
            $("#pywebio-scope-groups").scrollTop(
                $("#pywebio-scope-group_{group[0]}").position().top
                + $("#pywebio-scope-groups").scrollTop() - 59
            )
        """
        put_button(
            label=t(f"{group[0]}._info.name"),
            onclick=lambda: run_js(js),
            color="navigator",
        )

    def set_dashboard(self, arg, arg_dict, config):
        i18n = arg_dict.get('i18n')
        if i18n:
            name = t(i18n)
        else:
            name = arg
        color = arg_dict.get("color", "#777777")
        nodata = t("Gui.Dashboard.NoData")

        def set_value(dic):
            if "total" in dic.get("attrs", []) and config.get("total") is not None:
                return [
                    put_text(readable_number(config.get("value", nodata))).style("--dashboard-value--"),
                    put_text(f' / {config.get("total", "")}').style("--dashboard-time--"),
                ]
            elif "comment" in dic.get("attrs", []) and config.get("comment") is not None:
                return [
                    put_text(readable_number(config.get("value", nodata))).style("--dashboard-value--"),
                    put_text(f' {config.get("comment", "")}').style("--dashboard-time--"),
                ]
            else:
                return [
                    put_text(readable_number(config.get("value", nodata))).style("--dashboard-value--"),
                ]

        with use_scope(f"dashboard-row-{arg}", clear=True):
            put_html(f'<div><div class="dashboard-icon" style="background-color:{color}"></div>'),
            put_scope(f"dashboard-content-{arg}", [
                put_scope(f"dashboard-value-{arg}", set_value(arg_dict)),
                put_scope(f"dashboard-time-{arg}", [
                    put_text(f"{name} - {lang.readable_time(config.get('time', ''))}").style("--dashboard-time--"),
                ])
            ])

    @use_scope("content", clear=True)
    def alas_overview(self) -> None:
        self.init_menu(name="Overview")
        self.set_title(t(f"Gui.MenuAlas.Overview"))

        put_scope("overview", [put_scope("schedulers"), put_scope("logs")])

        with use_scope("schedulers"):
            put_scope(
                "scheduler-bar",
                [
                    put_text(t("Gui.Overview.Scheduler")).style(
                        "font-size: 1.25rem; margin: auto .5rem auto;"
                    ),
                    put_scope("scheduler_btn"),
                ],
            )
            put_scope(
                "running",
                [
                    put_text(t("Gui.Overview.Running")),
                    put_html('<hr class="hr-group">'),
                    put_scope("running_tasks"),
                ],
            )
            put_scope(
                "pending",
                [
                    put_text(t("Gui.Overview.Pending")),
                    put_html('<hr class="hr-group">'),
                    put_scope("pending_tasks"),
                ],
            )
            put_scope(
                "waiting",
                [
                    put_text(t("Gui.Overview.Waiting")),
                    put_html('<hr class="hr-group">'),
                    put_scope("waiting_tasks"),
                ],
            )

        switch_scheduler = BinarySwitchButton(
            label_on=t("Gui.Button.Stop"),
            label_off=t("Gui.Button.Start"),
            onclick_on=lambda: self.alas.stop(),
            onclick_off=lambda: self.alas.start(None, updater.event),
            get_state=lambda: self.alas.alive,
            color_on="off",
            color_off="on",
            scope="scheduler_btn",
        )

        log = RichLog("log")

        with use_scope("logs"):
            put_scope("log-bar", [
                put_scope("log-title", [
                    put_text(t("Gui.Overview.Log")).style("font-size: 1.25rem; margin: auto .5rem auto;"),
                    put_scope("log-title-btns", [
                        put_scope("log_scroll_btn"),
                    ]),
                ]),
                put_html('<hr class="hr-group">'),
                put_scope("dashboard", [
                    # Empty dashboard, values will be updated in alas_update_overview_task()
                    put_scope(f"dashboard-row-{arg}", [])
                    for arg in self.ALAS_STORED.keys() if deep_get(self.ALAS_STORED, keys=[arg, "order"], default=0)
                    # Empty content to left-align last row
                ] + [put_html("<i></i>")] * min(len(self.ALAS_STORED), 4))
            ])
            put_scope("log", [put_html("")])

        log.console.width = log.get_width()

        switch_log_scroll = BinarySwitchButton(
            label_on=t("Gui.Button.ScrollON"),
            label_off=t("Gui.Button.ScrollOFF"),
            onclick_on=lambda: log.set_scroll(False),
            onclick_off=lambda: log.set_scroll(True),
            get_state=lambda: log.keep_bottom,
            color_on="on",
            color_off="off",
            scope="log_scroll_btn",
        )

        self.task_handler.add(switch_scheduler.g(), 1, True)
        self.task_handler.add(switch_log_scroll.g(), 1, True)
        self.task_handler.add(self.alas_update_overview_task, 10, True)
        self.task_handler.add(log.put_log(self.alas), 0.25, True)

    def _init_alas_config_watcher(self) -> None:
        def put_queue(path, value):
            self.modified_config_queue.put({"name": path, "value": value})

        for path in get_alas_config_listen_path(self.ALAS_ARGS):
            pin_on_change(
                name="_".join(path), onchange=partial(put_queue, ".".join(path))
            )
        logger.info("Init config watcher done.")

    def _alas_thread_update_config(self) -> None:
        modified = {}
        while self.alive:
            try:
                d = self.modified_config_queue.get(timeout=10)
                config_name = self.alas_name
                config_updater = self.alas_config
            except queue.Empty:
                continue
            modified[d["name"]] = d["value"]
            while True:
                try:
                    d = self.modified_config_queue.get(timeout=1)
                    modified[d["name"]] = d["value"]
                except queue.Empty:
                    self._save_config(modified, config_name, config_updater)
                    modified.clear()
                    break

    def _save_config(
            self,
            modified: Dict[str, str],
            config_name: str,
            config_updater: AzurLaneConfig = State.config_updater,
    ) -> None:
        try:
            valid = []
            invalid = []
            config = config_updater.read_file(config_name)
            for k, v in modified.copy().items():
                valuetype = deep_get(self.ALAS_ARGS, k + ".valuetype")
                v = parse_pin_value(v, valuetype)
                validate = deep_get(self.ALAS_ARGS, k + ".validate")
                if not len(str(v)):
                    default = deep_get(self.ALAS_ARGS, k + ".value")
                    modified[k] = default
                    deep_set(config, k, default)
                    valid.append(k)
                    pin["_".join(k.split("."))] = default

                elif not validate or re_fullmatch(validate, v):
                    deep_set(config, k, v)
                    modified[k] = v
                    valid.append(k)

                    for set_key, set_value in config_updater.save_callback(k, v):
                        modified[set_key] = set_value
                        deep_set(config, set_key, set_value)
                        valid.append(set_key)
                        pin["_".join(set_key.split("."))] = to_pin_value(set_value)
                else:
                    modified.pop(k)
                    invalid.append(k)
                    logger.warning(f"Invalid value {v} for key {k}, skip saving.")
            self.pin_remove_invalid_mark(valid)
            self.pin_set_invalid_mark(invalid)
            new_hidden_args = config_updater.get_hidden_args(config)
            for k in new_hidden_args - self.alas_config_hidden:
                self.pin_set_hidden_arg(k, type_=deep_get(self.ALAS_ARGS, f"{k}.type"))
            for k in self.alas_config_hidden - new_hidden_args:
                self.pin_remove_hidden_arg(k, type_=deep_get(self.ALAS_ARGS, f"{k}.type"))
            self.alas_config_hidden = new_hidden_args

            if modified:
                toast(
                    t("Gui.Toast.ConfigSaved"),
                    duration=1,
                    position="right",
                    color="success",
                )
                logger.info(
                    f"Save config {filepath_config(config_name)}, {dict_to_kv(modified)}"
                )
                config_updater.write_file(config_name, config)
        except Exception as e:
            logger.exception(e)

    def alas_update_overview_task(self) -> None:
        """Refresh overview lists/dashboard. Must never kill the caller task."""
        if not self.visible:
            return
        if not hasattr(self, "alas") or not hasattr(self, "alas_config"):
            return

        try:
            self.alas_config.load()
            self.alas_config.get_next_task()

            alive = self.alas.alive
            if len(self.alas_config.pending_task) >= 1:
                if alive:
                    running = self.alas_config.pending_task[:1]
                    pending = self.alas_config.pending_task[1:]
                else:
                    running = []
                    pending = self.alas_config.pending_task[:]
            else:
                running = []
                pending = []
            waiting = self.alas_config.waiting_task

            def put_task_list(scope_name: str, tasks: list):
                # Snapshot content so we can skip no-op redraws
                snap = [
                    (f.command, str(f.next_run), f.enable)
                    for f in (tasks or [])
                ]
                cache_key = f"overview-tasks-{scope_name}"
                if not self.scope_expired_then_add(cache_key, snap):
                    return
                clear(scope_name)
                with use_scope(scope_name):
                    if not tasks:
                        put_text(t("Gui.Overview.NoTask")).style(
                            "--overview-notask-text--"
                        )
                        return
                    for func in tasks:
                        # Direct children of running/pending/waiting_tasks — no nested put_scope
                        put_row(
                            [
                                put_column(
                                    [
                                        put_text(t(f"Task.{func.command}.name")).style(
                                            "--arg-title--"
                                        ),
                                        put_text(str(func.next_run)).style(
                                            "--arg-help--"
                                        ),
                                    ],
                                    size="auto auto",
                                ),
                                put_button(
                                    label=t("Gui.Button.Setting"),
                                    onclick=partial(self.alas_set_group, func.command),
                                    color="off",
                                ),
                            ],
                            size="1fr auto",
                        ).style("--overview-task-card--")

            put_task_list("running_tasks", running)
            put_task_list("pending_tasks", pending)
            put_task_list("waiting_tasks", waiting)

            for arg, arg_dict in self.ALAS_STORED.items():
                if not arg_dict.get("order", 0):
                    continue
                path = arg_dict["path"]
                if self.scope_expired_then_add(f"dashboard-time-value-{arg}", [
                    deep_get(self.alas_config.data, keys=f"{path}.value"),
                    lang.readable_time(
                        deep_get(self.alas_config.data, keys=f"{path}.time")
                    ),
                ]):
                    self.set_dashboard(
                        arg,
                        arg_dict,
                        deep_get(self.alas_config.data, keys=path, default={}),
                    )
        except Exception as e:
            # Keep the periodic task alive; log and retry next tick
            logger.exception(e)

    @use_scope("content", clear=True)
    def alas_daemon_overview(self, task: str) -> None:
        self.init_menu(name=task)
        self.set_title(t(f"Task.{task}.name"))

        log = RichLog("log")

        if self.is_mobile:
            put_scope(
                "daemon-overview",
                [
                    put_scope("scheduler-bar"),
                    put_scope("groups"),
                    put_scope("daemon-log-bar"),
                    put_scope("log", [put_html("")]),
                ],
            )
        else:
            put_scope(
                "daemon-overview",
                [
                    put_none(),
                    put_scope(
                        "_daemon",
                        [
                            put_scope(
                                "_daemon_upper",
                                [put_scope("scheduler-bar"), put_scope("daemon-log-bar")],
                            ),
                            put_scope("groups"),
                            put_scope("log", [put_html("")]),
                        ],
                    ),
                    put_none(),
                ],
            )

        log.console.width = log.get_width()

        with use_scope("scheduler-bar"):
            put_text(t("Gui.Overview.Scheduler")).style(
                "font-size: 1.25rem; margin: auto .5rem auto;"
            )
            put_scope("scheduler_btn")

        switch_scheduler = BinarySwitchButton(
            label_on=t("Gui.Button.Stop"),
            label_off=t("Gui.Button.Start"),
            onclick_on=lambda: self.alas.stop(),
            onclick_off=lambda: self.alas.start(task),
            get_state=lambda: self.alas.alive,
            color_on="off",
            color_off="on",
            scope="scheduler_btn",
        )

        with use_scope("daemon-log-bar"):
            with use_scope("log-title"):
                put_text(t("Gui.Overview.Log")).style(
                    "font-size: 1.25rem; margin: auto .5rem auto;"
                )
                put_scope(
                    "log-bar-btns",
                    [
                        put_scope("log_scroll_btn"),
                    ],
                )

        switch_log_scroll = BinarySwitchButton(
            label_on=t("Gui.Button.ScrollON"),
            label_off=t("Gui.Button.ScrollOFF"),
            onclick_on=lambda: log.set_scroll(False),
            onclick_off=lambda: log.set_scroll(True),
            get_state=lambda: log.keep_bottom,
            color_on="on",
            color_off="off",
            scope="log_scroll_btn",
        )

        config = self.alas_config.read_file(self.alas_name)
        for group, arg_dict in deep_iter(self.ALAS_ARGS[task], depth=1):
            if group[0] == "Storage":
                continue
            self.set_group(group, arg_dict, config, task)

        run_js("""
            $("#pywebio-scope-log").css(
                "grid-row-start",
                -2 - $("#pywebio-scope-_daemon").children().filter(
                    function(){
                        return $(this).css("display") === "none";
                    }
                ).length
            );
            $("#pywebio-scope-log").css(
                "grid-row-end",
                -1
            );
        """)

        self.task_handler.add(switch_scheduler.g(), 1, True)
        self.task_handler.add(switch_log_scroll.g(), 1, True)
        self.task_handler.add(log.put_log(self.alas), 0.25, True)

    @use_scope("menu", clear=True)
    def dev_set_menu(self) -> None:
        self.init_menu(collapse_menu=False, name="Develop")

        put_button(
            label=t("Gui.MenuDevelop.HomePage"),
            onclick=self.show,
            color="menu",
        ).style(f"--menu-HomePage--")

        # put_button(
        #     label=t("Gui.MenuDevelop.Translate"),
        #     onclick=self.dev_translate,
        #     color="menu",
        # ).style(f"--menu-Translate--")

        put_button(
            label=t("Gui.MenuDevelop.Update"),
            onclick=self.dev_update,
            color="menu",
        ).style(f"--menu-Update--")

        put_button(
            label=t("Gui.MenuDevelop.Remote"),
            onclick=self.dev_remote,
            color="menu",
        ).style(f"--menu-Remote--")

        put_button(
            label=t("Gui.MenuDevelop.Utils"),
            onclick=self.dev_utils,
            color="menu",
        ).style(f"--menu-Utils--")

    def dev_translate(self) -> None:
        go_app("translate", new_window=True)
        lang.TRANSLATE_MODE = True
        self.show()

    @use_scope("content", clear=True)
    def dev_update(self) -> None:
        self.init_menu(name="Update")
        self.set_title(t("Gui.MenuDevelop.Update"))

        if State.restart_event is None:
            put_warning(t("Gui.Update.DisabledWarn"))

        put_row(
            content=[put_scope("updater_loading"), None, put_scope("updater_state")],
            size="auto .25rem 1fr",
        )

        put_scope("updater_btn")
        put_scope("updater_info")

        def update_table():
            with use_scope("updater_info", clear=True):
                updater.read()
                # Refresh origin/<branch> for history / git-fallback display
                updater.execute(
                    f'"{updater.git}" fetch origin {updater.Branch}',
                    allow_failure=True,
                )

                local_commit = updater.get_commit(short_sha1=True)

                # Prefer CDN tip whenever GitOverCdn has it.
                # `git fetch origin` can rewrite origin/<branch> back to gitee's
                # older tip and hide the CDN-synced commit after an update.
                cdn_sha = ""
                if State.deploy_config.GitOverCdn:
                    try:
                        cdn_sha = updater.goc_client.latest_commit or ""
                    except Exception:
                        cdn_sha = ""

                if cdn_sha:
                    upstream_rev = cdn_sha
                else:
                    upstream_rev = f"origin/{updater.Branch}"

                upstream_commit = updater.get_commit(upstream_rev, short_sha1=True)
                if not upstream_commit[0]:
                    # CDN commit not in local object DB yet — still show the sha
                    show_sha = upstream_rev[:7] if cdn_sha else upstream_rev
                    upstream_commit = (show_sha, "-", "-", "Cloudflare CDN")

                put_table(
                    [
                        [t("Gui.Update.Local"), *local_commit],
                        [t("Gui.Update.Upstream"), *upstream_commit],
                    ],
                    header=[
                        "",
                        "SHA1",
                        t("Gui.Update.Author"),
                        t("Gui.Update.Time"),
                        t("Gui.Update.Message"),
                    ],
                )
            with use_scope("updater_detail", clear=True):
                put_text(t("Gui.Update.DetailedHistory"))
                history = updater.get_commit(
                    f"origin/{updater.Branch}", n=20, short_sha1=True
                )
                if not history or not history[0]:
                    history = []
                elif not isinstance(history[0], (list, tuple)):
                    history = [history]
                put_table(
                    [commit for commit in history],
                    header=[
                        "SHA1",
                        t("Gui.Update.Author"),
                        t("Gui.Update.Time"),
                        t("Gui.Update.Message"),
                    ],
                )

        def u(state):
            if state == -1:
                return
            clear("updater_loading")
            clear("updater_state")
            clear("updater_btn")
            if state == 0:
                put_loading("border", "secondary", "updater_loading").style(
                    "--loading-border-fill--"
                )
                put_text(t("Gui.Update.UpToDate"), scope="updater_state")
                put_button(
                    t("Gui.Button.CheckUpdate"),
                    onclick=updater.check_update,
                    color="info",
                    scope="updater_btn",
                )
                update_table()
            elif state == 1:
                put_loading("grow", "success", "updater_loading").style(
                    "--loading-grow--"
                )
                put_text(t("Gui.Update.HaveUpdate"), scope="updater_state")
                put_button(
                    t("Gui.Button.ClickToUpdate"),
                    onclick=updater.run_update,
                    color="success",
                    scope="updater_btn",
                )
                update_table()
            elif state == "checking":
                put_loading("border", "primary", "updater_loading").style(
                    "--loading-border--"
                )
                put_text(t("Gui.Update.UpdateChecking"), scope="updater_state")
            elif state == "failed":
                put_loading("grow", "danger", "updater_loading").style(
                    "--loading-grow--"
                )
                put_text(t("Gui.Update.UpdateFailed"), scope="updater_state")
                put_button(
                    t("Gui.Button.RetryUpdate"),
                    onclick=updater.run_update,
                    color="primary",
                    scope="updater_btn",
                )
            elif state == "start":
                put_loading("border", "primary", "updater_loading").style(
                    "--loading-border--"
                )
                put_text(t("Gui.Update.UpdateStart"), scope="updater_state")
                put_button(
                    t("Gui.Button.CancelUpdate"),
                    onclick=updater.cancel,
                    color="danger",
                    scope="updater_btn",
                )
            elif state == "wait":
                put_loading("border", "primary", "updater_loading").style(
                    "--loading-border--"
                )
                put_text(t("Gui.Update.UpdateWait"), scope="updater_state")
                put_button(
                    t("Gui.Button.CancelUpdate"),
                    onclick=updater.cancel,
                    color="danger",
                    scope="updater_btn",
                )
            elif state == "run update":
                put_loading("border", "primary", "updater_loading").style(
                    "--loading-border--"
                )
                put_text(t("Gui.Update.UpdateRun"), scope="updater_state")
                put_button(
                    t("Gui.Button.CancelUpdate"),
                    onclick=updater.cancel,
                    color="danger",
                    scope="updater_btn",
                    disabled=True,
                )
            elif state == "reload":
                put_loading("grow", "success", "updater_loading").style(
                    "--loading-grow--"
                )
                put_text(t("Gui.Update.UpdateSuccess"), scope="updater_state")
                update_table()
            elif state == "finish":
                put_loading("grow", "success", "updater_loading").style(
                    "--loading-grow--"
                )
                put_text(t("Gui.Update.UpdateFinish"), scope="updater_state")
                update_table()
            elif state == "cancel":
                put_loading("border", "danger", "updater_loading").style(
                    "--loading-border--"
                )
                put_text(t("Gui.Update.UpdateCancel"), scope="updater_state")
                put_button(
                    t("Gui.Button.CancelUpdate"),
                    onclick=updater.cancel,
                    color="danger",
                    scope="updater_btn",
                    disabled=True,
                )
            else:
                put_text(
                    "Something went wrong, please contact develops",
                    scope="updater_state",
                )
                put_text(f"state: {state}", scope="updater_state")

        updater_switch = Switch(
            status=u, get_state=lambda: updater.state, name="updater"
        )

        update_table()
        self.task_handler.add(updater_switch.g(), delay=0.5, pending_delete=True)

        updater.check_update()

    @use_scope("content", clear=True)
    def dev_utils(self) -> None:
        self.init_menu(name="Utils")
        self.set_title(t("Gui.MenuDevelop.Utils"))
        put_button(label="Raise exception", onclick=raise_exception)

        def _force_restart():
            if State.restart_event is not None:
                toast("Alas will restart in 3 seconds", duration=0, color="error")
                clearup()
                State.restart_event.set()
            else:
                toast("Reload not enabled", color="error")

        put_button(label="Force restart", onclick=_force_restart)

    @use_scope("content", clear=True)
    def dev_remote(self) -> None:
        self.init_menu(name="Remote")
        self.set_title(t("Gui.MenuDevelop.Remote"))
        put_row(
            content=[put_scope("remote_loading"), None, put_scope("remote_state")],
            size="auto .25rem 1fr",
        )
        put_scope("remote_info")

        def u(state):
            if state == -1:
                return
            clear("remote_loading")
            clear("remote_state")
            clear("remote_info")
            if state in (1, 2):
                put_loading("grow", "success", "remote_loading").style(
                    "--loading-grow--"
                )
                put_text(t("Gui.Remote.Running"), scope="remote_state")
                put_text(t("Gui.Remote.EntryPoint"), scope="remote_info")
                entrypoint = RemoteAccess.get_entry_point()
                if entrypoint:
                    if State.electron:  # Prevent click into url in electron client
                        put_text(entrypoint, scope="remote_info").style(
                            "text-decoration-line: underline"
                        )
                    else:
                        put_link(name=entrypoint, url=entrypoint, scope="remote_info")
                else:
                    put_text("Loading...", scope="remote_info")
            elif state in (0, 3):
                put_loading("border", "secondary", "remote_loading").style(
                    "--loading-border-fill--"
                )
                if (
                        State.deploy_config.EnableRemoteAccess
                        and State.deploy_config.Password
                ):
                    put_text(t("Gui.Remote.NotRunning"), scope="remote_state")
                else:
                    put_text(t("Gui.Remote.NotEnable"), scope="remote_state")
                put_text(t("Gui.Remote.ConfigureHint"), scope="remote_info")
                url = "http://app.azurlane.cloud" + (
                    "" if State.deploy_config.Language.startswith("zh") else "/en.html"
                )
                put_html(
                    f'<a href="{url}" target="_blank">{url}</a>', scope="remote_info"
                )
                if state == 3:
                    put_warning(
                        t("Gui.Remote.SSHNotInstall"),
                        closable=False,
                        scope="remote_info",
                    )

        remote_switch = Switch(
            status=u, get_state=RemoteAccess.get_state, name="remote"
        )

        self.task_handler.add(remote_switch.g(), delay=1, pending_delete=True)

    def ui_develop(self) -> None:
        if not self.is_mobile:
            self.show()
            return
        self.init_aside(name="Home")
        self.set_title(t("Gui.Aside.Home"))
        self.dev_set_menu()
        self.alas_name = ""
        if hasattr(self, "alas"):
            del self.alas
        self.state_switch.switch()

    def ui_alas(self, config_name: str) -> None:
        if config_name == self.alas_name:
            self.expand_menu()
            return
        self.init_aside(name=config_name)
        clear("content")
        self.alas_name = config_name
        self.alas_mod = get_config_mod(config_name)
        self.alas = ProcessManager.get_manager(config_name)
        self.alas_config = load_config(config_name)
        self.state_switch.switch()
        self.initial()
        self.alas_set_menu()

    def ui_manage_alas(self) -> None:
        """Full-page manage view: menu (list / import) + content, like Home/Develop."""
        self.init_aside(name="ManageAlas")
        self.alas_name = ""
        if hasattr(self, "alas"):
            del self.alas
        self.set_title(t("Gui.Aside.ManageAlas"))
        self.state_switch.switch()
        self.manage_set_menu()
        self.manage_show_list()

    @use_scope("menu", clear=True)
    def manage_set_menu(self) -> None:
        self.init_menu(collapse_menu=False, name="ManageAlas")
        put_buttons(
            [
                {
                    "label": t("Gui.ManageAlas.TabList"),
                    "value": "ConfigList",
                    "color": "menu",
                }
            ],
            onclick=[lambda: self.manage_show_list()],
        ).style("--menu-ConfigList--")
        put_buttons(
            [
                {
                    "label": t("Gui.ManageAlas.TabImport"),
                    "value": "ImportConfig",
                    "color": "menu",
                }
            ],
            onclick=[lambda: self.manage_show_import()],
        ).style("--menu-ImportConfig--")

    def _manage_instances(self):
        out = []
        for n in alas_instance():
            if not n or n.lower().startswith("template"):
                continue
            if os.path.exists(filepath_config(n, get_config_mod(n))):
                out.append(n)
        return out

    def _manage_refresh_aside(self) -> None:
        # Force full aside redraw after add/delete/import
        self.load_home = True
        self.set_aside()
        self.active_button("aside", "ManageAlas")

    @use_scope("content", clear=True)
    def manage_show_list(self) -> None:
        self.init_menu(collapse_menu=False, name="ConfigList")
        self.set_title(t("Gui.ManageAlas.TabList"))

        instances = self._manage_instances()

        # set_scope(if_exist=clear): reuse existing panel or create once; never put_scope same id
        set_scope("manage_panel", container_scope="content", if_exist="clear")

        with use_scope("manage_panel"):
            put_row(
                [
                    put_text(t("Gui.ManageAlas.TabList")).style(
                        "font-size:1.25rem;margin:auto .5rem auto;"
                    ),
                    put_button(
                        label=t("Gui.ManageAlas.TabAdd"),
                        onclick=self.ui_add_alas,
                        color="on",
                    ).style(
                        "margin:0 .25rem .375rem 0;width:auto;flex-shrink:0;"
                        "white-space:nowrap;font-size:.8125rem;padding:.25rem .75rem;"
                        "line-height:1.25rem;"
                    ),
                ],
                size="1fr auto",
            )
            put_html('<hr class="hr-group">')

            if not instances:
                put_text(t("Gui.ManageAlas.ListEmpty")).style("--arg-help--")
                put_text(t("Gui.ManageAlas.DeleteRunningTip")).style("--arg-help--")
                return

            # Nested list: create once under panel, refill via use_scope
            set_scope("config_list", container_scope="manage_panel", if_exist="clear")
            with use_scope("config_list"):
                for name in instances:
                    put_row(
                        [
                            put_text(name).style(
                                "flex:1;min-width:0;font-size:.875rem;"
                                "line-height:1.25rem;overflow-wrap:anywhere;margin:0;"
                            ),
                            put_button(
                                label=t("Gui.ManageAlas.Delete"),
                                onclick=partial(self._manage_ask_delete, name),
                                color="danger",
                            ),
                        ],
                        size="1fr auto",
                    ).style("--cfg-row-flex--")

            put_text(t("Gui.ManageAlas.DeleteRunningTip")).style("--arg-help--")

    def ui_add_alas(self) -> None:
        """Original add-config popup, opened from Manage > 配置列表."""
        with popup(t("Gui.AddAlas.PopupTitle")) as s:

            def get_unused_name():
                all_name = alas_instance()
                for i in range(2, 100):
                    if f"ns{i}" not in all_name:
                        return f"ns{i}"
                else:
                    return ""

            def add():
                name = pin["AddAlas_name"]
                origin = pin["AddAlas_copyfrom"]

                if name in alas_instance():
                    err = "Gui.AddAlas.FileExist"
                elif set(name) & set(".\\/:*?\"'<>|"):
                    err = "Gui.AddAlas.InvalidChar"
                elif name.lower().startswith("template"):
                    err = "Gui.AddAlas.InvalidPrefixTemplate"
                else:
                    err = ""
                if err:
                    clear(s)
                    put(name, origin)
                    put_error(t(err), scope=s)
                    return

                r = load_config(origin).read_file(origin)
                State.config_updater.write_file(name, r, get_config_mod(origin))
                close_popup()
                self._manage_refresh_aside()
                self.manage_show_list()
                toast(t("Gui.ManageAlas.AddSuccess", name=name), color="success")

            def put(name=None, origin=None):
                put_input(
                    name="AddAlas_name",
                    label=t("Gui.AddAlas.NewName"),
                    value=name or get_unused_name(),
                    scope=s,
                ),
                put_select(
                    name="AddAlas_copyfrom",
                    label=t("Gui.AddAlas.CopyFrom"),
                    options=alas_template() + alas_instance(),
                    value=origin or "template-ns",
                    scope=s,
                ),
                put_button(label=t("Gui.AddAlas.Confirm"), onclick=add, scope=s)

            put()

    def _manage_ask_delete(self, name: str) -> None:
        with popup(t("Gui.ManageAlas.Delete")) as s:
            put_warning(t("Gui.ManageAlas.DeleteConfirm", name=name), scope=s)
            put_buttons(
                [
                    {"label": t("Gui.ManageAlas.DeleteYes"), "value": "yes", "color": "danger"},
                    {"label": t("Gui.ManageAlas.DeleteNo"), "value": "no", "color": "secondary"},
                ],
                onclick=[
                    lambda: self._manage_delete(name),
                    lambda: close_popup(),
                ],
                scope=s,
            )

    def _manage_delete(self, name: str) -> None:
        close_popup()
        if not name or name.lower().startswith("template"):
            toast(t("Gui.AddAlas.InvalidPrefixTemplate"), color="error")
            return

        try:
            manager = ProcessManager.get_manager(name)
            if manager.alive:
                manager.stop()
            ProcessManager._processes.pop(name, None)
            path = filepath_config(name, get_config_mod(name))
            if os.path.exists(path):
                os.remove(path)
            if self.alas_name == name:
                self.alas_name = ""
                if hasattr(self, "alas"):
                    del self.alas
            self._manage_refresh_aside()
            self.manage_show_list()
            toast(t("Gui.ManageAlas.DeleteSuccess", name=name), color="success")
        except Exception as e:
            logger.exception(e)
            toast(f"{t('Gui.ManageAlas.DeleteFailed')}: {e}", color="error")

    @use_scope("content", clear=True)
    def manage_show_import(self) -> None:
        self.init_menu(collapse_menu=False, name="ImportConfig")
        self.set_title(t("Gui.ManageAlas.TabImport"))

        def do_import():
            try:
                files = pin["ImportAlas_file"]
            except KeyError:
                files = None
            if not files:
                clear("import_result")
                put_error(t("Gui.ManageAlas.ImportEmpty"), scope="import_result")
                return
            if isinstance(files, dict):
                files = [files]

            imported, errors = [], []
            for f in files:
                filename = f.get("filename") or ""
                content = f.get("content") or b""
                if not filename or not content:
                    errors.append(filename or "?")
                    continue

                base = os.path.splitext(os.path.basename(filename))[0]
                if not filename.lower().endswith(".json"):
                    errors.append(filename)
                    continue
                if not base or base.lower().startswith("template"):
                    errors.append(filename)
                    continue
                if set(base) & set(".\\/:*?\"'<>|"):
                    errors.append(filename)
                    continue

                name = base
                existing = self._manage_instances() + alas_instance()
                if name in existing:
                    i = 2
                    while f"{name}{i}" in existing:
                        i += 1
                    name = f"{name}{i}"

                try:
                    data = json.loads(content.decode("utf-8"))
                    if not isinstance(data, dict):
                        raise ValueError("Invalid config content")
                    State.config_updater.write_file(name, data, "alas")
                    imported.append(name)
                except Exception as e:
                    logger.exception(e)
                    errors.append(f"{filename}: {e}")

            self._manage_refresh_aside()
            clear("import_result")
            with use_scope("import_result"):
                if imported:
                    put_text(
                        t("Gui.ManageAlas.ImportSuccess", names=", ".join(imported))
                    ).style("color:#00b42a;")
                if errors:
                    put_error(
                        t("Gui.ManageAlas.ImportFailed", names=", ".join(errors))
                    )

        set_scope("manage_panel", container_scope="content", if_exist="clear")
        with use_scope("manage_panel"):
            put_text(t("Gui.ManageAlas.TabImport")).style(
                "font-size:1.25rem;margin:auto .5rem auto;"
            )
            put_html('<hr class="hr-group">')
            put_text(t("Gui.ManageAlas.ImportHint")).style("--arg-help--")
            put_row(
                [
                    put_file_upload(
                        name="ImportAlas_file",
                        label=t("Gui.ManageAlas.ImportFile"),
                        accept=[".json"],
                        multiple=True,
                    ),
                    put_button(
                        label=t("Gui.ManageAlas.Import"),
                        onclick=do_import,
                        color="on",
                    ).style(
                        "margin:1.55rem .25rem 0 .5rem;width:auto;flex-shrink:0;"
                        "white-space:nowrap;font-size:.8125rem;padding:.25rem .75rem;"
                        "line-height:1.25rem;"
                    ),
                ],
                size="1fr auto",
            )
            set_scope("import_result", container_scope="manage_panel", if_exist="clear")

    def show(self) -> None:
        self._show()
        self.load_home = True
        self.set_aside()
        self.init_aside(name="Home")
        self.dev_set_menu()
        self.init_menu(name="HomePage")
        self.alas_name = ""
        if hasattr(self, "alas"):
            del self.alas
        self.set_status(0)

        def set_language(l):
            lang.set_language(l)
            self.show()

        def set_theme(t):
            self.set_theme(t)
            run_js("location.reload()")

        with use_scope("content"):
            put_text("Select your language / 选择语言").style("text-align: center")
            put_buttons(
                [
                    {"label": "简体中文", "value": "zh-CN"},
                    {"label": "繁體中文", "value": "zh-TW"},
                    {"label": "English", "value": "en-US"},
                    {"label": "日本語", "value": "ja-JP"},
                    {"label": "Español", "value": "es-ES"},
                ],
                onclick=lambda l: set_language(l),
            ).style("text-align: center")
            put_text("Change theme / 更改主题").style("text-align: center")
            put_buttons(
                [
                    {"label": "Light", "value": "default", "color": "light"},
                    {"label": "Dark", "value": "dark", "color": "dark"},
                ],
                onclick=lambda t: set_theme(t),
            ).style("text-align: center")

            # show something
            put_markdown(
                """
            NarutoScript is a free open source software, if you paid for NS from any channel, please refund.
            NarutoScript 是一款免费开源软件，如果你在任何渠道付费购买了NS，请退款。
            Project repository 项目地址：`https://github.com/Elmyran/NarutoScript`
            QQ群:921572302,有问题可以进群反馈
            """
            ).style("text-align: center")

        if lang.TRANSLATE_MODE:
            lang.reload()

            def _disable():
                lang.TRANSLATE_MODE = False
                self.show()

            toast(
                _t("Gui.Toast.DisableTranslateMode"),
                duration=0,
                position="right",
                onclick=_disable,
            )

    def run(self) -> None:
        # setup gui
        set_env(title="NarutoScript", output_animation=False)
        add_css(filepath_css("alas"))
        if self.is_mobile:
            add_css(filepath_css("alas-mobile"))
        else:
            add_css(filepath_css("alas-pc"))

        if self.theme == "dark":
            add_css(filepath_css("dark-alas"))
        else:
            add_css(filepath_css("light-alas"))

        # Auto refresh when lost connection
        # [For develop] Disable by run `reload=0` in console
        run_js(
            """
        reload = 1;
        window.__nsLastAlive = Date.now();
        // Heartbeat: if UI stops receiving any WebIO traffic for a long time, force reload
        (function () {
            if (window.__nsAliveTimer) return;
            window.__nsAliveTimer = setInterval(function () {
                if (typeof reload === 'undefined' || reload !== 1) return;
                var sess = WebIO && WebIO._state && WebIO._state.CurrentSession;
                // Mark alive on any outgoing/incoming if possible; fall back to DOM presence
                var hasRoot = !!document.getElementById('pywebio-scope-ROOT');
                var hasContent = !!document.getElementById('pywebio-scope-content');
                // White-screen / hung session: root missing, or content empty for a long time
                var contentEmpty = hasContent && document.getElementById('pywebio-scope-content').children.length === 0;
                var now = Date.now();
                if (!hasRoot || (contentEmpty && now - (window.__nsLastAlive || 0) > 90000)) {
                    if (now - (window.__nsLastReload || 0) > 30000) {
                        window.__nsLastReload = now;
                        location.reload();
                    }
                }
            }, 15000);
        })();
        WebIO._state.CurrentSession.on_session_close(
            ()=>{
                setTimeout(
                    ()=>{
                        if (reload == 1){
                            location.reload();
                        }
                    }, 4000
                )
            }
        );
        """
        )

        # Delegated handlers for sortable priority lists
        # put_html(<script>) is stripped by jQuery, so bind once here
        # Drag: take the row out of flow (position:fixed), follow pointer with
        # transform (no CSS transition), leave a placeholder for reordering.
        run_js(
            r"""
        if (!window.__nsSortableBound) {
            window.__nsSortableBound = true;

            function nsSortableItems(list) {
                return Array.prototype.slice.call(list.querySelectorAll('.sortable-item'));
            }
            function nsSortableSync(list) {
                if (!list) return;
                var input = document.querySelector('input[name="' + list.id.replace('sortable-list-', '') + '"]');
                if (!input) return;
                var values = nsSortableItems(list).map(function (el) {
                    return el.getAttribute('data-value');
                });
                var next = values.join('>');
                if (input.value !== next) {
                    input.value = next;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
            function nsSortableFlip(list, mutate, highlightEls) {
                var items = Array.prototype.slice.call(list.children).filter(function (el) {
                    if (!el.classList) return false;
                    // Never animate the row currently under the pointer
                    if (el.classList.contains('sortable-dragging')) return false;
                    return el.classList.contains('sortable-item') ||
                        el.classList.contains('sortable-placeholder');
                });
                var firstTops = new Map();
                items.forEach(function (el) {
                    firstTops.set(el, el.getBoundingClientRect().top);
                });
                mutate();
                // Double rAF: paint the inverted state once, then play
                items.forEach(function (el) {
                    var first = firstTops.get(el);
                    if (first === undefined) return;
                    var dy = first - el.getBoundingClientRect().top;
                    if (!dy) return;
                    el.style.transition = 'none';
                    el.style.transform = 'translate3d(0,' + dy + 'px,0)';
                    requestAnimationFrame(function () {
                        requestAnimationFrame(function () {
                            if (!el.isConnected) return;
                            el.style.transition = 'transform 200ms cubic-bezier(0.2, 0.7, 0.3, 1)';
                            el.style.transform = 'translate3d(0,0,0)';
                        });
                    });
                });
                if (highlightEls && highlightEls.length) {
                    highlightEls.forEach(function (el) {
                        if (!el || !el.classList) return;
                        el.classList.add('sortable-moved');
                        setTimeout(function () {
                            el.classList.remove('sortable-moved');
                        }, 280);
                    });
                }
            }
            function nsSortableMove(list, value, delta) {
                if (!list) return;
                var items = nsSortableItems(list);
                var index = -1;
                for (var i = 0; i < items.length; i++) {
                    if (items[i].getAttribute('data-value') === value) { index = i; break; }
                }
                var target = index + delta;
                if (index < 0 || target < 0 || target >= items.length) return;
                var current = items[index];
                var other = items[target];
                // Animate BOTH rows so the swap is readable
                nsSortableFlip(list, function () {
                    if (delta < 0) {
                        list.insertBefore(current, other);
                    } else {
                        list.insertBefore(other, current);
                    }
                }, [current, other]);
                nsSortableSync(list);
            }
            function nsSortableReset(list, order) {
                if (!list || !order || !order.length) return;
                var byValue = {};
                nsSortableItems(list).forEach(function (el) {
                    byValue[el.getAttribute('data-value')] = el;
                });
                var moved = [];
                nsSortableFlip(list, function () {
                    order.forEach(function (value) {
                        var el = byValue[value];
                        if (el) {
                            list.appendChild(el);
                            delete byValue[value];
                            moved.push(el);
                        }
                    });
                    Object.keys(byValue).forEach(function (value) {
                        list.appendChild(byValue[value]);
                        moved.push(byValue[value]);
                    });
                }, moved);
                nsSortableSync(list);
            }

            window.nsSortableReset = nsSortableReset;
            window.nsSortableSync = nsSortableSync;

            document.addEventListener('click', function (e) {
                var btn = e.target.closest ? e.target.closest('.sortable-up, .sortable-down') : null;
                if (!btn) return;
                e.preventDefault();
                var list = btn.closest('.sortable-list');
                var delta = btn.classList.contains('sortable-up') ? -1 : 1;
                nsSortableMove(list, btn.getAttribute('data-value'), delta);
            });

            // --- pointer drag ---
            var drag = null;
            var rafPending = false;
            var lastClientX = 0;
            var lastClientY = 0;

            function nsClearDrag() {
                if (!drag) return;
                var d = drag;
                drag = null;
                rafPending = false;
                if (d.ph && d.ph.parentNode) {
                    d.ph.parentNode.removeChild(d.ph);
                }
                if (d.el) {
                    d.el.classList.remove('sortable-dragging');
                    d.el.style.transform = '';
                    d.el.style.width = '';
                    d.el.style.height = '';
                }
                try {
                    document.documentElement.releasePointerCapture(d.pointerId);
                } catch (err) {}
                document.body.classList.remove('sortable-body-dragging');
            }

            function nsPlaceCard(clientX, clientY) {
                if (!drag || !drag.el) return;
                var x = clientX - drag.grabX;
                var y = clientY - drag.grabY;
                drag.el.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
            }

            function nsMaybeReorder() {
                if (!drag || !drag.active || !drag.ph) return;
                var list = drag.list;
                if (!list) return;

                var mid = lastClientY;
                var items = Array.prototype.slice.call(list.children).filter(function (el) {
                    if (el === drag.ph || el === drag.el) return false;
                    return el.classList.contains('sortable-item') ||
                        el.classList.contains('sortable-placeholder');
                });
                if (!items.length) {
                    if (drag.ph.nextSibling !== null) list.appendChild(drag.ph);
                    return;
                }

                var insertBefore = null;
                for (var i = 0; i < items.length; i++) {
                    var rect = items[i].getBoundingClientRect();
                    if (mid < rect.top + rect.height * 0.5) {
                        insertBefore = items[i];
                        break;
                    }
                }

                if (!insertBefore) {
                    if (!drag.ph.nextSibling) return;
                    nsSortableFlip(list, function () {
                        list.insertBefore(drag.ph, null);
                    }, null);
                    return;
                }
                if (drag.ph.nextSibling === insertBefore) return;
                nsSortableFlip(list, function () {
                    list.insertBefore(drag.ph, insertBefore);
                }, null);
            }

            function nsOnDragMove(e) {
                if (!drag) return;
                if (e.pointerId !== undefined && drag.pointerId !== undefined && e.pointerId !== drag.pointerId) return;
                lastClientX = e.clientX;
                lastClientY = e.clientY;
                if (!drag.active) {
                    var dx = e.clientX - drag.startClientX;
                    var dy = e.clientY - drag.startClientY;
                    if (dx * dx + dy * dy < 9) return;
                    drag.active = true;
                    drag.el.classList.add('sortable-dragging');
                    document.body.classList.add('sortable-body-dragging');
                }
                // Follow pointer every event - no transition on the card
                nsPlaceCard(e.clientX, e.clientY);
                if (rafPending) return;
                rafPending = true;
                requestAnimationFrame(function () {
                    rafPending = false;
                    if (drag && drag.active) nsMaybeReorder();
                });
            }

            function nsEndDrag(e) {
                if (!drag) return;
                if (e && e.pointerId !== undefined && drag.pointerId !== undefined && e.pointerId !== drag.pointerId) return;
                var wasActive = drag.active;
                var list = drag.list;
                var el = drag.el;
                var ph = drag.ph;
                if (wasActive && ph && el && ph.parentNode) {
                    ph.parentNode.insertBefore(el, ph);
                }
                nsClearDrag();
                if (wasActive && list) nsSortableSync(list);
            }

            document.addEventListener('pointerdown', function (e) {
                if (drag) return;
                if (e.button !== 0 && e.pointerType === 'mouse') return;
                var item = e.target.closest ? e.target.closest('.sortable-item') : null;
                if (!item) return;
                if (e.target.closest('.sortable-btn')) return;
                var list = item.closest('.sortable-list');
                if (!list) return;
                if (!item.querySelector('.sortable-handle')) return;

                e.preventDefault();

                var rect = item.getBoundingClientRect();
                var ph = document.createElement('li');
                ph.className = 'sortable-placeholder';
                ph.style.height = rect.height + 'px';

                item.parentNode.insertBefore(ph, item);
                item.style.width = rect.width + 'px';
                item.style.height = rect.height + 'px';
                item.style.transform = 'translate3d(' + rect.left + 'px,' + rect.top + 'px,0)';

                drag = {
                    el: item,
                    ph: ph,
                    list: list,
                    grabX: e.clientX - rect.left,
                    grabY: e.clientY - rect.top,
                    startClientX: e.clientX,
                    startClientY: e.clientY,
                    active: false,
                    pointerId: e.pointerId
                };
                try {
                    document.documentElement.setPointerCapture(e.pointerId);
                } catch (err) {}
            });

            document.addEventListener('pointermove', nsOnDragMove);
            document.addEventListener('pointerup', nsEndDrag);
            document.addEventListener('pointercancel', nsEndDrag);
            window.addEventListener('blur', function () { if (drag) nsEndDrag(null); });
        }
        """
        )

        aside = get_localstorage("aside")
        self.show()

        # init config watcher
        self._init_alas_config_watcher()

        # save config
        _thread_save_config = threading.Thread(target=self._alas_thread_update_config)
        register_thread(_thread_save_config)
        _thread_save_config.start()

        visibility_state_switch = Switch(
            status={
                True: [
                    lambda: self.__setattr__("visible", True),
                    lambda: self.alas_update_overview_task()
                    if self.page == "Overview"
                    else 0,
                    lambda: self.task_handler._task.__setattr__("delay", 15),
                ],
                False: [
                    lambda: self.__setattr__("visible", False),
                    lambda: self.task_handler._task.__setattr__("delay", 1),
                ],
            },
            get_state=get_window_visibility_state,
            name="visibility_state",
        )

        self.state_switch = Switch(
            status=self.set_status,
            get_state=lambda: getattr(getattr(self, "alas", -1), "state", 0),
            name="state",
        )

        def goto_update():
            self.ui_develop()
            self.dev_update()

        update_switch = Switch(
            status={
                1: lambda: toast(
                    t("Gui.Toast.ClickToUpdate"),
                    duration=0,
                    position="right",
                    color="success",
                    onclick=goto_update,
                )
            },
            get_state=lambda: updater.state,
            name="update_state",
        )

        self.task_handler.add(self.state_switch.g(), 2)
        self.task_handler.add(self.set_aside_status, 2)
        self.task_handler.add(visibility_state_switch.g(), 15)
        self.task_handler.add(update_switch.g(), 1)
        self.task_handler.start()

        # Return to previous page
        if aside == "ManageAlas":
            self.ui_manage_alas()
        elif aside not in ["Home", None]:
            self.ui_alas(aside)


def debug():
    """For interactive python.
    $ python3
    >>> from module.webui.app import *
    >>> debug()
    >>>
    """
    startup()
    AlasGUI().run()


def startup():
    State.init()
    lang.reload()
    updater.event = State.manager.Event()
    if updater.delay > 0:
        task_handler.add(updater.check_update, updater.delay)
    task_handler.add(updater.schedule_update(), 86400)
    task_handler.start()
    # if State.deploy_config.DiscordRichPresence:
    #     init_discord_rpc()
    # if State.deploy_config.StartOcrServer:
    #     start_ocr_server_process(State.deploy_config.OcrServerPort)
    if (
            State.deploy_config.EnableRemoteAccess
            and State.deploy_config.Password is not None
    ):
        task_handler.add(RemoteAccess.keep_ssh_alive(), 60)


def clearup():
    """
    Notice: Ensure run it before uvicorn reload app,
    all process will NOT EXIT after close electron app.
    """
    logger.info("Start clearup")
    RemoteAccess.kill_ssh_process()
    # close_discord_rpc()
    # stop_ocr_server_process()
    for alas in ProcessManager._processes.values():
        alas.stop()
    State.clearup()
    task_handler.stop()
    logger.info("Alas closed.")


def app():
    parser = argparse.ArgumentParser(description="Alas web service")
    parser.add_argument(
        "-k", "--key", type=str, help="Password of alas. No password by default"
    )
    parser.add_argument(
        "--cdn",
        action="store_true",
        help="Use jsdelivr cdn for pywebio static files (css, js). Self host cdn by default.",
    )
    parser.add_argument(
        "--run",
        nargs="+",
        type=str,
        help="Run alas by config names on startup",
    )
    args, _ = parser.parse_known_args()

    # Apply config
    AlasGUI.set_theme(theme=State.deploy_config.Theme)
    lang.LANG = State.deploy_config.Language
    key = args.key or State.deploy_config.Password
    cdn = args.cdn if args.cdn else State.deploy_config.CDN
    runs = None
    if args.run:
        runs = args.run
    elif State.deploy_config.Run:
        # TODO: refactor poor_yaml_read() to support list
        tmp = State.deploy_config.Run.split(",")
        runs = [l.strip(" ['\"]") for l in tmp if len(l)]
    instances: List[str] = runs

    logger.hr("Webui configs")
    logger.attr("Theme", State.deploy_config.Theme)
    logger.attr("Language", lang.LANG)
    logger.attr("Password", True if key else False)
    logger.attr("CDN", cdn)

    from deploy.Windows.atomic import atomic_failure_cleanup
    atomic_failure_cleanup('./config')

    def index():
        if key is not None and not login(key):
            logger.warning(f"{info.user_ip} login failed.")
            time.sleep(1.5)
            run_js("location.reload();")
            return
        gui = AlasGUI()
        local.gui = gui
        gui.run()

    app = asgi_app(
        applications=[index],
        cdn=cdn,
        static_dir=None,
        debug=True,
        on_startup=[
            startup,
            lambda: ProcessManager.restart_processes(
                instances=instances, ev=updater.event
            ),
        ],
        on_shutdown=[clearup],
    )

    return app
