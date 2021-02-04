"""
Module contains Base View used for all Admin Views. This View is further extended by: Dashboard, Audience,
Product, Backend, and AccountSettings Views. All of them creates basic page structure for respective
Admin portal pages.
:TODO Add locators/menus for basic pages
"""
from typing import List
from widgetastic.widget import GenericLocatorWidget, View, Text

from testsuite.ui.navigation import step, Navigable
from testsuite.ui.widgets import Link, ContextMenu, NavigationMenu


class BaseAdminView(View, Navigable):
    """
    Basic representation of logged in admin portal page.
    All admin portal page should inherits from this class.
    """
    endpoint_path = ''
    explorer_menu = Link("//div[@id='api_selector']//a[@title='Context Selector']/span")
    threescale_menu_logo = GenericLocatorWidget('//*[@id="user_widget"]/a/div')
    support_link = Link("//a[@href='//access.redhat.com/products/red-hat-3scale#support']")
    user_session = GenericLocatorWidget("//a[@href='#session-menu']")
    user_logout_link = Link("//a[@href='/p/logout']")

    context_menu = ContextMenu()

    def logout(self):
        """Method which logouts current user from admin portal"""
        self.user_session.click()
        self.user_logout_link.click()

    @step("AudienceNavView")
    def audience(self):
        """Selects Audience item from ContextSelector"""
        self.context_menu.item_select("Audience")

    @step("ProductNavView")
    def products(self):
        """Selects Products item from ContextSelector"""
        self.context_menu.item_select("Products")

    @step("BackendNavView")
    def backends(self):
        """Selects Backends item from ContextSelector"""
        self.context_menu.item_select("Backends")

    @step("SettingsNavView")
    def settings(self):
        """Select Account Settings from ContextSelector"""
        self.context_menu.item_select("Account Settings")

    @step("DashboardView")
    def dashboard(self):
        """Select Dashboard from ContextSelector"""
        self.context_menu.item_select("Dashboard")

    # pylint: disable=invalid-overridden-method
    def is_displayed(self):
        return self.threescale_menu_logo.is_displayed \
               and self.support_link.is_displayed \
               and self.explorer_menu.is_displayed


class BaseNavView(BaseAdminView):
    """Class adding Navigation menu. Used by Audience, Product, Backend and Settings NavViews """
    NAV_ITEMS: List[str]
    nav = NavigationMenu(id='mainmenu')

    @step("@href")
    def step(self, href):
        """Perform step to specific item in Navigation with use of href locator"""
        self.nav.select_href(href)

    def is_displayed(self):
        if not self.nav.is_displayed:
            return False

        present_nav_items = set(self.nav.nav_links()) & set(self.NAV_ITEMS)
        return BaseAdminView.is_displayed(self) and len(present_nav_items) > 3

    def prerequisite(self):
        return BaseAdminView


class AudienceNavView(BaseNavView):
    """Base View for all Audience/Account pages. Features audience vertical navigation menu"""
    NAV_ITEMS = ['Accounts', 'Applications', 'Billing', 'Developer Portal', 'Messages']


class ProductNavView(BaseNavView):
    """Base View for all Product pages. Features product vertical navigation menu"""
    NAV_ITEMS = ['Overview', 'Analytics', 'Applications', 'ActiveDocs', 'Integration']


class BackendNavView(BaseNavView):
    """Base View for all Backends pages. Features backend vertical navigation menu"""
    NAV_ITEMS = ['Overview', 'Analytics', 'Methods & Metrics', 'Mapping Rules']


class SettingsNavView(BaseNavView):
    """Base View for all Account Settings pages. Features settings vertical navigation menu"""
    NAV_ITEMS = ['Overview', 'Personal', 'Users', 'Integrate', 'Export']


# pylint: disable=invalid-overridden-method
class DashboardView(BaseAdminView):
    """Dashboard view page object that can be found on endpoint_path"""
    endpoint_path = '/p/admin/dashboard'

    def is_displayed(self):
        return BaseAdminView.is_displayed(self) and self.endpoint_path in self.browser.url

    def prerequisite(self):
        return BaseAdminView


class AccessDeniedView(View):
    """Base Access Denied page object"""
    logo = GenericLocatorWidget(locator="//h1[@id='logo']/span[@class='logo-3scale--svg']")
    title = Text(locator='//*[@id="content"]/h1[2]')
    text_message = Text(locator='//*[@id="content"]/p')

    def is_displayed(self):
        return self.title.text == "Access Denied" and \
               self.text_message.text == "Sorry, you do not have permission to access this page." and\
               self.logo.is_displayed


class NotFoundView(View):
    """Base Not Found/404 page object"""
    logo = GenericLocatorWidget(locator="//h1[@id='logo']/span[@class='logo-3scale--svg']")
    title = Text(locator='//*[@id="content"]/h1[2]')
    text_message = Text(locator='//*[@id="content"]/p')

    def is_displayed(self):
        return self.title.text == "Not Found" and \
               self.text_message.text == "Sorry. We can't find what you're looking for." and \
               self.logo.is_displayed