#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

import appier

from .. import errors

class InteractiveDriver(object):

    def __init__(self, owner):
        self.owner = owner

    def start(self):
        pass

    def stop(self):
        pass

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

    def focus(self, element):
        raise appier.NotImplementedError()

    def press_key(self, element, key):
        raise appier.NotImplementedError()

    def write_text(self, element, text):
        raise appier.NotImplementedError()

    def press_enter(self, element):
        return self.press_key(element, "enter")

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

    def screenshot(self, file_path):
        raise appier.NotImplementedError()

    def wrap_outer(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def wrap_inner(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def safe(self, method, *args, **kwargs):
        return self.wrap_outer(self.wrap_inner, method, *args, **kwargs)

    @property
    def current_url(self):
        raise appier.NotImplementedError()

    def _wait(self, timeout = None):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self, owner):
        InteractiveDriver.__init__(self, owner)
        self.secure = appier.conf("SEL_SECURE", False, cast = bool)
        self.maximized = appier.conf("SEL_MAXIMIZED", False, cast = bool)
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)
        self.window_size = appier.conf("SEL_WINDOW_SIZE", "1920x1080")
        self.poll_frequency = appier.conf("SEL_POLL_FREQUENCY", None, cast = float)

    def stop(self):
        self._flush_log()
        InteractiveDriver.stop(self)

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

    def focus(self, element):
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(self.instance)
        actions.move_to_element(element)
        actions.perform()

    def press_key(self, element, key):
        key = self._resolve_key(key)
        element.send_keys(key)
        return element

    def write_text(self, element, text):
        element.send_keys(text)
        return element

    def click(self, element, ensure = True):
        from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException, WebDriverException

        try:
            # in case the ensure flag is set makes sure that the element
            # is visible (in an interactable way) to be then clicked
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
        # waits until the element is visible from a document point of view
        # no scroll ensuring a z index collision is enforced
        self._wait(timeout = timeout).until(
            lambda d: element.is_displayed(),
            "Element never became visible at block (display and opacity)"
        )

        # starts the operation by moving the cursor to the outside of the element
        # this ensures that the cursor is not "moving over" the element
        self._move_outside(element)

        # sets the initial value of the "entered" global variable and then registers the mouse
        # over event listener that will change the entered flag value
        self.instance.execute_script("window._entered = false")
        self.instance.execute_script("window._handler = function() { window._entered = true; };")
        self.instance.execute_script("arguments[0].addEventListener(\"mouseenter\", window._handler, true);", element)
        self.instance.execute_script("arguments[0].addEventListener(\"mouseover\", window._handler, true);", element)

        try:
            self._wait(timeout = timeout).until(
                lambda d: self._try_visible(element),
                "Element never became visible"
            )
        finally:
            self.instance.execute_script("delete window._entered")
            self.instance.execute_script("delete window._handler")
            self.instance.execute_script(
                "arguments[0].removeEventListener(\"mouseenter\", window._handler);",
                element
            )
            self.instance.execute_script(
                "arguments[0].removeEventListener(\"mouseover\", window._handler);",
                element
            )

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

    def screenshot(self, file_path):
        self.instance.save_screenshot(file_path)

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
    def current_url(self):
        return self.instance.current_url

    @property
    def instance(self):
        cls = self.__class__
        if hasattr(cls, "_instance") and cls._instance:
            return cls._instance

        import selenium.webdriver

        # creates the underlying instance of the Chrome driver
        # that is going to be used in the concrete execution
        cls._instance = selenium.webdriver.Chrome(
            chrome_options = self._selenium_options()
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
        cls._instance.close()
        cls._instance = None

    def _selenium_options(self):
        import selenium.webdriver

        # crates the base object for the options to be used by
        # the Google Chrome browser
        options = selenium.webdriver.ChromeOptions()

        # adds some of the default arguments to be used for the
        # execution of the Google Chrome instance
        options.add_argument("--disable-extensions")

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

    def _move_to_offset(self, element, x = 0, y = 0):
        from selenium.webdriver.common.action_chains import ActionChains

        # creates an action chain that will move the mouse into the
        # target offset of coordinates relative to the element
        actions = ActionChains(self.instance)
        actions.move_to_element_with_offset(element, x, y)
        actions.perform()

        # returns the element that currently has the mouse pointing
        # to it according to the defined offset (if possible)
        return element

    def _move_outside(self, element):
        """
        Moves the mouse outside a given element, this should
        ensure proper outside of element position (not hover).

        This method is going to use a series of strategies to
        try to achieve the goal of moving the cursor outside
        of the referred element.

        :type element: Element
        :param element: The element to move outside from.
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
            #(-1, -1),
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

        # raises an operation error as it was not possible
        # to move the cursor outside of the current element
        # using any of the available strategies
        raise appier.OperationalError(message = "Couldn't move outside element")

    def _try_visible(self, element, strategy = "scroll_to"):
        # prints some debug information on the retry of the visibility
        # test for the element in question
        self.owner.breadcrumbs.debug("Trying visibility on element: %s" % element.id)

        # runs the pre-validation of element visibility, to make sure that
        # the element is not yet visible and if that's the case returns
        # immediately (no need to run a scroll operation)
        self._move_to(element)
        if self.__is_visible(element): return True

        # executes the try-out strategy to try to make the element visible
        # in the view-port, by default this scrolls the element to the center
        # of the current screen (best possible strategy)
        if strategy == "scroll_to": self.scroll_to(element)

        # moves the element back to the outside of it and so that there's
        # a mouse movement one more time (skeptical move)
        self._move_outside(element)

        # runs the cursor movement to the element and then verifies the result
        # of the cursor moving operation (to the center of the element)
        self._move_to(element)
        return self.__is_visible(element)

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
            page_down = Keys.PAGE_DOWN
        )
        return KEYS[name]

    def _flush_log(self, levels = ("INFO", "WARN", "ERROR")):
        log = self.instance.get_log("browser")
        for item in log:
            if not item["level"] in levels: continue
            self.owner.breadcrumbs.info(log)

    def __is_visible(self, element):
        if self.instance.execute_script("return window._entered"): return True
        if self.instance.execute_script(
            "return Array.from(arguments[0].parentElement.querySelectorAll(\":hover\").values()).includes(arguments[0])",
            element
        ): return True
        return False
