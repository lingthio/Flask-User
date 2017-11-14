- Consider replacing @allow_unconfirmed_email with
  @login_required_allow_unconfirmed_email,
  @roles_accepted_allow_unconfirmed_email, and
  @roles_required_allow_unconfirmed_email
  Pros: No need for global setting g._flask_user_allow_unconfirmed_email
  Cons: Three extra decorators needed
  Decorator X could test for email and then call X_allow_unconfirmed_email

- Increase test coverage
  - 45 lines in user_manager_views: invite_user_view
  - 6 lines in user_manager_views: if invite_token and um.UserInvitationClass:
  - 4 lines Test with UserEmailClass
  - 2 lines in user_manager__utils: confirm_email_view with invalid token
  - 3 lines in forms: Test with USER_SHOW_EMAIL_DOES_NOT_EXIST
  - 3 lines in user_manager__views: edit_user_profile_view

- For autodocs of interfaces, init params are show twice
  - Idea:
  - conf.py: remove autoclass_content = 'both'
  - All classes except interfaces: Move __init__ docstring to class docstring

- API docs:
  Submenu1: Intro, UserManager, Decorators, Forms, Views, Interfaces
  UserManager submenu2: UserManager, Settings, Utils, Views
  Why two views?
  Move Managers to Intefaces

