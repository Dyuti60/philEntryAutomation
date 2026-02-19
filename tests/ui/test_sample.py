def test_homepage(page):
    page.goto("/")
    assert page.url is not None
    #assert False