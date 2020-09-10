#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

import appier

from .. import info
from .. import errors

LOG_LEVELS = (
    "FINEST",
    "FINER",
    "FINE",
    "INFO",
    "WARNING",
    "SEVERE"
)

LOG_LEVELS_M = dict(
    FINEST = "debug",
    FINER = "debug",
    FINE = "info",
    WARNING = "warn",
    SEVERE = "error"
)

class InteractiveDriver(object):

    def __init__(self, owner, **kwargs):
        self.owner = owner

    @staticmethod
    def driver_g(name):
        return globals()[name.capitalize() + "Driver"]

    @staticmethod
    def label_g():
        driver = appier.conf("DRIVER", "selenium")
        return InteractiveDriver.driver_g(driver).label()

    @classmethod
    def label(cls):
        return "Interactive"

    def start(self):
        pass

    def stop(self):
        pass

    def switch_context(self, name, *args, **kwargs):
        raise appier.NotImplementedError()

    def count_context(self, context, *args, **kwargs):
        raise appier.NotImplementedError()

    def clear_storage(self):
        self.clear_cookies()
        self.clear_local_storage()
        self.clear_session_storage()

    def clear_cookies(self):
        raise appier.NotImplementedError()

    def clear_local_storage(self):
        raise appier.NotImplementedError()

    def clear_session_storage(self):
        raise appier.NotImplementedError()

    def get_key(self, name):
        raise appier.NotImplementedError()

    def get(self, url):
        raise appier.NotImplementedError()

    def find_element(self, selector):
        raise appier.NotImplementedError()

    def find_elements(self, selector):
        raise appier.NotImplementedError()

    def find_by_name(self, name):
        raise appier.NotImplementedError()

    def press_key(self, element, key, ensure = True):
        raise appier.NotImplementedError()

    def write_text(self, element, text, ensure = True):
        raise appier.NotImplementedError()

    def click(self, element, ensure = True):
        raise appier.NotImplementedError()

    def ensure_visible(self, element, timeout = None):
        raise appier.NotImplementedError()

    def scroll_to(self, element, sleep = None):
        """
        Scrolls the element on which it's called into the visible area
        of the browser window.

        This operation should be performed in a deterministic way.

        :type element: Element
        :param element: The element to scroll into view.
        :type sleep: int
        :param sleep: The number of seconds to sleep after the scroll
        operation, important for smooth scrolls.
        """

        raise appier.NotImplementedError()

    def highlight(self, elements):
        raise appier.NotImplementedError()

    def lowlight(self, elements):
        raise appier.NotImplementedError()

    def screenshot(self, file_path):
        raise appier.NotImplementedError()

    def switch_tab(self, tab):
        raise appier.NotImplementedError()

    def close_tab(self, tab = None):
        raise appier.NotImplementedError()

    def wrap_outer(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def wrap_inner(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def safe(self, method, *args, **kwargs):
        return self.wrap_outer(self.wrap_inner, method, *args, **kwargs)

    def press_enter(self, element, ensure = True):
        return self.press_key(element, "enter", ensure = ensure)

    @property
    def options(self):
        raise appier.NotImplementedError()

    @property
    def current_url(self):
        raise appier.NotImplementedError()

    @property
    def current_tab(self):
        raise appier.NotImplementedError()

    @property
    def tab_count(self):
        raise appier.NotImplementedError()

    def _wait(self, timeout = None):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self, owner, **kwargs):
        InteractiveDriver.__init__(self, owner, **kwargs)
        self.secure = appier.conf("SEL_SECURE", False, cast = bool)
        self.browser = appier.conf("SEL_BROWSER", "chrome")
        self.browser_cache = appier.conf("SEL_BROWSER_CACHE", True, cast = bool)
        self.maximized = appier.conf("SEL_MAXIMIZED", False, cast = bool)
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)
        self.device = appier.conf("SEL_DEVICE", None)
        self.window_size = appier.conf("SEL_WINDOW_SIZE", "1920x1080")
        self.pixel_ratio = appier.conf("SEL_PIXEL_RATIO", 1, cast = int)
        self.mobile_emulation = appier.conf("SEL_MOBILE_EMULATION", False, cast = bool)
        self.poll_frequency = appier.conf("SEL_POLL_FREQUENCY", None, cast = float)
        self.service_args = appier.conf("SEL_SERVICE_ARGS", [], cast = list)
        self.secure = kwargs.get("secure", self.secure)
        self.browser = kwargs.get("browser", self.browser)
        self.browser_cache = kwargs.get("browser_cache", self.browser_cache)
        self.maximized = kwargs.get("maximized", self.maximized)
        self.headless = kwargs.get("headless", self.headless)
        self.device = kwargs.get("device", self.device)
        self.window_size = kwargs.get("resolution", self.window_size)
        self.window_size = kwargs.get("window_size", self.window_size)
        self.pixel_ratio = kwargs.get("pixel_ratio", self.pixel_ratio)
        self.mobile_emulation = kwargs.get("mobile", self.mobile_emulation)
        self.mobile_emulation = kwargs.get("mobile_emulation", self.mobile_emulation)
        self.poll_frequency = kwargs.get("poll_frequency", self.poll_frequency)
        self.service_args = kwargs.get("service_args", self.service_args)

    @classmethod
    def label(cls):
        import selenium.webdriver
        browser = cls.browser()
        return "Selenium %s (%s/%s)" % (
            selenium.webdriver.__version__,
            browser["name"],
            browser["version"]
        )

    @classmethod
    def browser(cls):
        import selenium.webdriver
        browser = appier.conf("SEL_BROWSER", "chrome")
        browser_cache = appier.conf("SEL_BROWSER_CACHE", True, cast = bool)
        fix_path = appier.conf("SEL_FIX_PATH", True, cast = bool)
        if fix_path: cls._fix_path()
        if browser == "chrome":
            options = selenium.webdriver.ChromeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-browser-side-navigation")
            options.add_argument("--headless")
            if not browser_cache:
                options.add_argument("--disable-application-cache")
            if sys.platform.startswith("linux"):
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
            instance = selenium.webdriver.Chrome(options = options)
            try:
                name = instance.capabilities.get("browserName", None)
                version = instance.capabilities.get("browserVersion", None)
            finally:
                instance.quit()
        elif browser == "firefox":
            options = selenium.webdriver.FirefoxOptions()
            options.headless = True
            options.set_preference("devtools.console.stdout.content", True)
            instance = selenium.webdriver.Firefox(options = options)
            try:
                name = instance.capabilities.get("browserName", None)
                version = instance.capabilities.get("browserVersion", None)
            finally:
                instance.quit()
        else:
            raise appier.OperationalError(
                message = "Unknown browser '%s'" % browser
            )
        return dict(
            name = name,
            version = version
        )

    @classmethod
    def _fix_path(cls, paths = ("/usr/local/bin",)):
        path = os.environ.get("PATH", "")
        separator = ";" if os.name == "nt" else ":"
        path_s = path.split(separator)
        for _path in paths:
            if _path in path_s: continue
            path_s.append(_path)
        os.environ["PATH"] = separator.join(path_s)

    def stop(self):
        self._flush_log()
        InteractiveDriver.stop(self)

    def clear_cookies(self):
        self.instance.delete_all_cookies()

    def clear_local_storage(self):
        self.instance.execute_script("localStorage.clear();")

    def clear_session_storage(self):
        self.instance.execute_script("sessionStorage.clear();")

    def get(self, url):
        return self.instance.get(url)

    def find_element(self, selector):
        return self.instance.find_element_by_css_selector(selector)

    def find_elements(self, selector):
        return self.instance.find_elements_by_css_selector(selector)

    def find_by_name(self, name):
        return self.instance.find_element_by_name(name)

    def find_element_by_css_selector(self, selector):
        return self.find_element(selector)

    def find_elements_by_css_selector(self, selector):
        return self.find_elements(selector)

    def find_element_by_name(self, name):
        return self.find_by_name(name)

    def press_key(self, element, key, ensure = True):
        # in case the ensure flag is set makes sure that the element
        # is visible in an interactable way
        if ensure: self.ensure_visible(element)

        key = self._resolve_key(key)
        element.send_keys(key)
        return element

    def write_text(self, element, text, ensure = True):
        # in case the ensure flag is set makes sure that the element
        # is visible in an interactable way
        if ensure: self.ensure_visible(element)

        # sends the complete set of keys defined in the text
        # to the element and then returns it
        element.send_keys(text)
        return element

    def click(self, element, ensure = True):
        from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException, WebDriverException

        try:
            # in case the ensure flag is set makes sure that the element
            # is visible in an interactable way
            if ensure: self.ensure_visible(element)

            # moves the mouse to the element according to the pre-defined
            # pivot, this will allow proper clicking
            self._move_to(element)

            # runs the click operation directly on the element without any
            # kind of previous interaction as expected
            element.click()
        except (
            ElementClickInterceptedException,
            ElementNotVisibleException,
            WebDriverException
        ) as exception:
            self.owner.breadcrumbs.debug("Element is not \"clickable\" because: %s (%s)" % (
                exception,
                exception.__class__
            ))
            return None

        # returns the element object to the caller so that it can
        # be piped in a chain of operations
        return element

    def ensure_visible(self, element, timeout = None):
        # starts the operation by moving the cursor to the outside of the element
        # this ensures that the cursor is not "moving over" the element
        self._move_outside(element, raise_e = False)

        # "installs" the global event listeners for visibility detection
        # on the current target element, to be used by the try visible test
        self.__install_listener(element)

        try:
            self.wrap_outer(
                lambda: self._wait(timeout = timeout).until(
                    lambda d: self._try_visible(element),
                    "Element (%s) never became visible" % element._text()
                )
            )
        except errors.TimeoutError:
            try: self.__highlight(element)
            except Exception: pass
            raise
        finally:
            self.__uninstall_listener(element)

        # returns the element object so that in can be chained in multiple
        # operations (functional design decision)
        return element

    def scroll_to(self, element, position = "center", sleep = None):
        # builds the proper options string taking into account the offset
        # in terms of positioning of the element in the scroll
        if position == "center": options = "{ block: \"center\", inline: \"center\" }"
        else: options = ""

        # as Selenium doesn't automatically support automatically scrolling
        # in elements inside the page, such as when using an iframe or
        # overflow scroll, therefore we must rely on Web API `Element.scrollIntoView()`
        # that allows proper scroll operation into element
        self.instance.execute_script("arguments[0].scrollIntoView(%s);" % options, element)

        # when triggering a smooth scroll, the element may take some time to
        # be displayed in the desired position, hence the optional sleep
        if sleep: time.sleep(sleep)

        # returns the element back to the caller method, ready to be used
        # in a chained call strategy of execution
        return element

    def highlight(self, elements):
        if not isinstance(elements, (list, tuple)):
            elements = (elements,)
        for element in elements:
            self.__highlight(element)
        return elements

    def lowlight(self, elements):
        if not isinstance(elements, (list, tuple)):
            elements = (elements,)
        for element in elements:
            self.__lowlight(element)
        return elements

    def screenshot(self, file_path):
        self.instance.save_screenshot(file_path)

    def switch_tab(self, tab):
        try:
            new_window_handle = self.instance.window_handles[tab]
            self.instance.switch_to.window(new_window_handle)
        except IndexError:
            raise errors.UnexistingTabError(tab = tab, tab_count = self.tab_count)

    def close_tab(self, tab = None):
        tab = tab or self.current_tab

        if self.tab_count <= 1:
            raise errors.CloseTabError(
                message = "There is only a single tab, so you can't close it"
            )
        if tab >= self.tab_count:
            raise errors.UnexistingTabError(
                tab = tab,
                tab_count = self.tab_count
            )

        # saves the current tab in question so that we can restore
        # its selection at the end of the operation
        current_tab = self.current_tab

        tab_window_handle = self.instance.window_handles[tab]
        self.instance.switch_to.window(tab_window_handle)
        self.instance.close()

        if current_tab == tab: self.switch_tab(max(0, current_tab - 1))
        else: self.switch_tab(current_tab)

    def wrap_outer(self, method, *args, **kwargs):
        from selenium.common.exceptions import TimeoutException
        try:
            return method(*args, **kwargs)
        except TimeoutException as exception:
            raise errors.TimeoutError(message = exception.msg)

    def wrap_inner(self, method, *args, **kwargs):
        """
        Wraps the method being waited on to tolerate some exceptions since
        in most cases these are transitory conditions that shouldn't break
        the test.

        :type method: Function
        :param method: The method that is going to be executed in a wrapped
        fashion to properly handle exceptions.
        :rtype Function
        :return: The method wrapped on a try-catch for exceptions.
        """

        from selenium.common.exceptions import WebDriverException
        try: return method(*args, **kwargs)
        except (WebDriverException, AssertionError) as exception:
            self.owner.breadcrumbs.debug("Got exception while waiting: %s" % exception)
            return None

    @property
    def options(self):
        return dict(
            secure = self.secure,
            browser = self.browser,
            browser_cache = self.browser_cache,
            maximized = self.maximized,
            headless = self.headless,
            device = self.device,
            window_size = self.window_size,
            pixel_ratio = self.pixel_ratio,
            mobile_emulation = self.mobile_emulation,
            poll_frequency = self.poll_frequency,
            service_args = self.service_args
        )

    @property
    def current_url(self):
        return self.instance.current_url

    @property
    def current_tab(self):
        return self.instance.window_handles.index(self.instance.current_window_handle)

    @property
    def tab_count(self):
        return len(self.instance.window_handles)

    @property
    def instance(self):
        cls = self.__class__

        # in case there's already an instance defined in the class
        # and it is still considered valid then re-uses it
        if hasattr(cls, "_instance") and cls._instance and\
            hasattr(cls, "_options") and self.options == cls._options:
            return cls._instance

        import selenium.webdriver

        # in case there's an instance currently available destroys it
        # to avoid possible collision (garbage collection)
        self._destroy_instance()

        # "saves" the currently set options so that they can be used
        # in the definition of the instance to be created
        cls._options = self.options

        if self.browser == "chrome":
            # creates the underlying instance of the Chrome driver
            # that is going to be used in the concrete execution
            cls._instance = selenium.webdriver.Chrome(
                options = self._selenium_options(self.browser),
                desired_capabilities = self._selenium_capabilities(self.browser),
                service_args = self.service_args or None
            )
        elif self.browser == "firefox":
            # creates the underlying Firefox instance using the
            # pre-defined options as expected
            cls._instance = selenium.webdriver.Firefox(
                options = self._selenium_options(self.browser),
                desired_capabilities = self._selenium_capabilities(self.browser),
                firefox_profile = self._selenium_profile(self.browser),
                service_args = self.service_args or None
            )
        else:
            raise appier.OperationalError(
                message = "Unknown browser '%s'" % self.browser
            )

        # in case the browser should be started maximized, then
        # a new argument is added to the list of options
        if self.maximized:
            cls._instance.fullscreen_window()

        # in case the browser should have a specific window size
        # then splits the window size around the specific values
        if self.window_size:
            width, height = (int(value) for value in self.window_size.split("x"))
            cls._instance.set_window_size(width, height)

        # registers the destroy instance method to be called once
        # the runner is finished (proper cleanup)
        self.owner.runner.add_on_finish(self._destroy_instance)

        # returns the final instance of the driver to the caller
        # so that it can be used for operation
        return cls._instance

    def _destroy_instance(self):
        cls = self.__class__
        if not hasattr(cls, "_instance") or not self._instance:
            return
        cls._instance.quit()
        cls._instance = None
        cls._options = None

    def _selenium_options(self, browser = None):
        browser = browser or self.browser
        if not hasattr(self, "_selenium_options_%s" % browser): return None
        return getattr(self, "_selenium_options_%s" % browser)()

    def _selenium_options_chrome(self):
        import selenium.webdriver

        # crates the base object for the options to be used by
        # the Google Chrome browser
        options = selenium.webdriver.ChromeOptions()

        # in case the mobile emulation is required then an extra
        # experimental option is added to allow custom behaviour
        # (including touch, pixel ratio and user agent)
        if self.mobile_emulation:
            width, height = (int(value) for value in self.window_size.split("x", 1))
            user_agent = info.USER_AGENTS.get(self.device, None) if self.device else None
            emulation_options = dict(
                deviceMetrics = dict(
                    width = width,
                    height = height,
                    pixelRatio = self.pixel_ratio,
                    touch = False
                )
            )
            if user_agent: emulation_options["userAgent"] = user_agent
            options.add_experimental_option("mobileEmulation", emulation_options)

        # adds some of the default arguments to be used for the
        # execution of the Google Chrome instance
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-browser-side-navigation")

        # in case the browser cache is disabled then add the correct
        # argument to the list of command line arguments
        if not self.browser_cache:
            options.add_argument("--disable-application-cache")

        # in case the headless mode was selected then an
        # extra argument is added to the set of options
        if self.headless:
            options.add_argument("--headless")

        # fixes issue when running within a docker container
        # since it typically uses /dev/shm shared memory with
        # little space making chrome crash when rendering large pages
        if sys.platform.startswith("linux"):
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")

        # returns the options to the calling method as expected
        # by the current infrastructure
        return options

    def _selenium_options_firefox(self):
        import selenium.webdriver

        # crates the base object for the options to be used by
        # the Mozilla Firefox browser
        options = selenium.webdriver.FirefoxOptions()

        # in case mobile emulation is requested the current test
        # must be skipped as there's no support available
        if self.mobile_emulation: self.owner.skip("Firefox can't run tests that require a mobile device")

        # in case the headless instance option is set propagates
        # it to the Firefox options object
        if self.headless:
            options.headless = True

        # returns the options to the calling method as expected
        # by the current infrastructure
        return options

    def _selenium_capabilities(self, browser):
        return getattr(self, "_selenium_capabilities_%s" % browser)()

    def _selenium_capabilities_chrome(self):
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["loggingPrefs"] = dict(
            browser = "ALL",
            driver = "ALL",
            client = "ALL",
            performance = "ALL"
        )

        return capabilities

    def _selenium_capabilities_firefox(self):
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        capabilities = DesiredCapabilities.FIREFOX
        capabilities["loggingPrefs"] = dict(
            browser = "ALL",
            driver = "ALL",
            client = "ALL",
            performance = "ALL"
        )

        return capabilities

    def _selenium_profile(self, browser):
        return getattr(self, "_selenium_profile_%s" % browser)()

    def _selenium_profile_firefox(self):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

        profile = FirefoxProfile()

        if not self.browser_cache:
            profile.set_preference("browser.cache.disk.enable", False)
            profile.set_preference("browser.cache.memory.enable", False)
            profile.set_preference("browser.cache.offline.enable", False)

        return profile

    def _wait(self, timeout = None):
        from selenium.webdriver.support.ui import WebDriverWait
        kwargs = dict()
        if self.poll_frequency: kwargs["poll_frequency"] = self.poll_frequency
        if timeout == None: timeout = self.owner.timeout
        return WebDriverWait(self.instance, timeout, **kwargs)

    def _move_to(self, element, pivot = "center"):
        element_width = element.size["width"]
        element_height = element.size["height"]

        if pivot == "center":
            return self._move_to_offset(
                element,
                x = int(element_width / 2),
                y = int(element_height / 2)
            )

        if pivot == "left-top":
            return self._move_to_offset(
                element,
                x = 0,
                y = 0
            )

        if pivot == "right-top":
            return self._move_to_offset(
                element,
                x = element_width - 1,
                y = 0
            )

        if pivot == "right-bottom":
            return self._move_to_offset(
                element,
                x = element_width - 1,
                y = element_height - 1
            )

        if pivot == "left-bottom":
            return self._move_to_offset(
                element,
                x = 0,
                y = element_height - 1
            )

    def _move_to_offset(self, element, x = 0, y = 0, safe = False):
        from selenium.webdriver.common.action_chains import ActionChains

        # creates an action chain that will move the mouse into the
        # target offset of coordinates relative to the element
        actions = ActionChains(self.instance)
        if safe: actions.move_to_element_with_offset(element, x, y)
        else: self._move_to_unsafe(actions, element, x, y)
        actions.perform()

        # returns the element that currently has the mouse pointing
        # to it according to the defined offset (if possible)
        return element

    def _move_to_unsafe(self, actions, element, x = 0, y = 0, duration = 5):
        instance = actions.w3c_actions.pointer_action

        if not x == None or not y == None:
            element_rect = element.rect
            left_offset = element_rect["width"] / 2
            top_offset = element_rect["height"] / 2
            left = left_offset * -1 + (x or 0)
            top = top_offset * -1 + (y or 0)
        else:
            left = 0
            top = 0

        instance.source.create_pointer_move(
            duration = duration,
            x = int(left),
            y = int(top),
            origin = element
        )

        return instance

    def _move_outside(self, element, raise_e = True):
        """
        Moves the mouse outside a given element, this should
        ensure proper outside of element position (not hover).

        This method is going to use a series of strategies to
        try to achieve the goal of moving the cursor outside
        of the referred element.

        :type element: Element
        :param element: The element to move outside from.
        :type raise_e: bool
        :param raise_e: If an exception should be raised when
        it's not possible to move outside the element.
        """

        from selenium.common.exceptions import MoveTargetOutOfBoundsException

        # gathers the element's dimensions to be able to calculate other
        # corner's offset positions, for the list of possibilities
        size = element.size
        width, height = size["width"], size["height"]

        # creates the tuple that contains the complete set of strategies
        # for the offset operation to move the cursor outside of the
        # requested element (avoiding collision)
        possibilities = (
            (-1, -1),
            (-1, 0),
            (0, -1),
            (width, -1),
            (width, 0),
            (-1, height),
            (0, height),
            (width, height)
        )

        # iterates over the complete set of offset possibilities
        # and runs the cursor to the requested offset, in case
        # there's no exception the control flow is returned (success)
        for x, y in possibilities:
            try:
                self._move_to_offset(element, x, y)
                return
            except MoveTargetOutOfBoundsException:
                pass

        # raises an operation error as it was not possible to move
        # the cursor outside of the current element using any of
        # the available strategies (only active if the raise~
        # exception flag is set as a parameter)
        if raise_e:
            raise appier.OperationalError(
                message = "Couldn't move outside element"
            )

    def _try_visible(self, element, strategy = "scroll_to"):
        from selenium.common.exceptions import MoveTargetOutOfBoundsException

        # makes sure that the element in testing is still the same that
        # has been originally selected (avoiding possible new elements with
        # the same selection criteria from being used)
        element._ensure_same()

        # prints some debug information on the retry of the visibility
        # test for the element in question
        self.owner.breadcrumbs.debug("Trying visibility on element '%s'" % element.id)

        try:
            # tries to run the cursor movement to the element, this may fail
            # as the element is not currently visible in the viewport
            self._move_to(element)
        except MoveTargetOutOfBoundsException:
            # some drivers raise exceptions when trying to move to elements
            # outside the viewport, we must ignore such exceptions
            pass

        # runs the is visible operation on the element that should guarantee
        # that the element is visible and interactable, if the returns is
        # positive the control flow is returned and the return value is positive
        if self.__is_visible(element): return True

        # executes the try-out strategy to try to make the element visible
        # in the view-port, by default this scrolls the element to the center
        # of the current screen (best possible strategy)
        if strategy == "scroll_to": self.scroll_to(element)

        # moves the element back to the outside of it, so that there's
        # a mouse movement one more time (skeptical move)
        self._move_outside(element, raise_e = False)

        # "resets" the value of the entered flag back to the original value
        # so that the test may be done against the movement to be performed
        self.instance.execute_script("window._entered = false")

        try:
            # tries to run the cursor movement to the element, this may or
            # may not fail according to the success of the strategy
            self._move_to(element)
        except MoveTargetOutOfBoundsException:
            # some drivers raise exceptions when trying to move to elements
            # outside the viewport, we must ignore such exceptions
            pass

        # verifies if the element is visible and interactable and if that's
        # the case returns a positive result and the control flow
        if self.__is_visible(element): return True

        # by default the visibility/interactability of the provided element
        # is assumed to be false (not interactable) as no tests have passed
        return False

    def _resolve_key(self, name):
        from selenium.webdriver.common.keys import Keys
        KEYS = dict(
            enter = Keys.ENTER,
            space = Keys.SPACE,
            backspace = Keys.BACKSPACE,
            left = Keys.LEFT,
            right = Keys.RIGHT,
            up = Keys.UP,
            down = Keys.DOWN,
            page_up = Keys.PAGE_UP,
            page_down = Keys.PAGE_DOWN,
            esc = Keys.ESCAPE,
            cmd = Keys.COMMAND,
            ctrl = Keys.CONTROL,
            tab = Keys.TAB,
            shift = Keys.SHIFT
        )
        return KEYS[name]

    def _flush_log(self, levels = LOG_LEVELS, browser = None):
        browser = browser or self.browser
        if not hasattr(self, "_flush_log_%s" % browser): return
        return getattr(self, "_flush_log_%s" % browser)()

    def _flush_log_chrome(self, levels = LOG_LEVELS):
        from selenium.common.exceptions import WebDriverException

        for name in ("browser", "client", "driver", "performance"):

            try: log = self.instance.get_log(name)
            except WebDriverException as exception:
                self.owner.browser_logger.warn(exception)
                log = []

            for item in log:
                if not item["level"] in levels: continue
                if not "message" in item: continue
                level, message = item["level"], item["message"]
                level_n = LOG_LEVELS_M.get(level, "info")
                level_m = getattr(self.owner.browser_logger, level_n)
                level_m(message.strip())

    def __is_visible(self, element):
        """
        Internal method that verifies the visibility/interactability
        of the provided element taking into account a series of
        previously inserted setup operation.

        There are two strategies within this method one that uses the
        entered flag on window (previously installed handlers) and
        another (unsafer) that uses the :hover query selector.

        Should be used with proper care to avoid unwanted behaviour as
        it's considered an extremely low level function.

        :type element: Element
        :param element: The element to validated for visibility and/or
        intractability (probably for click purposes).
        :rtype: bool
        :return: If the element is currently interactable.
        """

        if not self.secure and self.instance.execute_script("return window._entered"): return True
        if self.instance.execute_script(
            "return Array.from(arguments[0].parentElement.querySelectorAll(\":hover\").values()).includes(arguments[0])",
            element
        ): return True
        return False

    def __install_listener(self, element):
        # sets the initial value of the "entered" global variable and then registers the mouse
        # over event listener that will change the entered flag value
        self.instance.execute_script("window._entered = false")
        self.instance.execute_script("window._handler = function() { window._entered = true; };")
        self.instance.execute_script("arguments[0].addEventListener(\"mouseenter\", window._handler, true);", element)
        self.instance.execute_script("arguments[0].addEventListener(\"mouseover\", window._handler, true);", element)

    def __uninstall_listener(self, element):
        # removes the complete set of global variables and event listeners associated with
        # the "global strategy" for visibility detection of an element
        self.instance.execute_script(
            "arguments[0].removeEventListener(\"mouseover\", window._handler);",
            element
        )
        self.instance.execute_script(
            "arguments[0].removeEventListener(\"mouseenter\", window._handler);",
            element
        )
        self.instance.execute_script("delete window._handler")
        self.instance.execute_script("delete window._entered")

    def __highlight(self, element, color = "#ff0000", sleep = None, safe = True):
        # in case the safe flag is set then both the transition and the
        # animation settings are disabled to make sure that the visual
        # updates are made immediately
        if safe:
            self.instance.execute_script(
                "arguments[0].style.transition = \"none\";",
                element,
            )
            self.instance.execute_script(
                "arguments[0].style.animation = \"none\";",
                element,
            )

        # changes the background color of the target element to make
        # it highlighted in contrast with the other elements
        self.instance.execute_script(
            "arguments[0].style.backgroundColor = \"%s\";" % color,
            element,
        )

        # in case the sleep value is set, then wait a certain amount of time
        # to make sure the UI operations are visible, taking into consideration
        # that due to things like transition and animations the visual operations
        # may take some time to be presented on screen
        if sleep: time.sleep(sleep)

    def __lowlight(self, element, sleep = None, safe = True):
        # in case the safe flag is set then both the transition and the
        # animation settings are re-enabled to make sure that the visual
        # updates are restored back to the original CSS values
        if safe:
            self.instance.execute_script(
                "arguments[0].style.transition = \"\";",
                element,
            )
            self.instance.execute_script(
                "arguments[0].style.animation = \"\";",
                element,
            )

        # removes the background color value back to the "original" unset value
        # so that top level CSS can take action
        self.instance.execute_script(
            "arguments[0].style.backgroundColor = \"\";",
            element,
        )

        # in case the sleep value is set, then wait a certain amount of time
        # to make sure the UI operations are visible, taking into consideration
        # that due to things like transition and animations the visual operations
        # may take some time to be presented on screen
        if sleep: time.sleep(sleep)

class AppiumDriver(InteractiveDriver):

    CONTEXT_MAPPER = dict(
        native = "NATIVE_APP",
        webview = "WEBVIEW_"
    )

    def __init__(self, owner, **kwargs):
        InteractiveDriver.__init__(self, owner, **kwargs)
        self.server_url = appier.conf("APM_SERVER_URK", "http://localhost:4723/wd/hub")
        self.avd = appier.conf("APM_AVD", "Nexus_5X_API_29_x86")
        self.platform = appier.conf("APM_PLATFORM", "Android")
        self.device = appier.conf("APM_DEVICE", "Android Emulator")
        self.package = appier.conf("APM_PACKAGE", "com.platforme.ripe_robin")
        self.activity = appier.conf("APM_ACTIVITY", "com.platforme.ripe_robin.MainActivity")
        self.app_path = appier.conf("APM_APP_PATH", "/Users/gcc/ripe-robin-revamp/android/app/build/outputs/apk/debug/app-debug.apk")
        self.headless = appier.conf("APM_HEADLESS", False, cast = bool)
        self.poll_frequency = appier.conf("APM_POLL_FREQUENCY", None, cast = float)
        self.server_url = kwargs.get("server_url", self.server_url)
        self.avd = kwargs.get("avd", self.avd)
        self.platform = kwargs.get("platform", self.platform)
        self.device = kwargs.get("device", self.device)
        self.package = kwargs.get("package", self.package)
        self.activity = kwargs.get("activity", self.activity)
        self.app_path = kwargs.get("app_path", self.app_path)
        self.headless = kwargs.get("headless", self.headless)
        self.poll_frequency = kwargs.get("poll_frequency", self.poll_frequency)

    @classmethod
    def label(cls):
        import appium.version
        return "Appium %s" % appium.version.version

    def switch_context(self, context, *args, **kwargs):
        if context == "native":
            return self.instance.switch_to.context(self.contexts[0])
        if context == "webview":
            index = kwargs.get("index", 0)
            webview_contexts = [context for context in self.contexts if context.startswith("WEBVIEW_")]
            return self.instance.switch_to.context(webview_contexts[index])
        raise appier.OperationalError(
            message = "Context not supported '%s'" % context
        )

    def count_context(self, context, *args, **kwargs):
        cls = self.__class__
        context_n = cls.CONTEXT_MAPPER.get(context, None)
        return len([context for context in self.contexts if context.startswith(context_n)])

    def find_element(self, selector):
        if self.in_native:
            element = None
            for method in (
                self.find_element_by_accessibility_id,
                self.find_element_by_id
            ):
                element = method(selector)
                if element: break
            return element
        else:
            return self.find_element_by_css_selector(selector)

    def find_elements(self, selector):
        if self.in_native:
            elements = []
            for method in (
                self.find_elements_by_accessibility_id,
                self.find_elements_by_id
            ):
                elements = method(selector)
                if len(elements) > 0: break
            return elements
        else:
            return self.find_elements_by_css_selector(selector)

    def find_element_by_css_selector(self, selector):
        return self.instance.find_element_by_css_selector(selector)

    def find_elements_by_css_selector(self, selector):
        return self.instance.find_elements_by_css_selector(selector)

    def find_element_by_accessibility_id(self, id):
        return self.instance.find_element_by_accessibility_id(id)

    def find_elements_by_accessibility_id(self, id):
        return self.instance.find_elements_by_accessibility_id(id)

    def find_element_by_id(self, id):
        return self.instance.find_element_by_id(id)

    def find_elements_by_id(self, id):
        return self.instance.find_elements_by_id(id)

    def press_key(self, element, key, ensure = True):
        # in case the ensure flag is set makes sure that the element
        # is visible in an interactable way
        if ensure: self.ensure_visible(element)

        key = self._resolve_key(key)
        element.send_keys(key)
        return element

    def write_text(self, element, text, ensure = True):
        # in case the ensure flag is set makes sure that the element
        # is visible in an interactable way
        if ensure: self.ensure_visible(element)

        # sends the complete set of keys defined in the text
        # to the element and then returns it
        element.send_keys(text)
        return element

    def click(self, element, ensure = True):
        from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException, WebDriverException

        try:
            # in case the ensure flag is set makes sure that the element
            # is visible in an interactable way
            if ensure: self.ensure_visible(element)

            # moves the mouse to the element according to the pre-defined
            # pivot, this will allow proper clicking
            self._move_to(element)

            # runs the click operation directly on the element without any
            # kind of previous interaction as expected
            element.click()
        except (
            ElementClickInterceptedException,
            ElementNotVisibleException,
            WebDriverException
        ) as exception:
            self.owner.breadcrumbs.debug("Element is not \"clickable\" because: %s (%s)" % (
                exception,
                exception.__class__
            ))
            return None

        # returns the element object to the caller so that it can
        # be piped in a chain of operations
        return element

    def ensure_visible(self, element, timeout = None):
        return element

    def scroll_to(self, element, position = "center", sleep = None):
        return element

    def wrap_outer(self, method, *args, **kwargs):
        from selenium.common.exceptions import TimeoutException
        try:
            return method(*args, **kwargs)
        except TimeoutException as exception:
            raise errors.TimeoutError(message = exception.msg)

    def wrap_inner(self, method, *args, **kwargs):
        """
        Wraps the method being waited on to tolerate some exceptions since
        in most cases these are transitory conditions that shouldn't break
        the test.

        :type method: Function
        :param method: The method that is going to be executed in a wrapped
        fashion to properly handle exceptions.
        :rtype Function
        :return: The method wrapped on a try-catch for exceptions.
        """

        from selenium.common.exceptions import WebDriverException
        try: return method(*args, **kwargs)
        except (WebDriverException, AssertionError) as exception:
            self.owner.breadcrumbs.debug("Got exception while waiting: %s" % exception)
            return None

    @property
    def options(self):
        return dict(
            avd = self.avd,
            platform = self.platform,
            device = self.device,
            package = self.package,
            activity = self.activity,
            app_path = self.app_path,
            headless = self.headless,
            poll_frequency = self.poll_frequency
        )

    @property
    def instance(self):
        cls = self.__class__

        # in case there's already an instance defined in the class
        # and it is still considered valid then re-uses it
        if hasattr(cls, "_instance") and cls._instance and\
            hasattr(cls, "_options") and self.options == cls._options:
            return cls._instance

        import appium.webdriver

        # in case there's an instance currently available destroys it
        # to avoid possible collision (garbage collection)
        self._destroy_instance()

        # "saves" the currently set options so that they can be used
        # in the definition of the instance to be created
        cls._options = self.options

        # creates the underlying instance of the Appium driver
        # that is going to be used in the concrete execution
        cls._instance = appium.webdriver.Remote(
            self.server_url,
            desired_capabilities = dict(
                avd = self.avd,
                platformName = self.platform,
                deviceName = self.device,
                appPackage = self.package,
                appActivity = self.activity,
                app = self.app_path,
                isHeadless = self.headless
            )
        )

        # registers the destroy instance method to be called once
        # the runner is finished (proper cleanup)
        self.owner.runner.add_on_finish(self._destroy_instance)

        # returns the final instance of the driver to the caller
        # so that it can be used for operation
        return cls._instance

    @property
    def context(self):
        return self.instance.context

    @property
    def contexts(self):
        return self.instance.contexts

    @property
    def in_native(self):
        return self.context == "NATIVE_APP"

    @property
    def in_webview(self):
        return self.context.startswith("WEBVIEW_")

    def _destroy_instance(self):
        cls = self.__class__
        if not hasattr(cls, "_instance") or not self._instance:
            return
        cls._instance.quit()
        cls._instance = None
        cls._options = None

    def _wait(self, timeout = None):
        from selenium.webdriver.support.ui import WebDriverWait
        kwargs = dict()
        if self.poll_frequency: kwargs["poll_frequency"] = self.poll_frequency
        if timeout == None: timeout = self.owner.timeout
        return WebDriverWait(self.instance, timeout, **kwargs)

    def _move_to(self, element, pivot = "center"):
        return element

    def _flush_log(self, levels = LOG_LEVELS):
        from selenium.common.exceptions import WebDriverException

        for name in ("driver", "server"):
            try: log = self.instance.get_log(name)
            except WebDriverException as exception:
                self.owner.browser_logger.warn(exception)
                log = []

            for item in log:
                if not item["level"] in levels: continue
                if not "message" in item: continue
                level, message = item["level"], item["message"]
                level_n = LOG_LEVELS_M.get(level, "info")
                level_m = getattr(self.owner.browser_logger, level_n)
                level_m(message.strip())
