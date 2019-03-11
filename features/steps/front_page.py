from behave import given, when, then

from django.contrib.auth.models import User, Permission

from selenium.common.exceptions import NoSuchElementException


@given("an anonymous user")
def given_an_anonymous_user(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(context.base_url)
    assert 'MyTardis' in context.browser.page_source


@given("a logged-in user")
def given_a_logged_in_user(context):
    """
    :type context: behave.runner.Context
    """
    user = User.objects.create_user(
            username="testuser1",
            password="testpass",  # nosec
            email="testuser1@example.com",
            first_name="Test",
            last_name="User1")
    user.user_permissions.add(Permission.objects.get(codename='add_experiment'))
    user.user_permissions.add(Permission.objects.get(codename='change_experiment'))
    user.user_permissions.add(Permission.objects.get(codename='add_dataset'))
    user.user_permissions.add(Permission.objects.get(codename='change_objectacl'))
    context.browser.get(context.base_url + "/login/")
    username_field = context.browser.find_element_by_id('id_username')
    username_field.send_keys(user.username)
    password_field = context.browser.find_element_by_id('id_password')
    password_field.send_keys("testpass")
    login_form = context.browser.find_element_by_id('login-form')
    login_form.submit()


@when("they open the index url")
def they_open_the_index_url(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(context.base_url)


@then("they see the front page")
def they_see_the_front_page(context):
    """
    :type context: behave.runner.Context
    """
    try:
        login_button = context.browser.find_element_by_id("login-button")
        found_login_button = True
    except NoSuchElementException:
        found_login_button = False
    context.test.assertTrue(found_login_button)

    console_errors = []
    for error in context.browser.get_log('browser'):
        console_errors.append(error)
    context.test.assertEqual(
        len(console_errors), 0, str(console_errors))

@then("they see the user menu")
def they_see_the_user_menu(context):
    """
    :type context: behave.runner.Context
    """
    try:
        user_menu = context.browser.find_element_by_id("user-menu")
        found_user_menu = True
    except NoSuchElementException:
        found_user_menu = False
    context.test.assertTrue(found_user_menu)
