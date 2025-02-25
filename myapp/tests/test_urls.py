import pytest
from pytest import mark
from django.urls import reverse, resolve, NoReverseMatch
from myapp.views import (
    home,
    issue_map,
    report_issue,
    submitted_issue,
    view_issues,
    assigned_issues,
    login_user,
    register_user,
    logout_view,
    issue_management,
    update_issue,
    delete_issue
)


@mark.parametrize(
        "template_url, kwargs, expected_output, should_fail",
        [
            (
                'not-valid-url', {}, NoReverseMatch, True
            ),

            (
                'home', {}, home, False
            ),

            (
                'login', {}, login_user, False
            ),

            (
                'report_issue', {}, report_issue, False
            ),

            (
                'view_issues', {}, view_issues, False
            ),

            (
                'update_issue', 1, update_issue, False
            ),

            (
                'delete_issue', 2, delete_issue, False
            ),

            (
                'logout', {}, logout_view, False
            ),

            (
                'register', {}, register_user, False
            ),

            (
                'issue_management', {}, issue_management, False
            ),

            (
                'assigned_issues', {}, assigned_issues, False
            ),

            (
                'issue_submitted', {}, submitted_issue, False
            ),

            (
                'issue_map', {}, issue_map, False
            )
        ]
)
def test_urls(template_url, kwargs, expected_output, should_fail):

    if should_fail:
        with pytest.raises(NoReverseMatch):
            reverse(template_url)
    if kwargs:
        path = reverse(template_url, args=[kwargs])
    else:
        path = reverse(template_url)

    assert resolve(path).func == expected_output
