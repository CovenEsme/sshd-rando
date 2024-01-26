from collections import Counter
from functools import partial

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QWidget,
)

from constants.configconstants import get_default_setting, get_new_seed
from constants.guiconstants import *
from constants.itemconstants import STARTABLE_ITEMS
from filepathconstants import CONFIG_PATH, ITEMS_PATH
from gui.components.list_pair import ListPair
from gui.mixed_entrance_pools import MixedEntrancePools
from logic.config import Config, write_config_to_file
from logic.location_table import build_location_table, get_disabled_shuffle_locations
from logic.settings import Setting
from sslib.yaml import yaml_load

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main
    from gui.ui.ui_main import Ui_main_window


class Settings:
    def __init__(self, main: "Main", ui: "Ui_main_window"):
        self.main = main
        self.ui = ui
        self.config: Config = main.config

        self.settings = self.config.settings[0].settings
        self.location_table = build_location_table()

        self.set_setting_descriptions(None)

        # Init seed
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        seed_widget.setText(self.config.seed)
        seed_widget.textChanged.connect(self.update_seed)

        self.ui.new_seed_button.clicked.connect(self.new_seed)
        self.ui.reset_settings_to_default_button.clicked.connect(self.reset)

        # Init mixed entrance pools
        mixed_entrance_pools = self.config.settings[0].mixed_entrance_pools
        self.mixed_entrance_pools = MixedEntrancePools(
            self.main, self.ui, mixed_entrance_pools
        )
        self.mixed_entrance_pools.mixedEntrancePoolsChanged.connect(
            partial(self.update_settings, update_descriptions=False)
        )

        # Init excluded locations
        excludable_locations = list(
            (location.name, location.types)
            for location in self.location_table.values()
            if location.is_gui_excluded_location
        )

        self.exclude_locations_pair = ListPair(
            self.config.settings[0].excluded_locations,
            get_default_setting("excluded_locations"),
            self.ui.excluded_locations_list_view,
            self.ui.included_locations_list_view,
            self.ui.exclude_location_button,
            self.ui.include_location_button,
            self.ui.locations_reset_button,
            excludable_locations,
            excluder_list=self.get_disabled_shuffle_location_names(),
        )
        self.exclude_locations_pair.listPairChanged.connect(self.update_settings)

        self.ui.excluded_locations_free_search.textChanged.connect(
            self.exclude_locations_pair.update_option_list_filter
        )
        self.ui.included_locations_free_search.textChanged.connect(
            self.exclude_locations_pair.update_non_option_list_filter
        )

        self.ui.included_locations_type_filter.addItem("All")
        self.ui.included_locations_type_filter.addItems(LOCATION_FILTER_TYPES)
        self.ui.included_locations_type_filter.currentTextChanged.connect(
            self.exclude_locations_pair.update_non_option_list_type_filter
        )

        self.ui.excluded_locations_type_filter.addItem("All")
        self.ui.excluded_locations_type_filter.addItems(LOCATION_FILTER_TYPES)
        self.ui.excluded_locations_type_filter.currentTextChanged.connect(
            self.exclude_locations_pair.update_option_list_type_filter
        )

        # Init excluded hint locations
        excludable_hint_locations = list(
            (location.name, location.types)
            for location in self.location_table.values()
            if "Hint Location" in location.types
        )

        self.exclude_hints_locations_pair = ListPair(
            self.config.settings[0].excluded_hint_locations,
            get_default_setting("excluded_hint_locations"),
            self.ui.excluded_hint_locations_list_view,
            self.ui.included_hint_locations_list_view,
            self.ui.exclude_hint_location_button,
            self.ui.include_hint_location_button,
            self.ui.hints_reset_button,
            excludable_hint_locations,
        )
        self.exclude_hints_locations_pair.listPairChanged.connect(self.update_settings)

        self.ui.excluded_hint_locations_free_search.textChanged.connect(
            self.exclude_hints_locations_pair.update_option_list_filter
        )
        self.ui.included_hint_locations_free_search.textChanged.connect(
            self.exclude_hints_locations_pair.update_non_option_list_filter
        )

        # Type filters will be added once there are multiple types of hint sources
        #
        # self.ui.included_hint_locations_type_filter.addItem("All")
        # self.ui.included_hint_locations_type_filter.addItems(LOCATION_FILTER_TYPES)
        # self.ui.included_hint_locations_type_filter.currentTextChanged.connect(
        #     self.exclude_hints_locations_pair.update_non_option_list_type_filter
        # )

        # self.ui.excluded_hint_locations_type_filter.addItem("All")
        # self.ui.excluded_hint_locations_type_filter.addItems(LOCATION_FILTER_TYPES)
        # self.ui.excluded_hint_locations_type_filter.currentTextChanged.connect(
        #     self.exclude_hints_locations_pair.update_option_list_type_filter
        # )

        # Init starting items
        item_defs: list[dict] = list(yaml_load(ITEMS_PATH))
        item_types: dict[str, list[str]] = {
            item["name"]: item["types"] for item in item_defs
        }

        startable_items = list(
            (item_name, item_types[item_name]) for item_name in STARTABLE_ITEMS
        )

        self.starting_inventory_pair = ListPair(
            list(self.config.settings[0].starting_inventory.elements()),
            list(get_default_setting("starting_inventory").elements()),
            self.ui.starting_items_list_view,
            self.ui.randomized_items_list_view,
            self.ui.start_with_item_button,
            self.ui.randomize_item_button,
            self.ui.inventory_reset_button,
            startable_items,
        )
        self.starting_inventory_pair.listPairChanged.connect(self.update_settings)

        self.ui.starting_items_free_search.textChanged.connect(
            self.starting_inventory_pair.update_option_list_filter
        )
        self.ui.randomized_items_free_search.textChanged.connect(
            self.starting_inventory_pair.update_non_option_list_filter
        )

        self.ui.randomized_items_type_filter.addItem("All")
        self.ui.randomized_items_type_filter.addItems(ITEM_FILTER_TYPES)
        self.ui.randomized_items_type_filter.currentTextChanged.connect(
            self.starting_inventory_pair.update_non_option_list_type_filter
        )

        self.ui.starting_items_type_filter.addItem("All")
        self.ui.starting_items_type_filter.addItems(ITEM_FILTER_TYPES)
        self.ui.starting_items_type_filter.currentTextChanged.connect(
            self.starting_inventory_pair.update_option_list_type_filter
        )

        # Init other settings
        for setting_name, setting_info in self.settings.items():
            current_option_value = setting_info.value

            widget = None  # type: ignore
            label = None  # type: ignore

            try:
                widget: QWidget = getattr(self.ui, "setting_" + setting_name)
            except:
                print(f"Could not find widget for setting: {setting_name}.")
                continue

            # Used to change the settings description when mousing over a setting
            widget.installEventFilter(self.main)

            try:
                label = getattr(self.ui, setting_name + "_label")
                label.setText(setting_info.info.pretty_name)
                label.installEventFilter(self.main)
            except:
                pass

            if isinstance(widget, QCheckBox):  # on or off
                widget.setTristate(True)

                if current_option_value == "on":
                    widget.setChecked(True)
                elif current_option_value == "random":
                    widget.setCheckState(Qt.CheckState.PartiallyChecked)
                elif current_option_value == "off":
                    widget.setChecked(False)
                else:
                    raise TypeError(
                        f"Setting '{setting_name}' has value '{current_option_value}' which is invalid for a QAbstractButton. Expected either 'on' or 'off'."
                    )

                widget.setText(setting_info.info.pretty_name)
                widget.clicked.connect(partial(self.update_settings, widget))
            elif isinstance(widget, QComboBox):  # pick one option
                for option in setting_info.info.pretty_options:
                    widget.addItem(option)

                widget.setCurrentIndex(
                    setting_info.info.options.index(setting_info.value)
                )
                widget.currentIndexChanged.connect(
                    partial(self.update_settings, widget)
                )
            elif isinstance(widget, QSpinBox):  # pick a value
                widget.setMinimum(
                    int(setting_info.info.options[0]) - 1
                )  # -1 for special value
                widget.setMaximum(int(setting_info.info.options[-2]))
                widget.setSpecialValueText("Random")

                if current_option_value == "random":
                    widget.setValue(widget.minimum())
                else:
                    widget.setValue(int(current_option_value))

                widget.valueChanged.connect(partial(self.update_settings, widget))

        # Force descriptions to update before changing any setting
        self.update_settings()

    def update_settings(
        self,
        from_widget=None,
        widget_info=None,
        update_descriptions: bool = True,
        allow_rewrite: bool = True,
    ):
        should_update_location_counter = True

        for setting_name, setting in self.settings.items():
            widget = None  # type: ignore

            try:
                widget: QWidget = getattr(self.ui, "setting_" + setting_name)
            except:
                # print(f"Cannot find attribute for '{setting_name}', ignoring.")
                continue

            if not widget:
                continue

            if widget == from_widget and "shuffle" not in setting_name:
                should_update_location_counter = False

            new_setting = setting
            new_option = ""

            if isinstance(widget, QCheckBox):
                # Makes tristate buttons cycle: off, on, random
                # instead of off, random, on
                # but only when manually changed
                if widget == from_widget and update_descriptions:
                    if widget.checkState() == Qt.CheckState.Checked:
                        widget.setCheckState(Qt.CheckState.Unchecked)
                        new_option = "off"
                    elif widget.checkState() == Qt.CheckState.PartiallyChecked:
                        widget.setCheckState(Qt.CheckState.Checked)
                        new_option = "on"
                    else:
                        widget.setCheckState(Qt.CheckState.PartiallyChecked)
                        new_option = "random"
                else:
                    if widget.checkState() == Qt.CheckState.Checked:
                        new_option = "on"
                    elif widget.checkState() == Qt.CheckState.PartiallyChecked:
                        new_option = "random"
                    else:
                        new_option = "off"
            elif isinstance(widget, QComboBox):
                new_option = new_setting.info.options[widget.currentIndex()]
            elif isinstance(widget, QSpinBox):
                new_option = str(widget.value())

            self.settings[setting_name] = self.get_updated_setting(
                new_setting, new_option
            )

            widget.setToolTip(
                "➜ Right-click to view all options.\n➜ Middle-click to reset to default."
            )

        self.config.settings[0].settings = self.settings

        # Special cases
        ## Excluded locations
        excluded_locations = self.exclude_locations_pair.get_added()
        self.config.settings[0].excluded_locations = excluded_locations

        ## Excluded hint locations
        excluded_hint_locations = self.exclude_hints_locations_pair.get_added()
        self.config.settings[0].excluded_hint_locations = excluded_hint_locations

        ## Starting inventory
        starting_inventory = self.starting_inventory_pair.get_added()
        self.config.settings[0].starting_inventory = Counter(starting_inventory)

        ## Mixed entrance pools
        if isinstance(from_widget, MixedEntrancePools) and widget_info is not None:
            mixed_entrance_pools = [pool for pool in widget_info if len(pool) > 0]
            self.config.settings[0].mixed_entrance_pools = mixed_entrance_pools

        if allow_rewrite:
            write_config_to_file(CONFIG_PATH, self.config)

        # Has to be updated *after* the the config has been rewritten
        #
        # This operation isn't *very* expensive but it does require re-reading
        # the config file so only do it if something has actually changed
        if should_update_location_counter:
            disabled_shuffle_locations = self.get_disabled_shuffle_location_names()
            self.exclude_locations_pair.update_excluder_list(disabled_shuffle_locations)

            included_loc_count = len(
                [
                    location
                    for location in self.exclude_locations_pair.get_not_added()
                    if location not in disabled_shuffle_locations
                ]
            )
            excluded_loc_count = len(
                [
                    location
                    for location in excluded_locations
                    if location not in disabled_shuffle_locations
                ]
            )
            total_loc_count = excluded_loc_count + included_loc_count
            self.ui.included_locations_group_box.setTitle(
                f"Included Locations ({included_loc_count} out of {total_loc_count})"
            )

        if update_descriptions:
            self.update_descriptions(from_widget)

    def get_updated_setting(self, setting: Setting, value: str) -> Setting:
        if value == "":
            raise ValueError(
                f"Cannot update setting '{setting.name}' value as value is empty."
            )

        new_setting = setting

        if ((value.startswith("-") and value[1:].isdigit()) or value.isdigit()) and int(
            value
        ) == int(setting.info.options[0]) - 1:
            option_index = setting.info.options.index("random")
            new_setting.value = "random"
        else:
            option_index = setting.info.options.index(value)
            new_setting.value = value

        new_setting.current_option_index = option_index
        new_setting.info.current_option_index = option_index

        return new_setting

    def new_seed(self):
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        seed_widget.setText(get_new_seed())

    def update_seed(self):
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        self.config.seed = seed_widget.text()

        write_config_to_file(CONFIG_PATH, self.config)

    def reset_single(
        self, setting: Setting | None, from_reset_all: bool = False
    ) -> bool:
        if setting is None:
            return False

        setting_name = setting.info.name
        widget = None  # type: ignore

        try:
            widget: QWidget = getattr(self.ui, "setting_" + setting_name)
        except:
            # print(f"Cannot find attribute for '{setting_name}', ignoring.")
            return False

        if not widget:
            return False

        default_option = setting.info.options[setting.info.default_option_index]

        if isinstance(widget, QCheckBox):
            if default_option == "on":
                widget.setCheckState(Qt.CheckState.Checked)
            elif default_option == "random":
                widget.setCheckState(Qt.CheckState.PartiallyChecked)
            elif default_option == "off":
                widget.setCheckState(Qt.CheckState.Unchecked)
        elif isinstance(widget, QComboBox):
            widget.setCurrentIndex(setting.info.default_option_index)
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(default_option))

        # Otherwise, the config file is re-written once for *every* setting
        if not from_reset_all:
            self.update_settings(from_widget=widget, update_descriptions=False)

        return True

    def reset(self):
        confirm_choice = QMessageBox.question(
            self.main,
            "Are you sure?",
            "Are you sure you want to reset EVERY option?",
        )

        if confirm_choice != QMessageBox.Yes:  # type: ignore (Qt is stupid)
            return

        for setting_name, setting in self.settings.items():
            self.reset_single(setting, from_reset_all=True)

        self.mixed_entrance_pools.reset()
        self.exclude_locations_pair.reset()
        self.exclude_hints_locations_pair.reset()
        self.starting_inventory_pair.reset()

    def get_setting_from_widget(self, widget: QObject | None) -> Setting | None:
        if not widget:
            return None

        widget_name = widget.objectName()
        setting_name = widget_name.removeprefix("setting_")
        setting_name = setting_name.removesuffix("_label")

        if self.settings.get(setting_name):
            return self.settings[setting_name]
        else:
            return None

    def set_setting_descriptions(self, setting: Setting | None):
        if setting is None:
            default_description = (
                OPTION_PREFIX
                + "Hover over a setting to see a description of the current and default options.<br>"
            )
            default_description += (
                OPTION_PREFIX
                + "Right click a setting to see a full description of all the options.<br>"
            )
            default_description += (
                OPTION_PREFIX + "Middle click a setting to reset it to default."
            )

            self.ui.settings_current_option_description_label.setText(
                default_description
            )
            self.ui.settings_default_option_description_label.setText("")
            # self.ui.settings_current_option_description_label.setStyleSheet("color: grey;")
        else:
            current_option_description = (
                "<b>Current Option</b> (<i>Right-click to see all the options</i>):<br>"
            )
            current_option_description += self.format_description(
                setting, setting.current_option_index
            )
            default_option_description = "<b>Default Option</b>:<br>"
            default_option_description += self.format_description(
                setting, setting.info.default_option_index
            )

            self.ui.settings_current_option_description_label.setText(
                current_option_description
            )
            self.ui.settings_default_option_description_label.setText(
                default_option_description
            )
            # self.ui.settings_current_option_description_label.setStyleSheet("")

    def format_description(
        self, setting: Setting, option_index: int, custom_option_name: str | None = None
    ) -> str:
        formatted_description = "<b>" + OPTION_PREFIX

        if custom_option_name:
            formatted_description += custom_option_name + "</b>: "
        else:
            formatted_description += (
                setting.info.pretty_options[option_index] + "</b>: "
            )

        formatted_description += setting.info.descriptions[option_index]
        return formatted_description

    def update_descriptions(self, target: QObject | None) -> bool:
        if setting := self.get_setting_from_widget(target):
            self.set_setting_descriptions(setting)
        else:
            self.set_setting_descriptions(None)

        return True

    def show_full_descriptions(self, target: QWidget | None) -> bool:
        if target is None or not (setting := self.get_setting_from_widget(target)):
            return True

        description_text = "<b>Current Option</b>:<br>"
        description_text += self.format_description(
            setting, setting.current_option_index
        )
        description_text += "<br><br><b>Default Option</b>:<br>"
        description_text += self.format_description(
            setting, setting.info.default_option_index
        )
        description_text += "<br><br><b>All Options</b>:<br>"

        try:
            widget: QWidget = getattr(self.ui, "setting_" + setting.name)
        except:
            raise Exception(f"Could not find widget for setting: {setting.name}.")

        if isinstance(widget, QSpinBox):
            last_index = len(setting.info.options) - 1

            if is_random := setting.info.options[last_index] == "random":
                last_index -= 1

            description_text += self.format_description(
                setting,
                0,
                custom_option_name=f"{setting.info.options[0]}-{setting.info.options[last_index]}",
            )

            if is_random:
                description_text += "<br>" + self.format_description(setting, -1)
        else:
            for option_index in range(0, len(setting.info.options)):
                description_text += (
                    self.format_description(setting, option_index) + "<br>"
                )

        dialog_title = setting.info.pretty_name + " Options"
        self.main.fi_info_dialog.show_dialog(title=dialog_title, text=description_text)
        return True

    def get_disabled_shuffle_location_names(self) -> list[str]:
        return [
            location.name
            for location in get_disabled_shuffle_locations(
                self.location_table, self.config
            )
        ]
